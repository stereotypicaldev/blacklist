from pathlib import Path
import os
from typing import Set

from urls_operations import validate_format, is_active, extract_domains
from misc import validate_url_via_parse, validate_url_via_regex

def validate_file(path: Path) -> bool:
    """
    
    Check if a given FilePath object is valid.
    
    """
    try:

        # Check if given parameter is a valid Path object
        assert isinstance(path, Path), "The provided path is not a valid Path object."
        
        # Check if the path exists
        if not path.exists():
            raise FileNotFoundError("The file does not exist.")
        
        # Check if it is a file and not a directory
        if not path.is_file():
            raise IsADirectoryError("The path is not a file.")
        
        # Check if the file is accessible
        if not os.access(path, os.R_OK):
            raise PermissionError("The file is not accessible.")
        
        # Check if the file is readable
        with path.open('r'):
            pass      
            
        return True
    
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except FileNotFoundError as fnf:
        print(f"FileNotFoundError: {fnf}")
    except IsADirectoryError as iae:
        print(f"IsADirectoryError: {iae}")
    except PermissionError as pe:
        print(f"PermissionError: {pe}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return False

def parse_sources(FilePath: Path) -> Set[str]:
    """
    
    Parses the file at FilePath and returns a set of unique, properly formatted URLs. (based on Pihole Domains)

    """
    unique = set()
    
    with FilePath.open('r') as file:
        for line in file:
            if line and not line.isspace():
                
                # Remove leading and trailing whitespace + Validate Format
                if validate_format(line.strip()): 
                    unique.add(line.strip())
            continue

    return unique

def aggregate_domains(Sources: Set) -> Set[str]:
    domains = set()

    for index, source in enumerate(Sources,start=1):
        print(f"Processing - {index}/{len(Sources)}")
        if is_active(source):
            domains.update(extract_domains(source))

    return domains

def extract_to_file(file_path: Path, domains: Set[str]) -> bool:
    """
    Writes the contents of a Domains (Set) to a specified file.
    """
    try:

        # Ensure domains is a Set of strings
        if not isinstance(domains, set) or not all(isinstance(domain, str) for domain in domains):
            raise TypeError("domains must be a Set of strings.")
        
        # Write domains to file
        with file_path.open('w') as file:
            for domain in domains:
                file.write(f"{domain}\n")
        
        # Check that the file is non-empty and has the expected number of lines
        with file_path.open('r') as file:
            lines = file.readlines()
        
        # Ensure the file is not empty and has exactly as many lines as the number of domains
        assert len(lines) > 0, "File is empty after writing."
        assert len(lines) == len(domains), "File does not contain the expected number of lines."
        
        return True
    
    except AssertionError as e:
        return False
    except IOError as e:
        return False
    except TypeError as e:
        return False
    except Exception as e:
        return False

def extract_unique(Finput: Path) -> set:
    """
    Reads a file line by line and returns a unique set of lines.
    
    Returns - A set of properly formatted URLs.
    """

    # Ensure Finput is a Path object
    assert isinstance(Finput, Path), "File input must be of type Path"
    
    # Ensure the file exists
    assert Finput.exists(), "The file does not exist"

    # Ensure the file is not a directory
    assert Finput.is_file(), "Finput must be a file, not a directory"

    # Initiate Set
    unique = set()

    try:
        # Open the file and read lines
        with Finput.open('r', encoding='utf-8') as file:
            for line in file:

                # Remove any surrounding whitespace characters
                line = line.strip()

                if line not in unique:
                    unique.add(line)
        
    except (IOError, OSError) as e:
        print(f"An error occurred while reading the file: {e}")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return unique

def parse_blocklists(sources: set) -> set:

    # Assert to check that 'sources' is a set
    assert isinstance(sources, set), "Sources must be a set type."

    # Assert to check that all items in the set are strings
    assert all(isinstance(item, str) for item in sources), "All items in the set must be strings."

    valid = set()

    try:

        for item in sources:
            if isinstance(item, str) and (item.startswith('http://') or item.startswith('https://')):
                if validate_url_via_parse and validate_url_via_regex:
                    valid.add(item)
        
    except Exception as e:
        print(f"An error occurred: {e}")

    return valid

