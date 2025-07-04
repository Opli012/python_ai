from pathlib import Path
from google.genai import types


def get_files_info(working_directory, directory=None):
    abs_working_dir = Path(working_directory).resolve()
    target_dir = abs_working_dir
    if directory:
        target_dir = Path(abs_working_dir.joinpath(directory)).resolve()

    try:
        target_dir.relative_to(abs_working_dir)
    except ValueError:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not target_dir.exists():
        return f"{directory} does not exist."

    if not target_dir.is_dir():
        return f"{directory} is not a directory."

    lines = []
    for item in sorted(target_dir.iterdir(), key=lambda p: p.name.lower()):
        try:
            size = item.stat().st_size
        except OSError:
            size = 0
        lines.append(f"- {item.name}: file_size={size} bytes, is_dir={item.is_dir()}")
    return "\n".join(lines)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
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