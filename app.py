import streamlit as st
from dotenv import load_dotenv  # type: ignore
from PyPDF2 import PdfReader  # type: ignore

from langchain.text_splitter import CharacterTextSplitter  # type: ignore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI  # type: ignore
from langchain_community.vectorstores import FAISS  # type: ignore
from langchain.memory.buffer import ConversationBufferMemory  # type: ignore
from langchain.chains import ConversationalRetrievalChain  # type: ignore  # type: ignore

from typing import List, Optional, Any

from htmlTemplates import css, bot_template, user_template  # type: ignore
from conv_manager import ConversationManager  # type: ignore
from vectorstore import VectorStoreManager  # type: ignore
from text_utils import PDFHandler, TextSplitter  # type: ignore

# class PDFHandler:
#     """PDFHandler class for extracting raw text from provided PDF documents.

#     Methods:
#         get_pdf_text(self, pdf_docs)
#     """

#     def __init__(self) -> None:
#         """Initializes a new instance of the class
#         and sets the `raw_text` attribute with an empty string.

#         Parameters:
#             None
#         Returns:
#             None
#         """
#         self.raw_text: str = ""

#     def get_pdf_text(self, pdf_docs: List[Any]) -> str:
#         """Extracts raw text from a list of provided PDF documents.

#         Args:
#             pdf_docs (List[Any]): A list of PDF documents to be processed.

#         Returns:
#             str: The raw text extracted from the provided PDF documents.

#         """
#         raw_text_chunks = []
#         for pdf_document in pdf_docs:
#             pdf_reader = PdfReader(pdf_document)
#             raw_text_chunks.extend(page.extract_text() for page in pdf_reader.pages)
#         self.raw_text = "".join(raw_text_chunks)
#         return self.raw_text


# class TextSplitter:
#     """TextSplitter class for splitting raw text into smaller chunks for further processing.

#     Methods:
#         get_text_chunks(self, raw_text: str)
#     """

#     def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200) -> None:
#         """
#         Initializes a new instance of the TextSplitter class with the specified chunk size and overlap.

#         Args:
#             chunk_size (int, optional): The size of each text chunk. Defaults to 1000.
#             chunk_overlap (int, optional): The overlap between adjacent text chunks. Defaults to 200.

#         Returns:
#             None
#         """
#         self.chunk_size = chunk_size
#         self.chunk_overlap = chunk_overlap
#         self.text_chunks: List[str] = []

#     def get_text_chunks(self, raw_text: str) -> List[str]:
#         """Splits raw text into chunks based on the specified size and overlap

#         Args:
#             raw_text (str): The raw text to be split into chunks.

#         Returns:
#             List[str]: A list of text chunks.

#         """
#         text_splitter = CharacterTextSplitter(
#             separator="\n",
#             chunk_size=self.chunk_size,
#             chunk_overlap=self.chunk_overlap,
#             length_function=len,
#         )
#         self.text_chunks = text_splitter.split_text(raw_text)
#         return text_splitter.split_text(raw_text)


# class VectorStoreManager:
#     """VectorStoreManager class for managing the creation and
#     retrieval of a vector store.

#     Methods:
#         get_vectorstore(self, text_chunks: List[str])
#     """

#     def __init__(self) -> None:
#         """Initializes a new instance of the class with the `vectorstore` attribute set to `None`.

#         Args:
#             None
#         Returns:
#             None
#         """
#         self.vectorstore: Optional[Any] = None

#     def get_vectorstore(self, text_chunks: List[str]) -> Any:
#         """Creates a vector store from text chunks.

#         Args:
#             text_chunks (List[str]): A list of text chunks to be stored in the
#             vector store as embeddings.

#         Returns:
#             Any: The created vector store.
#         """
#         embeddings = OpenAIEmbeddings(
#             model="text-embedding-3-small"
#         )  # "text-embedding-ada-002"
#         self.vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
#         return self.vectorstore


# class ConversationManager:
#     """ConversationManager class for managing the conversational chain and user input.

#     Methods:
#         get_conversation_chain(self, vectorstore)
#         handle_user_input(self, question: str)
#     """

#     def __init__(self) -> None:
#         """Initializes a new instance of the class with the `conversation_chain`
#         attribute set to `None`.

#         Parameters:
#             None
#         Returns:
#             None
#         """
#         self.conversation_chain: Optional[ConversationalRetrievalChain] = None

#     def get_conversation_chain(self, vectorstore) -> ConversationalRetrievalChain:
#         """Generates a conversational hstory chain using the given vectorstore.

#         Args:
#             vectorstore (VectorStore): The vectorstore containing the embeddings for the text chunks.
#         Returns:
#             ConversationalRetrievalChain: The generated conversational retrieval chain.
#         """
#         llm = ChatOpenAI()
#         memory = ConversationBufferMemory(
#             memory_key="chat_history", return_messages=True
#         )
#         self.conversation_chain = ConversationalRetrievalChain.from_llm(
#             llm=llm, retriever=vectorstore.as_retriever(), memory=memory
#         )
#         return self.conversation_chain

#     def handle_user_input(self, question: str) -> dict:
#         """Handles user input and updates the session state with the chat history.

#         Args:
#             question (str): The user's question.
#         Returns:
#             dict: A dictionary containing the chat history and the response generated by the conversation chain.
#         """
#         response = st.session_state.conversation({"question": question})
#         st.session_state.chat_history = response["chat_history"]
#         return response


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
            self.display_chat_history(response)

        with st.sidebar:
            st.subheader("Your documents")
            pdf_documents = st.file_uploader(
                "Upload your documents", accept_multiple_files=True
            )
            if st.button("Submit your documents"):
                with st.spinner("Your documents are being processed..."):
                    raw_text = self.pdf_processor.get_pdf_text(pdf_documents)
                    text_chunks = self.text_chunker.get_text_chunks(raw_text)
                    vectorstore = self.vectorstore_manager.get_vectorstore(text_chunks)
                    conversation_chain = (
                        self.conversation_manager.get_conversation_chain(vectorstore)
                    )
                    st.session_state.conversation = conversation_chain


def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="Chat with PDFs knowledge base", page_icon=":books:")
    load_dotenv()
    chat_bot_app = ChatBotApp()
    chat_bot_app.run_app()


if __name__ == "__main__":
    main()
