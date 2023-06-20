import sys
import subprocess
import json

# Import the other scripts from the project
from src import gpt4
from src import command_executor
from src import error_handler
from src import safety
from src import context_manager

def main():
    while True:
        try:
            # Prompt the user for input
            user_input = input("Enter a command in natural language: ")

            # Add the user input to the context
            context_manager.add_to_context(user_input)

            # Send the user input and the context to GPT-4
            gpt4_response = gpt4.send_input(user_input, context_manager.get_context())

            # Parse the GPT-4 response into a terminal command
            command = command_executor.parse_response(gpt4_response)

            # Add the GPT-4 response and the command to the context
            context_manager.add_to_context(gpt4_response)
            context_manager.add_to_context(command)

            # Check if the command is safe to execute
            if not safety.is_safe(command):
                print("This command is potentially harmful. Please confirm execution.")
                confirmation = input("Are you sure you want to execute this command? (yes/no): ")
                if confirmation.lower() != "yes":
                    continue

            # Execute the terminal command
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Get the output and error (if any) from the command
            output, error = process.communicate()

            # Add the output and error (if any) to the context
            context_manager.add_to_context(output.decode())
            if process.returncode != 0:
                context_manager.add_to_context(error.decode())

            # If there was an error, handle it
            if process.returncode != 0:
                error_handler.handle_error(error)
                continue

            # Print the output of the command
            print(output.decode())

        except Exception as e:
            # If an exception was raised, handle it
            error_handler.handle_exception(e)

if __name__ == "__main__":
    main()
