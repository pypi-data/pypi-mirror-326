import streamlit as st
from evoagent.llms.llms import OpenAILLM
from dotenv import load_dotenv

load_dotenv()

class Chatbot:
    def __init__(self, llm: OpenAILLM, title: str, chat_history: bool = True, custom_instructions: str = "", verbose: bool = True):
        self.llm = llm
        self.title = title
        self.chat_history = chat_history
        self.custom_instructions = custom_instructions
        self.verbose = verbose
        
        if 'messages' not in st.session_state:
            st.session_state.messages = []

    def display_example_queries(self):
        st.subheader("Example Queries")
        example_queries = {
            "example1": "Explain the concept of Agentic AI.",
            "example2": "How does a transformer model work?",
            "example3": "What are the advantages of RAG over fine-tuning?",
            "example4": "How to deploy a LangChain application?"
        }
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Explain the concept of Agentic AI", key="example1"):
                st.session_state.example_query = example_queries["example1"]
            if st.button("How does a transformer model work?", key="example2"):
                st.session_state.example_query = example_queries["example2"]
        with col2:
            if st.button("What are the advantages of RAG over fine-tuning?", key="example3"):
                st.session_state.example_query = example_queries["example3"]
            if st.button("How to deploy a LangChain application?", key="example4"):
                st.session_state.example_query = example_queries["example4"]

    def chat(self):
        st.title(self.title)
        
        self.display_example_queries()
        
        message_container = st.container()
        with message_container:
            for message in st.session_state.messages:
                role = message["role"]
                content = message["content"]
                with st.chat_message(role):
                    st.markdown(content)
        
        prompt = st.chat_input("What would you like to know?")
        
        if "example_query" in st.session_state:
            prompt = st.session_state.pop("example_query")
        
        if prompt:
            with st.chat_message("user"):
                st.markdown(prompt)
                if self.chat_history:
                    st.session_state.messages.append({"role": "user", "content": prompt})

            response_container = st.chat_message("assistant")
            with response_container:
                placeholder = st.empty()
                with placeholder:
                    with st.spinner("Thinking..."):
                        if self.chat_history:
                            conversation_history = f"{self.custom_instructions}\n"
                            for message in st.session_state.messages:
                                conversation_history += f"{message['role']}: {message['content']}\n"
                            full_prompt = f"Previous conversation history:\n{conversation_history}\nNew query: {prompt}"
                            response = self.llm.generate(full_prompt)
                        else:
                            response = self.llm.generate(prompt)
                    st.markdown(response)
                    if self.chat_history:
                        st.session_state.messages.append({"role": "assistant", "content": response})
