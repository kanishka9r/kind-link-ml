import os
import json
from groq import Groq
from action import *
from prompt import *
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#Takes the user's chat, decides if a tool is needed, and returns the AI reply.
    
def get_ai_response(user_message: str, user_id: str, user_name: str):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    # Send the chat to Llama 3 passing along our tools 
    response = groq_client.chat.completions.create(
         model="llama-3.1-8b-instant",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=1000
    )
    
    response_message = response.choices[0].message
    
    # Llama 3 decide it needs to use a tool
    if response_message.tool_calls:
        messages.append(response_message) # Save its thought process
        
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments) # The data Llama extracted from the chat
            
            # Execute the correct Python muscle
            if function_name == "search_ngos":
                result = search_ngos(args.get("location"), args.get("category"))
            elif function_name == "save_to_favorites":
                result = save_to_favorites(user_id, user_name, args.get("ngo_id"), args.get("ngo_name"))
            elif function_name == "book_visit":
                result = book_visit(user_id, user_name, args.get("ngo_id"), args.get("ngo_name"), args.get("date"))
            elif function_name == "log_donation_pledge":
                result = log_donation_pledge(user_id, user_name, args.get("ngo_id"), args.get("ngo_name"), args.get("items"))
            elif function_name == "request_callback":
                result = request_callback(user_id, user_name, args.get("ngo_id"), args.get("ngo_name"), args.get("phone_number"))
                
            # Tell Llama 3 the result of the MongoDB action
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": result
            })
            
        # Ask Llama 3 to write a final empathetic text reply to the user now that the action is done
        final_response = groq_client.chat.completions.create(
             model="llama-3.1-8b-instant",
            messages=messages
        )
        ai_reply = final_response.choices[0].message.content or ""
        return ai_reply.split("<function")[0].strip()
        
    else:
        # If no tool was needed, just return its normal text reply
        ai_reply = response_message.content or ""
        return ai_reply.split("<function")[0].strip()