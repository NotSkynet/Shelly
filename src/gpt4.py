import os
import openai
import json

# Your OpenAI API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# The GPT-4 model to use
MODEL = "gpt-4-0613"

# Set the OpenAI API key 
openai.api_key = OPENAI_API_KEY

def send_input(input_text):
    """Sends input text to GPT-4 and returns the response"""

    currpath = os.path.expanduser('~')

    available_functions = {
        "terminal_command_executor": terminal_command_executor,
    }

    functions = [
        {
            "name": "terminal_command_executor",
            "description": "Runs all the instructions specified by the user in one single MacOS terminal command, use this whenever the user asks for file creation or manipulation as well",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The terminal command to execute, e.g. If the user wants to list all files in the current folder, ls."},
                },
                "required": ["command"],
            },
        },
    ]
    # Create the GPT-4 response
    response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=messages,
            function_call="auto",
            functions=functions
        )

    # Parse the GPT-4 response into a JSON object
    response_json = json.loads(response["choices"][0]["text"])

    # Return the JSON response
    return response_json

def send_output(output_text):
    """Sends command output text to GPT-4 and returns the next command"""

    # Create the GPT-4 response
    response = openai.ChatCompletion.create(
        model=MODEL,
        prompt=output_text,
        temperature=0.7,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.5
    )

    # Parse the GPT-4 response into a JSON object
    response_json = json.loads(response["choices"][0]["text"])

    # Return the JSON response
    return response_json