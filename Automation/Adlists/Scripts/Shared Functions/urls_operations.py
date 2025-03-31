import re
from typing import Set
from urllib.parse import urlparse, urlunparse
import validators
import requests
from bs4 import BeautifulSoup

def validate_format(url: str) -> bool:
    """
    Validate if the given string is a properly encoded URL.

    Parameters:
    - url (str): The URL string to validate.

    Returns:
    - bool: True if the URL is valid and properly encoded, False otherwise.
    """

    # Assert that the url is a string
    assert isinstance(url, str), "The URL must be a string."

    # Check if the URL is a non-empty string
    if not url:
        raise ValueError("The URL cannot be an empty string.")

    # Regular expression for basic URL validation
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE)  # path

    # Validate URL format with regex
    if not re.match(url_pattern, url.strip()):
        raise ValueError("The URL format is invalid.")
    
    try:

        # Parse URL components
        parsed_url = urlparse(url)

        # Assert that the URL scheme and netloc are present
        assert parsed_url.scheme in [
            'http', 'https', 'ftp'
        ], "The URL scheme must be 'http', 'https', or 'ftp'."
        assert parsed_url.netloc, "The URL must have a network location (netloc)."

        # Assert that URL components are properly encoded
        # Reconstruct URL and compare with original to check encoding
        reconstructed_url = urlunparse(parsed_url)
        assert url == reconstructed_url, "The URL is not properly encoded."

    except AssertionError as e:
        raise ValueError(f"URL validation error: {e}")

    if not validators.url(url):
        raise ValueError("Invalid URL format.")

    return str(url).strip()

def is_active(url: str) -> bool:
    try:
        # Perform a HEAD request to check if URL is reachable
        response = requests.head(url, allow_redirects=True)
        
        # Check if the response status code indicates success
        if response.status_code >= 200 and response.status_code < 300:
            # Perform a GET request to check if the content is non-empty
            response = requests.get(url, allow_redirects=True)
            
            # Check if the content is not empty
            if response.status_code >= 200 and response.status_code < 300 and len(response.content) > 0:
                return True
                
    except requests.RequestException:
        # Catch any request-related exceptions and return False
        return False

    return False

def is_compatible_with_pihole(domain: str) -> bool:
    """
    Checks if the given string is a valid domain name compatible with Pi-hole.
    
    :param domain: The domain name to check.
    :return: True if the domain is compatible with Pi-hole, False otherwise.
    """
    # Check if the domain is not empty and does not exceed the maximum length
    if not domain or len(domain) > 253:
        return False
    
    # Regular expression to check if the domain follows standard domain naming conventions
    domain_regex = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+(?:[a-zA-Z]{2,})$'
    )
    
    # Validate the domain format
    if not domain_regex.match(domain):
        return False
    
    # Check for invalid characters or malformed domain structure
    # Domains should not start or end with a hyphen and should not have consecutive hyphens
    if '--' in domain or domain.startswith('-') or domain.endswith('-'):
        return False
    
    return True

def extract_domains(url: str) -> Set[str]:
    extracted_domains = set()

    try:
        # Fetch the content of the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
            
        # Use BeautifulSoup to parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract and process the text content
        for line in soup.get_text().splitlines():
            stripped_line = line.strip()
            if stripped_line:  # Ignore empty lines
                if is_compatible_with_pihole(stripped_line):
                    extracted_domains.add(stripped_line)
                    continue
                
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
    
    return extracted_domains

