from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import GooglePalmEmbeddings
from langchain.llms import GooglePalm
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
print(GOOGLE_API_KEY)
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:  #for reading multiple pdfs
        pdf_reader = PdfReader(pdf) 
        for page in pdf_reader.pages: #every single page of the pdf
            text += page.extract_text()
    return text 

def get_chunks(text): #Splitting the data into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap =20) #1000 characters in the chunk and overlap of 20 characters for continuity
    chunks = text_splitter.split_text(text)
    return chunks 

#def get_vector_store(text_chunks): 
    # Converts the text chunks into vector representations using embeddings
#    embeddings = GooglePalmEmbeddings()  # Using Google PaLM embeddings for vectorization
#    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)  # Storing the vectorized text in a FAISS vector database
#   return vector_store 

def get_vector_store(text_chunks):
    api_key = os.getenv("GOOGLE_API_KEY")  # Fetch the API key from the environment variable

    if not api_key:
        raise ValueError("Google API Key is missing! Please check your .env file or environment variables.")
    
    # Pass the api_key to GooglePalmEmbeddings
    embeddings = GooglePalmEmbeddings(google_api_key=api_key)  # Pass api_key explicitly
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store


def get_conversational_chain(vector_store):
    llm= GooglePalm() #Initiating the LLM
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True) #Creates a memory object to keep track of the conversation's history
    #memory_key="chat_history": Stores past interactions under this key.
    #return_messages=True: Ensures the stored history is accessible as messages for the LLM to use in context.
    converstion_chain = ConversationalRetrievalChain.from_llm(LLm= llm, retriever = vector_store.as_retriever(), memory= memory) #Combines the LLM, memory, and vector store to form the conversational retrieval chain
    #LLM: llm is used to generate responses.
    #Retriever: vector_store.as_retriever() allows the system to fetch relevant chunks of information from the vector store based on the current query.
    #Memory: memory provides the LLM with historical context to enable meaningful, coherent conversations over multiple turns.
    return converstion_chain 
