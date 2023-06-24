import json
import subprocess
from src import gpt4

def parse_response(gpt4_response):
    """Parses a GPT-4 response into a terminal command."""
    # Load the JSON response from GPT-4
    response = json.loads(gpt4_response)

    # Get the command from the response
    command = response.get("command")

    # Return the command
    return command

def execute_command(command):
    """Executes a terminal command and returns the output."""
    # Execute the command using subprocess
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # If there was an error, return it
    if process.returncode != 0:
        return error.decode()

    # Otherwise return the output
    return output.decode()

def get_next_command(gpt4_response, previous_output):
    """Sends the previous command output to GPT-4 and gets the next command."""
    # Add the previous output to the context for GPT-4
    context = [{"role": "output", "content": previous_output}]

    # Send the context and get a response from GPT-4
    response = gpt4.send_input(context=context)

    # Parse the response into a command
    command = parse_response(response)

    # Return the command
    return command

def execute_commands(user_input):
    """Executes multiple commands in a row based on user input."""
    # Get the first command from GPT-4 based on the user input
    first_command = gpt4.send_input(user_input)
    command = parse_response(first_command)

    # While the command is not "end_of_command", execute it and get the next command
    while command != "end_of_command":
        # Execute the command and get the output
        output = execute_command(command)

        # Send the output to GPT-4 and get the next command
        command = get_next_command(output)

    # Return the final output
    return output