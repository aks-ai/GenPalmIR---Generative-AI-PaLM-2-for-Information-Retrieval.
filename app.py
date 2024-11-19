import streamlit as st
from src.helper import get_pdf_text, get_chunks, get_vector_store, get_conversational_chain #importing the methods from helper file
import os 
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
print("Loaded Google API Key:", GOOGLE_API_KEY)  # Debugging line to print the key

def user_input(user_query):
    """
    Handles user input, retrieves responses from a conversational AI model, 
    and displays the conversation history in a Streamlit app.

    Args:
        user_question (str): The question or input from the user.
    """
    # Send the user's question to the conversational model and get a response
    response = st.session_state.conversation({'question': user_query})
    
    # Update the conversation history in session state
    st.session_state.chatHistory = response['chat_history']
    
    # Loop through the chat history and display the conversation
    for i, message in enumerate(st.session_state.chatHistory):
        if i % 2 == 0:  # Even indices correspond to user messages
            st.write("User: ", message.content)
        else:  # Odd indices correspond to AI replies
            st.write("Reply: ", message.content)

def main():
    st.set_page_config("GenPalmIR---Generative-AI-PaLM-2-for-Information-Retrieval")
    st.header("GenPalmIR---Generative-AI-PaLM-2-for-Information-Retrieval")

    user_query = st.text_input("Ask question from the PDF files")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = None
    if user_query:
        user_input(user_query)

    with st.sidebar:
        st.title("Menu:")
        pdf_document = st.file_uploader("Upload you document files and click on the Sumbit and Process Button", accept_multiple_files=True)
        if st.button("Submit and Process"):
            with st.spinner("Processing...."):
                raw_text = get_pdf_text(pdf_document)
                text_chunks = get_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)
                st.session_state.coversation = get_conversational_chain(vector_store)

                st.success("Done")

if __name__ == "__main__":
    main()