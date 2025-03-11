import streamlit as st
import tempfile
from evoagent.llms.llms import OpenAILLM
from evoagent.vector_stores import QdrantVectorStore
from evoagent.embeddings import OpenAIEmbeddings
from evoagent.tools.file_reader import DocumentReader
from dotenv import load_dotenv

load_dotenv()

class PDFChatbot:
    def __init__(self, title: str, llm: OpenAILLM, vector_store: QdrantVectorStore, embeddings: OpenAIEmbeddings, chat_history: bool = True, custom_instructions: str = "", verbose: bool = True):
        self.title = title
        self.llm = llm
        self.vector_store = vector_store
        self.embeddings = embeddings
        self.chat_history = chat_history
        self.custom_instructions = custom_instructions
        self.verbose = verbose
        
        if 'messages' not in st.session_state:
            st.session_state.messages = []

    def display_example_queries(self):
        with st.expander("Example Queries"):
            example_queries = {
                "example1": "Summarize the key points of this document.",
                "example2": "Who are the main entities mentioned in this document?",
                "example3": "Does this document contain financial data?",
                "example4": "What are the conclusions drawn in this document?"
            }
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Summarize the key points.", key="example1"):
                    st.session_state.example_query = example_queries["example1"]
                if st.button("Who are the main entities?", key="example2"):
                    st.session_state.example_query = example_queries["example2"]
            with col2:
                if st.button("Does it contain financial data?", key="example3"):
                    st.session_state.example_query = example_queries["example3"]
                if st.button("What are the conclusions?", key="example4"):
                    st.session_state.example_query = example_queries["example4"]

    def chat(self):
        st.title(self.title)
        
        if self.verbose:
            st.markdown("""
            Welcome to the EvoAgent PDF Chatbot! This chatbot can answer questions about a PDF file.
            Upload a PDF file and ask questions about its content!
            """)
        
        st.subheader("Example Queries")
        self.display_example_queries()
        
        uploaded_file = st.file_uploader("Choose a PDF file...", type=["pdf"])
        if uploaded_file is not None:
            reader = DocumentReader()
            with st.spinner("Reading PDF..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(uploaded_file.read())
                    temp_file_path = temp_file.name
                
                text = reader.read(temp_file_path)
                text_embedding = self.embeddings.embed(text)
                self.vector_store.add(text, text_embedding)
        
        message_container = st.container()
        
        prompt = st.chat_input("What would you like to know about the document?")
        
        if "example_query" in st.session_state:
            prompt = st.session_state.pop("example_query")
        
        with message_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        if prompt:
            if uploaded_file is None:
                st.warning("Please upload a PDF file first!")
                return
            
            with message_container:
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing document..."):
                        query_embedding = self.embeddings.embed(prompt)
                        relevant_texts = self.vector_store.query(query_embedding, k=3)
                        context = "\n".join(relevant_texts)
                        full_prompt = f"{self.custom_instructions}\nBased on the following context, {prompt}\n\nContext: {context}"
                        response = self.llm.generate(full_prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
