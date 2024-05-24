import streamlit as st
from dotenv import load_dotenv  # type: ignore

from htmlTemplates import css, bot_template, user_template  # type: ignore
from conv_manager import ConversationManager  # type: ignore
from vectorstore import VectorStoreManager  # type: ignore
from text_utils import PDFHandler, TextSplitter  # type: ignore


class ChatBotApp:
    """Main application class for the ChatBot.

    Methods:
        run_app(self)
        display_chat_history(self, response: dict)
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class with the `pdf_processor`, `text_chunker`, `vectorstore_manager`,
        and `conversation_manager` attributes set to instances of their respective classes.

        Args:
            None
        Returns:
            None
        """
        self.pdf_processor = PDFHandler()
        self.text_chunker = TextSplitter()
        self.vectorstore_manager = VectorStoreManager()
        self.conversation_manager = ConversationManager()

    def display_chat_history(self, response: dict) -> None:
        """Display the chat history from the given response.

        Args:
            response (dict): A dictionary containing the chat history.
        Returns:
            None

        This function retrieves the chat history from the provided response and displays it in the Streamlit session state.
        The chat history is stored in the `chat_history` key of the response dictionary.
        The function creates pairs of user and bot messages from the chat history. It iterates over the chat history in reverse order,
        creating pairs of consecutive messages. That is done so that the user doesn't have to scroll down to see the lates answer.
        If there is an odd number of messages in the chat history, the last message is ignored.
        For each pair of user and bot messages, the function writes the user message to the Streamlit session using the `user_template`
        and the bot message (if it exists) using the `bot_template`.
        """

        chat_history = response["chat_history"]
        st.session_state.chat_history = chat_history

        chat_pairs = [
            (
                chat_history[i],
                chat_history[i + 1] if i + 1 < len(chat_history) else None,
            )
            for i in range(0, len(chat_history), 2)
        ]
        reversed_chat_pairs = reversed(chat_pairs)

        for user_message, bot_message in reversed_chat_pairs:
            st.write(
                user_template.replace("{{MSG}}", user_message.content),
                unsafe_allow_html=True,
            )
            if bot_message:
                st.write(
                    bot_template.replace("{{MSG}}", bot_message.content),
                    unsafe_allow_html=True,
                )

    def run_app(self) -> None:
        """Runs the main application.

        This function initializes the session state if it doesn't already exist.
        It then writes the CSS to the Streamlit session and displays the header "Chat with PDFs knowledge base".
        It prompts the user to enter a question about the documents using the `st.text_input` function.
        If a question is provided, it calls the `handle_user_input` method of the `conversation_manager` to get the response.
        The response is then passed to the `display_chat_history` method that keeps the managaes the chat history.
        In the sidebar, it prompts the user to upload their documents using the `st.file_uploader` function.
        If the user clicks the "Submit your documents" button, it displays a spinner while processing the documents.
        It calls the `get_pdf_text` method of the `pdf_processor` to get the raw text from the uploaded documents.
        It then calls the `get_text_chunks` method of the `text_chunker` to get the text chunks from the raw text.
        It calls the `get_vectorstore` method of the `vectorstore_manager` to create a vector store from the text chunks.
        Finally, it calls the `get_conversation_chain` method of the `conversation_manager` to create a conversation chain using the vector store.
        The conversation chain is stored in the session state.

        Args:
            None
        Returns:
            None
        """
        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = None

        st.write(css, unsafe_allow_html=True)
        st.header("Chat with PDFs knowledge base :books:")

        question = st.text_input("Ask questions about the documents:")
        if question:
            response = self.conversation_manager.handle_user_input(question)
            if "error" in response:
                st.error(response["error"])
            else:
                self.display_chat_history(response)

        with st.sidebar:
            st.subheader("Your documents")
            pdf_documents = st.file_uploader(
                "Upload your documents", accept_multiple_files=True
            )

            if st.button("Submit your documents"):
                with st.spinner("Your documents are being processed..."):
                    try:
                        raw_text = self.pdf_processor.get_pdf_text(pdf_documents)
                        text_chunks = self.text_chunker.get_text_chunks(raw_text)
                        vectorstore = self.vectorstore_manager.get_vectorstore(
                            text_chunks
                        )
                        conversation_chain = (
                            self.conversation_manager.get_conversation_chain(
                                vectorstore
                            )
                        )
                        st.session_state.conversation = conversation_chain
                    except ValueError as ve:
                        st.error(str(ve))


def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="Chat with PDFs knowledge base", page_icon=":books:")
    load_dotenv()
    chat_bot_app = ChatBotApp()
    chat_bot_app.run_app()


if __name__ == "__main__":
    main()
