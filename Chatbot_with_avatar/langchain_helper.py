# pip install streamlit langchain langchain-openai beautifulsoup4 python-dotenv chromadb

from dotenv import load_dotenv
import pickle
from pathlib import Path
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import TextLoader


load_dotenv()


class langchian_helper:

    def __init__(self) -> None:

        self.url_list = [
            "https://hush1one.com/",
            "https://hush1one.com/about/",
            "https://sites.google.com/hush1one.com/drops",
            "https://sites.google.com/hush1one.com/drops/key-demos",
            "https://docs.google.com/document/d/1J0rlJIqrm8BftlzavJe1MiJ9G_5GOTi1s02o7svQplM/edit",
            "https://sites.google.com/hush1one.com/drops/products/app",
            "https://sites.google.com/hush1one.com/drops/products/developer-api",
            "https://sites.google.com/hush1one.com/drops/products/hushh-button",
            "https://sites.google.com/hush1one.com/drops/uiux",
            "https://sites.google.com/hush1one.com/drops/mlds",
        ]
        self.chat_history = [
            AIMessage(content="Hello, I am a bot. How can I help you?"),
        ]
        self.doc_path = ".\Kranthi.txt"
        self.vector_store = None

    def get_vectorstore_from_url(self, url, doc_path):
        # get the text in document form
        loader = WebBaseLoader(url)
        document = loader.load()

        text_loader = TextLoader(doc_path, encoding="UTF-8")
        text_documents = text_loader.load()
        document.extend(text_documents)

        # split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter()
        document_chunks = text_splitter.split_documents(document)

        # create a vectorstore from the chunks
        vector_store = Chroma.from_documents(document_chunks, OpenAIEmbeddings())

        return vector_store

    def get_context_retriever_chain(self, vector_store):
        llm = ChatOpenAI()

        retriever = vector_store.as_retriever()

        prompt = ChatPromptTemplate.from_messages(
            [
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
                (
                    "user",
                    "Given the above conversation, generate a search query to\
        look up in order to get information relevant to the conversation",
                ),
            ]
        )

        retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

        return retriever_chain

    def get_conversational_rag_chain(self, retriever_chain):

        llm = ChatOpenAI()

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Answer the user's questions based on the below context:\n\n{context}",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
            ]
        )

        stuff_documents_chain = create_stuff_documents_chain(llm, prompt)

        return create_retrieval_chain(retriever_chain, stuff_documents_chain)

    def get_response(self, user_query, vector_store, chat_history):
        retriever_chain = self.get_context_retriever_chain(vector_store)
        conversation_rag_chain = self.get_conversational_rag_chain(retriever_chain)

        response = conversation_rag_chain.invoke(
            {"chat_history": chat_history, "input": user_query}
        )

        return response["answer"]

    def append_chathistory(self, chat_history, user_query, response):
        chat_history.append(HumanMessage(content=user_query))
        chat_history.append(AIMessage(content=response))

    # vector_store = get_vectorstore_from_url(url_list)

    # user input

    def return_response(self, user_query):
        if self.vector_store == None:
            vector_store = self.get_vectorstore_from_url(self.url_list, self.doc_path)

        if user_query is not None and user_query != "":
            response = self.get_response(user_query, vector_store, self.chat_history)
            self.append_chathistory(self.chat_history, user_query, response)
            return response
        else:
            return "Enter a valid user query"


def create_pickle_file():
    if not Path("data.obj").exists():
        chat = langchian_helper()
        fileObj = open("data.obj", "wb")
        pickle.dump(chat, fileObj)
        fileObj.close()
