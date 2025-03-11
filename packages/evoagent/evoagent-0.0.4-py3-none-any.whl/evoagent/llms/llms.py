from openai import OpenAI
from anthropic import Anthropic
from groq import Groq
from huggingface_hub import InferenceClient
from typing import Union, Iterator
import os
from dotenv import load_dotenv

load_dotenv()

class LLM:
    def __init__(self, model: str, custom_instructions: str = ""):
        self.model = model
        self.custom_instructions = custom_instructions
        
    def generate(self, prompt: str, stream: bool = False) -> Union[str, Iterator[str]]:
        pass

class OpenAILLM(LLM):
    def __init__(self, model: str = "gpt-4o-mini", custom_instructions: str = ""):
        super().__init__(model, custom_instructions)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def generate(self, prompt: str, stream: bool = False) -> Union[str, Iterator[str]]:
        response = self.client.chat.completions.create(
            model=self.model, 
            messages=[
                {"role": "system", "content": self.custom_instructions}, 
                {"role": "user", "content": prompt}
            ],
            stream=stream
        )
        if stream:
            return (chunk.choices[0].delta.content for chunk in response if chunk.choices[0].delta.content is not None)
        return response.choices[0].message.content

class AnthropicLLM(LLM):
    def __init__(self, model: str = "claude-3-5-sonnet-20240620", custom_instructions: str = ""):
        super().__init__(model, custom_instructions)
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    def generate(self, prompt: str, stream: bool = False) -> Union[str, Iterator[str]]:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[
                {"role": "system", "content": self.custom_instructions}, 
                {"role": "user", "content": prompt}
            ],
            stream=stream
        )
        if stream:
            return (chunk.delta.text for chunk in response if chunk.delta.text is not None)
        return response.content[0].text

class GroqLLM(LLM):
    def __init__(self, model: str = "llama3-8b-8192", custom_instructions: str = ""):
        super().__init__(model, custom_instructions)
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
    def generate(self, prompt: str, stream: bool = False) -> Union[str, Iterator[str]]:
        response = self.client.chat.completions.create(
            model=self.model, 
            messages=[
                {"role": "system", "content": self.custom_instructions}, 
                {"role": "user", "content": prompt}
            ],
            stream=stream
        )
        if stream:
            return (chunk.choices[0].delta.content for chunk in response if chunk.choices[0].delta.content is not None)
        return response.choices[0].message.content

class GeminiLLM(LLM):
    def __init__(self, model: str = "gemini-1.5-flash", custom_instructions: str = ""):
        super().__init__(model, custom_instructions)
        self.client = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        
    def generate(self, prompt: str, stream: bool = False) -> Union[str, Iterator[str]]:
        response = self.client.chat.completions.create(
            model=self.model,
            n=1,
            messages=[
                {"role": "system", "content": self.custom_instructions},
                {"role": "user", "content": prompt}
            ],
            stream=stream
        )
        if stream:
            return (chunk.choices[0].delta.content for chunk in response if chunk.choices[0].delta.content is not None)
        return response.choices[0].message.content

class SambanovaLLM(LLM):
    def __init__(self, model: str = "DeepSeek-R1-Distill-Llama-70B", custom_instructions: str = ""):
        super().__init__(model, custom_instructions)
        self.client = OpenAI(
            api_key=os.getenv("SAMBANOVA_API_KEY"),
            base_url="https://api.sambanova.ai/v1"
        )
        
    def generate(self, prompt: str, stream: bool = False) -> Union[str, Iterator[str]]:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.custom_instructions},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            top_p=0.1,
            stream=stream
        )
        if stream:
            return (chunk.choices[0].delta.content for chunk in response if chunk.choices[0].delta.content is not None)
        return response.choices[0].message.content

class HuggingFaceLLM(LLM):
    def __init__(self, model: str = "microsoft/Phi-3.5-mini-instruct", custom_instructions: str = ""):
        super().__init__(model, custom_instructions)
        self.client = InferenceClient(api_key=os.getenv("HUGGINGFACE_API_KEY"))
        
    def generate(self, prompt: str, stream: bool = False) -> Union[str, Iterator[str]]:
        messages = [
            {"role": "system", "content": self.custom_instructions},
            {"role": "user", "content": prompt}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.5,
            max_tokens=2048,
            top_p=0.7,
            stream=stream
        )
        
        if stream:
            return (chunk.choices[0].delta.content for chunk in response if chunk.choices[0].delta.content is not None)
        return response.choices[0].message.content