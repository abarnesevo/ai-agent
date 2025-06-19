import os

def get_files_info(working_directory, directory=None):
    wd_abs_path = os.path.abspath(working_directory)

    if directory == None:
        target_path= wd_abs_path
    else:
        target_path = os.path.join(working_directory, directory)
    if os.path.isdir(os.path.abspath(target_path)) == False:
        return f'Error: "{directory}" is not a directory'
    if os.path.abspath(target_path).startswith(wd_abs_path) == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    abs_target_path = os.path.abspath(target_path)
    try:
        dir_contents = []
        for content in os.listdir(abs_target_path):
            dir_contents.append(
        f"- {content}: file_size={os.path.getsize(os.path.join(abs_target_path,content))}, is_dir={os.path.isdir(os.path.join(abs_target_path,content))}"
        )
        
        return f"{directory}\n" + "\n".join(dir_contents)


    except Exception as e:
            return f"Error: {e}"
                                        
