### file to initialize the agent
#import dotenv
from dotenv import load_dotenv, find_dotenv 
load_dotenv(find_dotenv()) ##initialize load env to find .env
from openai import OpenAI #import ollama chat
from litellm import acompletion
import os
import asyncio
#import models
from tavily import TavilyClient#import tavily to implemenet web search

import os
#import prompts
from prompts.prompts import prompts as pr
import json

##load available tools
from tools_schemas.tools_schemas import CalculatorTool as calc

##import tools


##agent class
class Agent:
    def __init__(self):
     ##load the model and api url           
     self.ollama_model = os.getenv("ollama_model")
     self.ollama_url = os.getenv("ollama_url")
     #create this array to store the messages in order to allow the agent to access them. Artificial memory :D 
     self.messages = [{"role": "system",
            "content": pr.system_prompt},
        {         
         "role":"user","content":"Who is Alexis Tsipras?"
       }] 
    
     #limit the agent to execute 10 concurrent requests only
     self.semaphore = asyncio.Semaphore(10)

     #initialize tavily client
     self.tavily_client = TavilyClient(os.getenv("TAVILY_API_KEY"))


     
   
     ##define a list with the tool definition to feed it to the model
     self.tools = [calc.calculator_definition]


    #method to handle tool calls
    def handle_tool_calls(self, ai_response) -> bool: 
        #if model did not called a tool return false
        if not ai_response.tool_calls:
            return False


        #if not Store assistant's tool call
        self.messages.append({
         "role": "assistant",
         "content": ai_response.content  or None,
          "tool_calls": ai_response.tool_calls
         })

         #execut the called tools
        for tool_call in ai_response.tool_calls:
         tool_name = tool_call.function.name ##extract tool's name
                   
         function_params = json.loads( tool_call.function.arguments ) ##extract function's paremeters
         ##if tool name is calculator perform the calculation
         if tool_name == "calculator":
           result = calc.calculator(**function_params)
         else:
           return ValueError(f"There is no such a tool with name:{tool_name}")

          #store the final result in the message
         self.messages.append({
                  "role": "tool",
                  "tool_call_id": tool_call.id,
                  "content": str(result)
              })

        return True
                                      
                                       
                   

    #call the agent
    async def chatbot(self):
     
     """LLM call with rate limiting and automatic retry."""
     async with self.semaphore: #use semaphore to implement rate limiting
       
       response = await acompletion(model=f'ollama_chat/{self.ollama_model}', messages=self.messages,tools=self.tools)
       ai_response = response.choices[0].message
      
       
       #extract the executed tool from the response
       ai_response = response.choices[0].message

       #test websearch
       def search_web(query: str, max_results: int = 2) -> list:

        response = self.tavily_client.search(query, max_results=max_results)
        print(response)
        return response.get("results")

       #search web
       search_web("Kipchoge's marathon world record")

       #define if a tool has been called
       if self.handle_tool_calls(ai_response):  
         
          #return the final response
        final_response = await acompletion(model=f'ollama_chat/{self.ollama_model}', messages=self.messages)
       

       

       
        answer = final_response.choices[0].message.content# store the answer
        #append the answer in message history
        self.messages.append({"role": "assistant", "content": answer})
        #print(f"Final answer: {answer}")
        #print(f"Tool used:{answer.message.tool_calls}")
        return answer

       else:
           #if no tools calls store the original answer
           self.messages.append({"role": "assistant", "content": ai_response.content})
           #print(f"Final answer: {ai_response.content}")
           
           return ai_response.content
           


       
                          
                        
        
    

   





