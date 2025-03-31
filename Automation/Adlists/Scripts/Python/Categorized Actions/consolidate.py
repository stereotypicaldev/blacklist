import os
import re
import requests
from urllib.parse import urlparse, urljoin, urlunparse
from pathlib import Path
import logging
import validators
import idna
import ipaddress

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Find the Git repository root
def find_git_root(start_path):
    current_path = Path(start_path).resolve()
    while current_path != current_path.parent:
        if (current_path / '.git').exists():
            return current_path
        current_path = current_path.parent
    raise FileNotFoundError("Git repository root not found")

# Check string is valid URL
def is_valid_url(url):
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc)

# Check URL is accessible and has non-empty content
def is_accessible_and_non_empty(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and response.text.strip():
            return True
    except requests.RequestException:
        pass
    return False

# Check domain Pihole Compatibillity
def check_compatibility(domain):
    
    domain_regex = re.compile(
        r'^(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,63}$'
    )

    try:
        # Check domain format with regex
        if not domain_regex.match(domain):
            return False
        
        # Check domain format using validators library
        if validators.domain(domain) is None:
            return False
        
        # Handle Internationalized Domain Names (IDNs)
        idna_domain = idna.encode(domain).decode('ascii')
        
        # Validate IDN domain with validators
        if validators.domain(idna_domain) is None:
            return False

        if domain.startswith(('http://', 'https://')):
            return False

        return True

    except (idna.IDNAError, ValueError):

        return False

def transform_to_compatible(domain):
    try:

        # Parse the URL and extract the network location (domain)
        parsed_url = urlparse(domain)
        
        # Extract the domain part
        domain = parsed_url.hostname
        
        # If domain is None or empty, return an empty string
        if not domain:
            return ""
        
        # Skip if the domain is an IPv6 address
        if domain.startswith('[') and domain.endswith(']'):
            # Remove square brackets for further processing
            domain = domain[1:-1]
            try:
                ipaddress.IPv6Address(domain)
                return ""  # Skip IPv6 addresses
            except ipaddress.AddressValueError:
                pass  # Not a valid IPv6 address, continue processing
    
    except ValueError:
        return ""
    
    # Use regex to clean and validate the domain
    domain = domain.lower()  # Convert to lowercase for consistency
    
    # Remove invalid characters and enforce domain name rules
    valid_domain = re.sub(r'[^a-zA-Z0-9.-]', '', domain)
    
    # Remove trailing dots (not allowed in TLDs)
    valid_domain = valid_domain.rstrip('.')
    
    # Optionally: Check if domain is valid by a simple regex pattern
    if re.match(r'^(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,63}$', valid_domain):
        return valid_domain
    else:
        return ""  # Return an empty string if the domain is invalid

# Process Files for Adlists
def process_files(input_folder):
    # Initialize a set to store unique, valid, and accessible URLs
    unique_urls = set()

    # Iterate over each file in the specified input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            logging.info(f'Processing file: {file_path}')
            
            # Open the text file and process it line by line
            with open(file_path, 'r') as file:
                for line_number, line in enumerate(file, start=1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    logging.info(f'{filename} - {line_number}: {line}')
                    
                    # Verify if the line is a valid URL
                    if is_valid_url(line):
                        # Check if the URL is accessible and non-empty
                        if is_accessible_and_non_empty(line):
                            unique_urls.add(line)  # Add the URL to the set
    
    return unique_urls

def scrape_urls(database: set):
    domains = set()
    
    for count, entry in enumerate(database):
        logging.info(f'Currently at {count} - {entry}')
        try:

            # Fetch the content of the URL
            response = requests.get(entry, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Get the content as text
            content = response.text.splitlines()

            for row in content:
               
                if not str(row).strip():
                    continue    
               
                if check_compatibility(domain=row): 
                    domains.add(str(row))
                    continue
                
                transformed = transform_to_compatible(domain=row)
                
                if not (str(transformed).strip()):
                    continue
                elif check_compatibility(domain=transformed):
                    domains.add(str(row))
                    continue

        except requests.RequestException as e:
        
            print(f"Failed to fetch or process : {e}")
      
    return domains

# Repository Directory
repo_root = find_git_root(__file__)

# Relative Paths 
input_folder = repo_root / 'Consolidate' / 'Input'
output_file = repo_root / 'Consolidate' / 'Output' / 'domains.txt'

# Ensure the output directory exists
output_file.parent.mkdir(parents=True, exist_ok=True)

# Run the script
unique = process_files(input_folder)
domains = scrape_urls(database=unique)

with open(output_file, 'w') as file:
    for item in domains:
        file.write(f"{item}\n")

print(f"Successful Operation - {len(domains)} were processed.")

