import os
import sys
import json
import functions.get_file_content
import functions.get_files_info
import functions.run_python_file
import functions.write_file
from dotenv import load_dotenv
from google import genai
from google.genai import types

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")
    
    funcs = {"get_files_info" : functions.get_files_info.get_files_info,
             "get_file_content" : functions.get_file_content.get_file_content,
             "run_python_file" : functions.run_python_file.run_python_file,
             "write_file" : functions.write_file.write_file}
    func_args = function_call_part.args
    func_args["working_directory"] = "./calculator"
    try:
        result = funcs[function_call_part.name](**func_args)
        return types.Content(
                role="tool",
                parts=[
                types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
                )
             ],
        )
    except SyntaxError:
        return types.Content(
                role="tool",
                parts=[
                types.Part.from_function_response(
                name=function_call_part.function_name,
                response={"error": f"Unknown function: {function_call_part.name}"}
                ),
            ],
        )

verbose = False

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

schema_get_files_info = types.FunctionDeclaration(
    name = "get_files_info",
        description = "Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
    "directory": types.Schema(
    type=types.Type.STRING,
    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
    ),
    },
    ),
)

schema_get_file_content= types.FunctionDeclaration(
    name = "get_file_content",
        description = "Reads the content of a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
    "file_path": types.Schema(
    type=types.Type.STRING,
    description="The file path of the file to read, relative to the working directory.",
    ),
    },
    ),
)

schema_run_python_file= types.FunctionDeclaration(
    name = "run_python_file",
        description = "Executes a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
    "file_path": types.Schema(
    type=types.Type.STRING,
    description="The file path of the file to execute, relative to the working directory.",
    ),
    },
    ),
)

schema_write_file= types.FunctionDeclaration(
    name = "write_file",
        description = "Writes to a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
    "file_path": types.Schema(
    type=types.Type.STRING,
    description="The file path of the file to execute, relative to the working directory.",
    ),
    "content": types.Schema(
    type=types.Type.STRING,
    description="Content to write into the specified file",
    ),
    },
    ),
)

available_functions = types.Tool(
    function_declarations=[
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
        ]
)

if len(sys.argv) < 2:
    user_prompt = ""
else:
    user_prompt = sys.argv[1]

if len(sys.argv) == 3:
    if sys.argv[2] == "--verbose":
        verbose = True


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key= api_key)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

count = 0

while count < 20:
    count += 1
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],system_instruction=system_prompt),
    )

    if response.candidates != None:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if verbose == True:
        print(f"User prompt: {user_prompt}")

    if response.function_calls != None:
        function_calls= response.function_calls

        for call in function_calls:
            result = call_function(call, verbose)
            messages.append(result)
    else:
        count = 20
        print(f"Final response:\n{response.candidates[0].content.parts[0].text}")

    if verbose == True: 
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


