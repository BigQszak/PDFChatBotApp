import streamlit as st
from langchain_openai import ChatOpenAI  # type: ignore
from langchain.memory.buffer import ConversationBufferMemory  # type: ignore
from langchain.chains import ConversationalRetrievalChain  # type: ignore  # type: ignore

from typing import Optional


class ConversationManager:
    """ConversationManager class for managing the conversational chain and user input.

    Methods:
        get_conversation_chain(self, vectorstore)
        handle_user_input(self, question: str)
    """

    def __init__(self) -> None:
        """Initializes a new instance of the class with the `conversation_chain`
        attribute set to `None`.

        Parameters:
            None
        Returns:
            None
        """
        self.conversation_chain: Optional[ConversationalRetrievalChain] = None

    def get_conversation_chain(self, vectorstore) -> ConversationalRetrievalChain:
        """Generates a conversational hstory chain using the given vectorstore.

        Args:
            vectorstore (VectorStore): The vectorstore containing the embeddings for the text chunks.
        Returns:
            ConversationalRetrievalChain: The generated conversational retrieval chain.
        """
        llm = ChatOpenAI()
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm, retriever=vectorstore.as_retriever(), memory=memory
        )
        return self.conversation_chain

    def handle_user_input(self, question: str) -> dict:
        """Handles user input and updates the session state with the chat history.

        Args:
            question (str): The user's question.
        Returns:
            dict: A dictionary containing the chat history and the response generated by the conversation chain.
        """
        try:
            if st.session_state.conversation is None:
                raise TypeError(
                    "No previous conversation found. Please provide a PDF document."
                )
            response = st.session_state.conversation({"question": question})
            if response is None:
                raise TypeError(
                    "Conversation returned no response. Please provide a PDF document."
                )
            if "chat_history" not in response:
                raise KeyError("The response does not contain 'chat_history'.")

            st.session_state.chat_history = response["chat_history"]
            return response

        except (TypeError, KeyError) as e:
            return {"error": str(e)}
