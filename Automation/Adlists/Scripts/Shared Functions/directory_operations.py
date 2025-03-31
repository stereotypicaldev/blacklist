from pathlib import Path
from git_root_path import identify_root
from misc import validate_file_extension
from typing import List

def validate_directory(directory_path: Path) -> bool:
    """
    Validate if `directory_path` meets all specified conditions relative to `git_root`.
    
    Args:
    - git_root (Path): The root directory of a git repository.
    - directory_path (Path): The directory to validate.
    
    Returns:
    - bool: True if the directory_path is valid according to the criteria, False otherwise.
    """

    groot = identify_root()

    try:

        # Validate the type and methods of directory argument
        if not (hasattr(directory_path, 'exists') and hasattr(directory_path, 'is_dir')):
            raise TypeError("Failed - TypeError (The directory argument must have 'exists' and 'is_dir' methods.)")
    
        # Check if directory_path is a directory
        if not directory_path.is_dir():
            raise ValueError(f"Failed - Value Error ('{directory_path}' is not a directory)")

        # Check if directory_path is accessible
        if not directory_path.exists():
            raise FileNotFoundError(
                f"Failed - FileNotFoundError ('{directory_path}' does not exist.)")

        # Check if directory_path is non-empty
        if not any(directory_path.iterdir()):
            raise ValueError(f"Failed - ValueError ('{directory_path}' is empty.)")

        # Ensure directory_path is a non-immediate sub-directory of git_root
        try:
            directory_path.relative_to(groot)
        except ValueError:
            raise ValueError(
                f"Failed - ValueError ('{directory_path}' is not a sub-directory of '{groot}')."
            )

        # If all checks pass, return True
        return True

    except (ValueError, FileNotFoundError) as e:
        print(e)
        return False

def fetch_files_by_extension(directory: Path, file_extension: str) -> List[Path]:
    """
    Returns a list of files in the specified directory that have the given file extension.
    
    Parameters:
    - directory (Path): The directory to search within.
    - file_extension (str): The file extension to match without the dot (e.g., 'txt', 'jpg').

    Returns:
    - List[Path]: A list of Path objects representing the files with the specified extension.
    """

    # Assert Arguments
    assert isinstance(directory, Path), "The 'directory' argument must be of type Path."
    assert isinstance(file_extension, str), "The 'file_extension' argument must be a string."
    
    if validate_directory(directory_path=directory):

        # Validate the type of file_extension argument
        if not validate_file_extension(file_extension):
            raise ValueError("Failed - File Extension Validation")

        try:
            
            # Get all files with the specified extension
            files = [
                file for file in directory.iterdir()
                if file.is_file() and file.suffix[1:] == file_extension
            ]

        except (OSError, PermissionError) as e:
            
            print(f"Error accessing files in the directory: {e}")
            return []
        
        except Exception as e:
        
            print(f"An unexpected error occurred during file filtering: {e}")
            return []

        # Assert that files is a list
        assert isinstance(files, list), "The 'files' variable must be a list."
        
        return files
    
    return []

