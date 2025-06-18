import os
import subprocess

def run_python_file(working_directory, file_path):
    wd_abs_path = os.path.abspath(working_directory)

    target_path = os.path.join(wd_abs_path, file_path)
    
    abs_target = os.path.abspath(target_path)

    if os.path.isfile(target_path) == False:
        return f'Error: File "{file_path}" not found'
    if target_path.startswith(abs_target) == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if target_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file'
    try:
        result = subprocess.run(["python", target_path], capture_output=True, timeout=30)

        if result.stdout == "":
            return "No output produced"
        
        return f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}'

    except subprocess.CalledProcessError as e:
        return f'Process exited with code {e.returncode}'

    except Exception as e:
            return f"Error: {e}"

