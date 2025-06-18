import os

def write_file(working_directory, file_path, content):
    wd_abs_path = os.path.abspath(working_directory)
    target_path = os.path.join(wd_abs_path, file_path)
   
    if os.path.abspath(target_path).startswith(wd_abs_path) == False:
        return f'Error: Cannot write to"{file_path}" as it is outside the permitted working directory'
    try:
        path_name = os.path.dirname(target_path)
        if os.path.exists(path_name) != True:
           os.makedirs(path_name)

        with open(target_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"

