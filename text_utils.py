from PyPDF2 import PdfReader  # type: ignore
from langchain.text_splitter import CharacterTextSplitter  # type: ignore

from typing import List, Any


class PDFHandler:
    """PDFHandler class for extracting raw text from provided PDF documents.

    Methods:
        get_pdf_text(self, pdf_docs)
    """

    def __init__(self) -> None:
        """Initializes a new instance of the class
        and sets the `raw_text` attribute with an empty string.

        Parameters:
            None
        Returns:
            None
        """
        self.raw_text: str = ""

    def get_pdf_text(self, pdf_docs: List[Any]) -> str:
        """Extracts raw text from a list of provided PDF documents.

        Args:
            pdf_docs (List[Any]): A list of PDF documents to be processed.

        Returns:
            str: The raw text extracted from the provided PDF documents.

        """
        if not pdf_docs:
            raise ValueError(
                "No PDF documents provided. Please submit documents from your computer."
            )
        raw_text_chunks = []
        for pdf_document in pdf_docs:
            pdf_reader = PdfReader(pdf_document)
            raw_text_chunks.extend(page.extract_text() for page in pdf_reader.pages)
        self.raw_text = "".join(raw_text_chunks)
        return self.raw_text


class TextSplitter:
    """TextSplitter class for splitting raw text into smaller chunks for further processing.

    Methods:
        get_text_chunks(self, raw_text: str)
    """

    def __init__(self, chunk_size: int = 1500, chunk_overlap: int = 200) -> None:
        """
        Initializes a new instance of the TextSplitter class with the specified chunk size and overlap.

        Args:
            chunk_size (int, optional): The size of each text chunk. Defaults to 1000.
            chunk_overlap (int, optional): The overlap between adjacent text chunks. Defaults to 200.

        Returns:
            None
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_chunks: List[str] = []

    def get_text_chunks(self, raw_text: str) -> List[str]:
        """Splits raw text into chunks based on the specified size and overlap

        Args:
            raw_text (str): The raw text to be split into chunks.

        Returns:
            List[str]: A list of text chunks.

        """
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
        self.text_chunks = text_splitter.split_text(raw_text)
        return text_splitter.split_text(raw_text)
