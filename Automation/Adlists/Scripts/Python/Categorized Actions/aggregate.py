# Fetch list from Aggregate by Category, concatinate them and output the resulted unique domains

import sys
from pathlib import Path
import time

# Add the directory containing File_Operations.py to sys.path
shared_functions_path = Path(__file__).resolve().parent.parent / 'Shared Functions'
sys.path.append(str(shared_functions_path))

# Import Helper Functions
from file_operations import validate_file, parse_sources, aggregate_domains, extract_to_file
from git_root_path import identify_root
from directory_operations import validate_directory, fetch_files_by_extension

# Get Git Root Path
groot = identify_root()

# Set Folder Path
input_directory = Path(groot.joinpath("Aggregate", "Input"))

# Validate Path
is_valid_directory = validate_directory(directory_path=input_directory)

if is_valid_directory:

    # Fetch Text Files
    for file in fetch_files_by_extension(
            Path(groot.joinpath("Aggregate", "Input")), str("txt")):
        # Verify Files
        if validate_file(file):
            sources = parse_sources(file)
            print(f"Parsed Successfully - {file.name} contains {len(sources)} unique adlists.")
            print("\n")

            if sources:
                domains = aggregate_domains(sources)
                print(f"Successfully Processed {len(domains)} domains from {len(sources)} under {file.name}.")
                print("\n")

                time.sleep(3)  # Done :) Taking a break...

                print(f"Extracting - {len(domains)} to Output/{file.name}")

                if validate_file(
                        Path(
                            groot.joinpath("Aggregate", "Output",
                                           str(file.name)))):
                    # Extract to File

                    success = extract_to_file(file_path=Path(
                        groot.joinpath("Aggregate", "Output", str(file.name))),
                                              domains=domains)

                    if success:
                        print("Success! Extraction has been successfully performed.")
                        print("\n")

    print("Ciao, a presto! 👋")
    sys.exit()

