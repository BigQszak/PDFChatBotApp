from langchain_openai import OpenAIEmbeddings  # type: ignore
from langchain_community.vectorstores import FAISS  # type: ignore

from typing import List, Optional, Any


class VectorStoreManager:
    """VectorStoreManager class for managing the creation and
    retrieval of a vector store.

    Methods:
        get_vectorstore(self, text_chunks: List[str])
    """

    def __init__(self) -> None:
        """Initializes a new instance of the class with the `vectorstore` attribute set to `None`.

        Args:
            None
        Returns:
            None
        """
        self.vectorstore: Optional[Any] = None

    def get_vectorstore(self, text_chunks: List[str]) -> Any:
        """Creates a vector store from text chunks.

        Args:
            text_chunks (List[str]): A list of text chunks to be stored in the
            vector store as embeddings.

        Returns:
            Any: The created vector store.
        """
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )  # "text-embedding-ada-002"
        self.vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return self.vectorstore
