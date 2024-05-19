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


class App:
    def __init__(self) -> None:
        self.raw_text: str = ""
        self.text_chunks: List[str] = []
        self.vectorstore: Optional[Any] = None
        self.conversation_chain: Optional[ConversationalRetrievalChain] = None

    def get_pdf_text(self, pdf_docs) -> str:
        for pdf_document in pdf_docs:
            pdf_reader = PdfReader(pdf_document)
            for page in pdf_reader.pages:
                self.raw_text += page.extract_text()

    def get_text_chunks(self, raw_text: str) -> List[str]:
        text_splitter = CharacterTextSplitter(
            separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
        )
        self.text_chunks = text_splitter.split_text(raw_text)
        # return self.text_chunks

    def get_vectorstore(self, text_chunks) -> None:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )  # "text-embedding-ada-002"
        self.vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)

    def get_conversation_chain(self, vectorstorestore) -> None:
        llm = ChatOpenAI()
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm, retriever=vectorstorestore.as_retriever(), memory=memory
        )

    def handle_user_input(self, question):
        response = st.session_state.conversation({"question": question})

        st.session_state.chat_history = response["chat_history"]
        reverse_chat_history = reversed(st.session_state.chat_history)

        st.write(response)

        for i, message in enumerate(
            reverse_chat_history
        ):  # st.session_state.chat_history
            if i % 2 == 0:
                st.write(
                    user_template.replace("{{MSG}}", message.content),
                    unsafe_allow_html=True,
                )
            else:
                st.write(
                    bot_template.replace("{{MSG}}", message.content),
                    unsafe_allow_html=True,
                )

    def handle_user_input_reversed(self, question):
        response = st.session_state.conversation({"question": question})
        st.session_state.chat_history = response["chat_history"]

        # Create pairs of user and bot messages
        chat_pairs = []
        for i in range(0, len(st.session_state.chat_history), 2):
            user_message = st.session_state.chat_history[i]
            bot_message = (
                st.session_state.chat_history[i + 1]
                if i + 1 < len(st.session_state.chat_history)
                else None
            )
            chat_pairs.append((user_message, bot_message))

        # Reverse the list of pairs
        reversed_chat_pairs = reversed(chat_pairs)

        # Display the chat history
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

    def chat_bot_app(self):
        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = None

        st.write(css, unsafe_allow_html=True)

        st.header("Chat with PDFs knowledge base :books:")
        question = st.text_input("Ask questions about the documents:")
        if question:
            # self.handle_user_input(question)
            self.handle_user_input_reversed(question)

        with st.sidebar:
            st.subheader("Your documents")
            pdf_documents = st.file_uploader(
                "Upload your documents", accept_multiple_files=True
            )
            if st.button("Submit your documents"):
                with st.spinner("Your documents are being processed..."):
                    self.get_pdf_text(pdf_documents)
                    self.get_text_chunks(self.raw_text)
                    self.get_vectorstore(self.text_chunks)
                    self.get_conversation_chain(self.vectorstore)
                    st.session_state.conversation = self.conversation_chain


def main():
    st.set_page_config(page_title="Chat with PDFs knowledge base", page_icon=":books:")
    load_dotenv()
    my_little_chatbot = App()
    my_little_chatbot.chat_bot_app()


if __name__ == "__main__":
    main()
