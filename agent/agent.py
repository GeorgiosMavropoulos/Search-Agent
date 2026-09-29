### file to initialize the agent
#import dotenv
from dotenv import load_dotenv, find_dotenv 
load_dotenv(find_dotenv()) ##initialize load env to find .env
from openai import OpenAI #import ollama chat
from litellm import acompletion
import os
import asyncio
import os
#import prompts
from prompts.prompts import prompts as pr

import json

##load available tools
from tools_schemas.calculator_tool_schema import CalculatorTool as calc
from mcp_implementation.mcp_client_launcher import client
#load websearch tool
from tools_schemas.websearch_tool_schema import WebSearch as w_search


#impor the class with the method generate code file
from tools_schemas.generate_code_file_tool import GenerateCodeFile as generate_code
#import the class with the method write to txt
from tools_schemas.save_to_txt_tool import WriteToTxt as write_txt
##import tools


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

     ##define a list with the tool definition to feed it to the model
     self.tool_functions = [calc.calculator, w_search.web_search,generate_code.generate_code_file,write_txt.write_to_file]

     #create the tools registry
     self.tool_registry = {fn.__name__: fn for fn in self.tool_functions}    


    #agent loop
    async def agent_loop(self,question):
     
      self.messages = [
        {"role": "system", "content": pr.system_prompt},
        {"role": "user", "content": question}
    ]

       ##start the session with the mcp client
      async with client() as response_data:

        session, tools = response_data       
           #create a loop to send back the updated information to the LLM
        while True:

            response = await acompletion(
                model=f'ollama_chat/{self.ollama_model}',
                messages=self.messages,
                tools=tools
                
            )

            #delegate into a variable LLM's message
            assistant_message = response.choices[0].message
            print(f"Tool call:{assistant_message.tool_calls}")

            for tool in tools:
               function_name = tool.name

            #if a tool was called return the final response with tools
            if self.handle_tool_calls(assistant_message,function_name):

             continue##return to the loop

            else:
             #if no tools calls store the original answer
             self.messages.append({"role": "assistant", "content": assistant_message.content})
                                    
            return assistant_message.content

    #method to handle tool calls
    def handle_tool_calls(self, ai_response,tools) -> bool: 
        #if model did not called a tool return false
        if not ai_response.tool_calls:
            return False

        for tool in ai_response.tool_calls:
           for available_tool in tools:
              if available_tool.name == tool.function.name:
                 available_tool.execute(tool)

        if ai_response.tool_calls:
           self.messages.append({
            "role": "assistant",
            "content": ai_response.content or None,
            "tool_calls": ai_response.tool_calls
        })
           for tool_call in ai_response.tool_calls:
                tool_result = self.tool_execution(self.tool_registry, tool_call)
                ##append the messages into message list
                self.messages.append({
                    "role": "tool", 
                    "content": str(tool_result), 
                    "tool_call_id": tool_call.id
                })
        
        return True
                                      

    #call the agent
    async def chatbot(self,question: str):
     
     """LLM call with rate limiting and automatic retry."""
     async with self.semaphore: #use semaphore to implement rate limiting
       
       
          #return the final response
        final_response = await self.agent_loop(question)
        
        return final_response
           


       
                          
                        
        
    

   