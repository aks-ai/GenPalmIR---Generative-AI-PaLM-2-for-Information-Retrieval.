import streamlit as st


def main():
    st.set_page_config("GenPalmIR---Generative-AI-PaLM-2-for-Information-Retrieval")
    st.header("GenPalmIR---Generative-AI-PaLM-2-for-Information-Retrieval")

    with st.sidebar:
        st.title("Menu:")
        pdf_document = st.file_uploader("Upload you document files and click on the Sumbit and Process Button", accept_multiple_files=True)
        if st.button("Submit and Process"):
            with st.spinner("Processing...."):


                st.success("Done")

if __name__ == "__main__":
    main()