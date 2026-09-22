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
     #create this array to store the messages in order to allow the agent to access them. Artificial memory :D 
     self.messages = []   

      #messages class
    def messages_function(self):
            #1st exchange
            self.messages.append({"role": "user", "content": "My name is george"})
            #user message
            response1 = completion(model=f"ollama/{self.ollama_model}",messages=self.messages)
            #ai message     
            assistant_message1 = response1.choices[0].message.content
            #add assistant's response to the list
            self.messages.append({"role":"system","content":assistant_message1})
            print(assistant_message1)
     
     
            #second exchange
            self.messages.append({"role": "user", "content": "What's my name?"})
            #user message
            response2 = completion(model=f"ollama/{self.ollama_model}",messages=self.messages)
            #ai message     
            assistant_message2 = response2.choices[0].message.content
            #add assistant's response to the list
            self.messages.append({"role":"system","content":assistant_message2})
            print(assistant_message2)


    #call the agent
    def chatbot(self):
     self.messages_function()

   





