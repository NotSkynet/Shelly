import os
import openai
import json

# Get the OpenAI API key from the environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

if openai.api_key is None:
    raise ValueError("Missing OpenAI API key. Please set the 'OPENAI_API_KEY' environment variable.")

# Define the available function for GPT-4
functions = [
    {
        "name": "terminal_command_executor",
        "description": "Runs all the instructions specified by the user in one single terminal command",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The terminal command to execute."},
            },
            "required": ["command"],
        },
    }
]

def send_input(user_input, context):
    # Add the user input to the messages
    messages = context + [{"role": "user", "content": user_input}]

    # Send the messages to GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=messages,
        function_call="auto",
        functions=functions
    )

    # Get the response message from GPT-4
    response_message = response["choices"][0]["message"]

    # If the response message contains a function call, get the function name and arguments
    if response_message.get("function_call"):
        function_name = response_message["function_call"]["name"]
        function_args = json.loads(response_message["function_call"]["arguments"])

        # If the function name is "terminal_command_executor", return the command
        if function_name == "terminal_command_executor":
            return function_args.get("command")

    # If the response message does not contain a function call, return the content of the message
    return response_message["content"]
