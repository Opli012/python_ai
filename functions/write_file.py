from pathlib import Path
from google.genai import types


def write_file(working_directory, file_path, content):
    abs_working_dir = Path(working_directory).resolve()
    abs_file_path = Path(abs_working_dir.joinpath(file_path)).resolve()

    try:
        abs_file_path.relative_to(abs_working_dir)
    except ValueError:
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

    try:
        abs_file_path.write_text(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except OSError as e:
        print(f"Error: An error occurred while creating or writing to the file: {e}")


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write text to a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file within the working directory."
            ),
        },
        required=["path"]
    ),
)