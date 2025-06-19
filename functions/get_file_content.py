import os

def get_file_content(working_directory, file_path):
    wd_abs_path = os.path.abspath(working_directory)

    target_path = os.path.join(wd_abs_path, file_path)
    
    if os.path.isfile(target_path) == False:
        return f'Error: file not found or is not a regular file: "{file_path}"'
    print(wd_abs_path)
    print(target_path)
    if target_path.startswith(wd_abs_path) == False:
        return f'Error: Cannot read"{file_path}" as it is outside the permitted working directory'

    try:
        MAX_CHARS = 10000
        
        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        
        return {"result" : file_content_string}

    except Exception as e:
        return f"Error: {e}"
