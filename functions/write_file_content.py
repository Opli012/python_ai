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
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)