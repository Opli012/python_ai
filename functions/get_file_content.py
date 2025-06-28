from pathlib import Path
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    abs_working_dir = Path(working_directory).resolve()
    abs_file_path = Path(abs_working_dir.joinpath(file_path)).resolve()

    try:
        abs_file_path.relative_to(abs_working_dir)
    except ValueError:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory "{working_directory}".'

    if not abs_file_path.exists():
        return f'Error: {file_path} does not exist.'
    
    if not abs_file_path.is_file():
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) >= 10000:
            file_content_string = (
                file_content_string[:10000] +
                f'\n\n[...File "{file_path}" truncated at 10000 characters]'
            )
        return file_content_string
    except Exception as e:
        return f'Error: Could not read {file_path}: {e}'