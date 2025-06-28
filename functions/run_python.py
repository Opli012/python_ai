from pathlib import Path
import subprocess
import sys


def run_python_file(working_directory, file_path):
    abs_working_dir = Path(working_directory).resolve()
    abs_file_path = Path(abs_working_dir.joinpath(file_path)).resolve()

    try:
        abs_file_path.relative_to(abs_working_dir)
    except ValueError:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not abs_file_path.exists():
        return f'Error: File "{file_path}" not found.'

    if not abs_file_path.suffix == ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            [sys.executable, abs_file_path],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
            cwd=abs_working_dir
        )

        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        
        return "\n".join(output) if output else "No output produced."
    
    except subprocess.CalledProcessError as e:
        return f"Error: executing Python file: {e}"