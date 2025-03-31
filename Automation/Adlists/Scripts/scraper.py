import chardet
import os
import urllib.parse
import requests
import validators
import re

# Write a function that checks if the file exists, is readable and is accessable 

def check_file_accessibility(filepath):
    """
    Checks if the file exists, is readable, writable, and accessible.
    
    Args:
        filepath (str): Path to the file to be checked.
    """

    accessibility = {
        'exists': False,
        'readable': False,
        'writable': False,
        'accessible': False
    }

    try:
        # Check if the file exists
        if os.path.isfile(filepath):
            accessibility['exists'] = True
        else:
            print(f"File does not exist.")
            return False
        
        # Check if the file is readable
        try:
            with open(filepath, 'r'):
                accessibility['readable'] = True
        except PermissionError:
            print(f"Permission denied - Read file")
            return False
        except Exception as e:
            print(f"An unexpected error occurred while checking readability: {e}")
            return False
        
        # Check if the file is writable
        try:
            with open(filepath, 'a'):
                accessibility['writable'] = True
        except PermissionError:
            print(f"Permission denied - Write to file.")
            return False
        except Exception as e:
            print(f"An unexpected error occurred while checking writability: {e}")
            return False
        
        # Update accessible status based on other checks
        accessibility['accessible'] = (accessibility['exists'] and 
                                       accessibility['readable'] and 
                                       accessibility['writable'])
        
        if accessibility['accessible']:
            print(f"File exists and is readable, writable, and accessible.")
            return True
        else:
            print(f"File is not fully accessible.")
            return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def is_valid_url(url):
    try:

        parsed = urllib.parse.urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            return False
        if not validators.url(url):
            return False
        return True
    
    except ValueError:
        return False

def is_url_reachable(url,timeout=5):

    successful_status_codes = {200, 201, 203, 205, 206, 302, 303}

    status_code_descriptions = {
        301: "Moved Permanently",
        307: "Temporary Redirect",
        308: "Permanent Redirect",
        400: "Bad Request",
        401: "Unauthorized",
        402: "Payment Required",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        407: "Proxy Authentication Required",
        408: "Request Timeout",
        409: "Conflict",
        410: "Gone",
        411: "Length Required",
        412: "Precondition Failed",
        413: "Payload Too Large",
        414: "URI Too Long",
        415: "Unsupported Media Type",
        416: "Range Not Satisfiable",
        417: "Expectation Failed",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
        505: "HTTP Version Not Supported",
    }

    try:
    
        response = requests.get(url, timeout=timeout)
        if response.status_code in successful_status_codes:
            return True
    
        description = status_code_descriptions.get(response.status_code, "Unknown Status Code")
        print(f"HTTP Error {response.status_code}: {description}")
        return False
    
    except (requests.RequestException, requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        return False

def process_line(line):
    if isinstance(line, bytes):
        try:
            # Try to decode the bytes to UTF-8
            line = line.decode('utf-8')
        except UnicodeDecodeError:
            # If decoding to UTF-8 fails, use detected encoding
            encoding = chardet.detect(line)['encoding']
            try:
                line = line.decode(encoding)
            except (UnicodeDecodeError, TypeError):
                # If both attempts fail, return None
                return None
    elif isinstance(line, str):
        # If the input is already a string, return it as is
        return line
    else:
        # If the input is neither bytes nor string, return None
        return None
    return line

def normalize_url(url):
    return url.lower().rstrip('/')

def check_terms(variable, filename="Terms.txt"):
    results = {}

    try:
        with open(filename, 'r') as file:
            for line in file:
                pattern = line.strip()  # Read and strip any extra whitespace/newlines
                if pattern:  # Skip empty lines
                    try:
                        # Compile the regex pattern and search the variable
                        regex = re.compile(pattern, re.IGNORECASE)
                        if regex.search(variable):
                            print(f'Skipped - Matched term "{pattern}"')
                            return True
                    except re.error as e:
                        print(f"Invalid regex pattern: {pattern}. Error: {e}")
            return False
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
        return False
    
def check_TLDs(var, file="TLDs.txt"):
    
    try:
        with open(file, 'r') as F:
            for TLD in F:
                pattern = TLD.strip()
                if pattern:
                    try:
                        regex = re.compile(rf'\.{pattern}$|{pattern}$')
                        if regex.search(var):
                            print(f'Skipped - Top Level Domain(TLD) matched "{pattern}"')
                            return True
                    except re.error as e:
                        print(f"Invalid regex pattern: {pattern}. Error: {e}")
            return False
    
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
        return False
    
def main(filepath):
    Unique = {}
    if check_file_accessibility(filepath):
        try:
            with open(filepath, 'r') as file:
                for line_number, line in enumerate(file, start=1):
                    print("Currently on line ", line_number)
                    line = process_line(line)
                
                    if line is None:
                        continue  # Skip lines that couldn't be processed
                
                    stripped_line = line.strip()  # Remove leading/trailing whitespace
                    if is_valid_url(stripped_line):
                        if is_url_reachable(stripped_line):
                            normalized = normalize_url(stripped_line)
                            if not check_TLDs(normalized):
                                if not check_terms(normalized):
                                    if normalized not in Unique:
                                        # Add the URL to the dictionary with a default value (e.g., None or any other value)
                                        Unique[normalized] = line_number
                                        print(f"Appended line by number {line_number} to Dictionary")
                                        continue
                    continue

        except Exception as e:
            print(e)

    try:
        with open("/home/user/Music/Blacklist/Testing/Purpose.txt", 'w') as file:
            # Write each key to the file, each on a new line
            for key in Unique.keys():
                file.write(f"{key}\n")
        print(f"{len(Unique)} keys have been written to unique.txt")
    except Exception as e:
        print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    # Example file path; replace with actual path as needed.
    filepath = "/home/user/Music/Blacklist/Testing/Unique.txt"
    main(filepath)

