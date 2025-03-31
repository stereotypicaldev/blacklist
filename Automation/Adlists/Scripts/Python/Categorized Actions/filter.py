from pathlib import Path
import sys

# Add the directory containing File_Operations.py to sys.path
shared_functions_path = Path(__file__).resolve().parent.parent / 'Shared Functions'
sys.path.append(str(shared_functions_path))

# Import Helper Functions
from file_operations import validate_file, extract_unique, parse_blocklists
from git_root_path import identify_root
from directory_operations import validate_directory, fetch_files_by_extension

# Get Git Root Path
groot = identify_root()

# Set Working Folder Path
input_directory = Path(groot.joinpath("Filtering", "Blocklists"))

if validate_directory(directory_path=input_directory):

    # Fetch Files via txt extension
    blocklists = fetch_files_by_extension(directory=input_directory,file_extension="txt")

    # Initiate Set
    unique_sources = set()

    for x in blocklists:
        # Validate blocklists files
        if validate_file(x):
            # Read and Extract
            unique_sources.update(extract_unique(x))

    parsed = parse_blocklists(sources=unique_sources)
    print(len(parsed))


