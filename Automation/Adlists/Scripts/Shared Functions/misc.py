import re
from urllib.parse import urlparse

def validate_file_extension(ext: str) -> bool:

    # Assert Arguments
    assert isinstance(ext, str), "File extension must be a string."
    assert ext is not None, "File extension cannot be None."
    assert 1 <= len(ext) <= 10, "File extension length must be between 1 and 10 characters long."

    if not ext:
        raise ValueError("File extension cannot be an empty string.")
    
    # Check if the extension length is reasonable (e.g., 1 to 10 characters)
    if not (1 <= len(ext) <= 10):
        raise ValueError("File extension must be between 1 and 10 characters long.")
    
    # Check if the extension matches the expected format (alphanumeric characters only)
    if not re.match(r'^[\w]+$', ext):
        raise ValueError("File extension must contain only alphanumeric characters.")

    return True

def validate_url_via_regex(url: str) -> bool:
    """
    Validate URL using a regex pattern.
    """
    # A simple regex pattern to check the format of a URL
    url_regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https:// or ftp:// or ftps://
        r'(?:\S+(?::\S*)?@)?'  # Optional username:password authentication
        r'(?:'  # Hostname
        r'(?:(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})'  # e.g., domain.com
        r'|'  # Or
        r'\d{1,3}(?:\.\d{1,3}){3}'  # IP address format
        r')'
        r'(?::\d+)?'  # Optional port
        r'(?:[/?#]\S*)?'  # Optional path, query string, and fragment
        r'$', re.IGNORECASE
    )
    return re.match(url_regex, url) is not None

def validate_url_via_parse(url: str) -> bool:
    """
    Validate URL using urllib's urlparse.
    """
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])

