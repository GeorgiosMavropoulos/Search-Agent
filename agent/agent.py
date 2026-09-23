### file to initialize the agent
#import dotenv
from dotenv import load_dotenv, find_dotenv 
load_dotenv(find_dotenv()) ##initialize load env to find .env
from openai import OpenAI #import ollama chat
from litellm import acompletion
import os
import asyncio
#import models
from models.model import ExtractedInfo
##agent class
class Agent:
    def __init__(self):
     ##load the model and api url           
     self.ollama_model = os.getenv("ollama_model")
     self.ollama_url = os.getenv("ollama_url")
     #create this array to store the messages in order to allow the agent to access them. Artificial memory :D 
     self.messages = [] 
       #prompts
     self.prompts = [
         f"What is {i} + {i}?" for i in range(100)
     ] 

     #limit the agent to execute 10 concurrent requests only
     self.semaphore = asyncio.Semaphore(10)
     


    
      #messages class
    async def messages_function(self,prompt: str) -> str:
            """LLM call with rate limiting and automatic retry."""
            async with self.semaphore:
                #1st exchange
                messages = [
            {"role": "user", "content": prompt}
        ]

            response1 = await acompletion(
                model=f"ollama/{self.ollama_model}",
                messages=messages,
                num_retries=3,
                api_base=self.ollama_url
            )
                #ai message     
            return  response1.choices[0].message.content
                #add assistant's response to the list
                #self.messages.append({"role":"system","content":assistant_message1})
                #print(assistant_message1)

    

     
            """
            #second exchange
            self.messages.append({"role": "user", "content": "What's my name?"})
            #user message
            response2 = completion(model=f"ollama/{self.ollama_model}",messages=self.messages)
            #ai message     
            assistant_message2 = response2.choices[0].message.content
            #add assistant's response to the list
            self.messages.append({"role":"system","content":assistant_message2})
            print(assistant_message2)
"""

    #call the agent
    async def chatbot(self):
     # Execute all requests concurrently
     # Even with 100 concurrent tasks, only 10 API calls run at a time
     tasks = [self.messages_function(p) for p in self.prompts]
     results = await asyncio.gather(*tasks,return_exceptions=True) #execute all tasks and return exceptions
     #print the given prompts
     for prompt, result in zip(self.prompts, results):
         print(f"Prompt:{prompt}")
         print(f"Result:{result}")
         print(type(result))

   





