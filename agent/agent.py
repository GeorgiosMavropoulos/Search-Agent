### file to initialize the agent
#import dotenv
from dotenv import load_dotenv, find_dotenv 
load_dotenv(find_dotenv()) ##initialize load env to find .env
from openai import OpenAI #import ollama chat
from litellm import completion
import os
##agent class
class Agent:
    def __init__(self):
     ##load the model and api url           
     self.ollama_model = os.getenv("ollama_model")
     self.ollama_url = os.getenv("ollama_url")
        


    #call the agent
    def chatbot(self):
        self.response = completion(
    model=f"ollama/{self.ollama_model}",
    messages=[
        {"role": "user", "content": "Hello"}
    ],
    api_base=self.ollama_url
)

        print(self.response.choices[0].message.content) #return the last response





