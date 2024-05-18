import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter


class Placeholder:
    def __init__(self):
        pass


class App:
    def __init__(self) -> None:
        # self.page_title = "Chat with PDFs knowledge base"
        # self.raw_text = ""

        pass
        """
            Upewnić się w jaki sposób działa odczytywanie raw 
            tekstu - czy przechowywać go w zmiennej 
            obiektowej czy normalnej zmiennej w pamieci
        """

    def get_pdf_text(self, pdf_docs) -> str:
        raw_text = ""
        for pdf_document in pdf_docs:
            pdf_reader = PdfReader(pdf_document)
            for page in pdf_reader.pages:
                # self.raw_text += page.extract_text()
                raw_text += page.extract_text()
        # return self.raw_text
        return raw_text

    def get_text_chunks(self, raw_text) -> list:
        text_splitter = CharacterTextSplitter(
            separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
        )
        chunks = text_splitter.split_text(raw_text)
        return chunks

    def setup(self):
        st.header("Chat with PDFs knowledge base :books:")
        st.text_input("Ask questions about the documents:")

        with st.sidebar:
            st.subheader("Your documents")
            pdf_documents = st.file_uploader(
                "Upload your documents", accept_multiple_files=True
            )
            if st.button("Submit your documents"):
                with st.spinner("Your documents are being processed..."):
                    # self.raw_pdf_text = self.get_pdf_text(pdf_documents)
                    # self.get_pdf_text(pdf_documents)
                    raw_pdf_text = self.get_pdf_text(pdf_documents)

                    text_chunks = self.get_text_chunks(raw_pdf_text)


def main():
    st.set_page_config(page_title="Chat with PDFs knowledge base", page_icon=":books:")
    load_dotenv()
    my_little_chatbot = App()
    my_little_chatbot.setup()


if __name__ == "__main__":
    main()
