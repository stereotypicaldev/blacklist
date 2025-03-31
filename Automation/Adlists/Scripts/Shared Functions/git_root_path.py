import subprocess
import os
from pathlib import Path

def identify_root():

    try:
        # Use `git rev-parse --show-toplevel` to find the root directory of the Git repository
        result = subprocess.run(['git', 'rev-parse', '--show-toplevel'],
                                capture_output=True,
                                text=True,
                                check=True)

        # Get the absolute path of the Git root
        abs_path = Path(result.stdout.strip())

        # Verify that the path exists and is a directory
        if not os.path.isdir(abs_path):
            raise RuntimeError(
                f"The path '{abs_path}' is not a directory.")

        return abs_path

    except subprocess.CalledProcessError:

        # Handle the case where `git` command fails (e.g., not in a git repository)
        print(
            "Error: Unable to determine Git root directory. Ensure you are inside a Git repository."
        )
        return None

    except FileNotFoundError:

        # Handle the case where `git` command is not found (e.g., Git not installed)
        print("Error: Git command not found. Please ensure Git is installed.")
        return None

    except Exception as e:

        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return None
