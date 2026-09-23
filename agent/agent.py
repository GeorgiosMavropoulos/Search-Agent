### file to initialize the agent
#import dotenv
from dotenv import load_dotenv, find_dotenv 
load_dotenv(find_dotenv()) ##initialize load env to find .env
from openai import OpenAI #import ollama chat
from litellm import acompletion
import os
import asyncio
#import models
from models.model import GaiaOutput
##download GAIA for evaluation
from datasets import load_dataset
import os
#import prompts
from prompts.prompts import prompts as pr


##load level1 gaia problems
level1_problems = load_dataset("gaia-benchmark/GAIA", "2023_level1", split="validation")



##agent class
class Agent:
    def __init__(self):
     ##load the model and api url           
     self.ollama_model = os.getenv("ollama_model")
     self.ollama_url = os.getenv("ollama_url")
     #create this array to store the messages in order to allow the agent to access them. Artificial memory :D 
     self.messages = [] 
    
     #limit the agent to execute 10 concurrent requests only
     self.semaphore = asyncio.Semaphore(10)
     
   

     self.question = level1_problems[0]["Question"]
     self.answer = level1_problems[0]["Final answer"]

    
    
    
      #messages class
    async def messages_function(self) -> str:
            """LLM call with rate limiting and automatic retry."""
            async with self.semaphore:
                #1st exchange
                messages = [
            {"role": "user", "content": pr.GAIAs_evaluation_prompt},
             {"role": "user", "content": self.question},
        ]

                response = await acompletion(
                model=f"ollama/{self.ollama_model}",
                messages=messages,
                num_retries=3,
                api_base=self.ollama_url,
                response_format=GaiaOutput #use GAIAOutput response's format
            )
                #ai message     
            finish_reason = response.choices[0].finish_reason #this is the extracted finish reason
            content = response.choices[0].message.content###this is the message's content from the llm.

            #return the appropriate output if finish_reason is refusal
            if finish_reason == "refusal" or content is None:
                return GaiaOutput(
                    is_solvable= False,
                    unsolvable_reason=f"Model refused to answer (finish_reason: {finish_reason})",
                    final_answer= ""


                )

            return GaiaOutput.model_validate_json(content) ##validate that content is in its appropriate form

    

     
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
     # execute the messages function
     prediction = await self.messages_function()

     
     print(prediction)

   





