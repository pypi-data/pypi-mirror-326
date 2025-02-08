# ⚔️🔗 EvoAgent

⚡ An orchestration framework for all your AI needs ⚡

```
    ███████╗██╗   ██╗ ██████╗      █████╗  ██████╗ ███████╗███╗   ██╗████████╗
    ██╔════╝██║   ██║██╔═══██╗    ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝
    █████╗  ██║   ██║██║   ██║    ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   
    ██╔══╝  ╚██╗ ██╔╝██║   ██║    ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   
    ███████╗ ╚████╔╝ ╚██████╔╝    ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   
    ╚══════╝  ╚═══╝   ╚═════╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   
    =====================================================================
         🤖 Welcome to EVO AGENT! Your Evolution in AI Begins Here 🤖
    =====================================================================
```

## Features

- 🤖 Multiple LLM Support (OpenAI, Anthropic, Groq)
- 📚 Vector Store Integration (FAISS, Qdrant, ChromaDB)
- 🔍 Advanced Document Processing
- 🎙️ Speech-to-Text Capabilities
- 🌐 Web Crawling
- 📊 Data Visualization
- 🎯 RAG Applications
- 🤝 PhiData Agent Integration
- 💬 Interactive Chatbots
- 🤖 Self-Evolving Autonomous Agents

## Installation

```bash
pip install evoagent
```

## Usage

### EvoAgent Framework

```python
from evoagent.agent import Agent

def example_function(input_text: str) -> str:
    return f"Processed: {input_text}"

agent = Agent()
agent.register_function(example_function)

query = "Analyze market trends in AI"
response = agent.process_query(query)
print(response)
```

### RAG Implementation

```python
from evoagent.vector_store import FAISSVectorStore
from evoagent.embeddings import HuggingFaceEmbeddings
from evoagent.llms import GroqLLM

vector_store = FAISSVectorStore()
embeddings = HuggingFaceEmbeddings()
llm = GroqLLM("llama3-8b-8192")

text = "AI is transforming industries with automation."
vector_store.add(text, embeddings.embed(text))

query = "How is AI impacting industries?"
response = llm.generate(query)
print(response)
```

### Chatbot Integration

```python
from evoagent.chatbot import Chatbot

chatbot = Chatbot(title="EvoAgent Chatbot")
chatbot.chat()
```

## Contributing

```bash
git clone https://github.com/yourusername/evoagent.git
cd evoagent
pip install -e .
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

