import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

def check_website_connectivity(input_str):
    """
    Check if a website can be connected to.

    Args:
        url (str): The URL of the website to check.

    Returns:
        bool: True if the website is reachable, False otherwise.
    """
    try:
        url = input_str.get('url')
        if not url:
            raise ValueError("The input dictionary must contain a 'url' key with a valid URL.")
        
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return response.status_code


def get_website_content(input_str):
    """
    Get the content of a website that deploys anti-bot measures.

    Args:
        url (str): The URL of the website to retrieve content from.

    Returns:
        str: The content of the website.
    """
    try:
        url = input_str.get('url')
        if not url:
            raise ValueError("The input dictionary must contain a 'url' key with a valid URL.")
        
        ua = UserAgent()
        headers = {'User-Agent': ua.random}

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.prettify()
    except requests.RequestException as e:
        return f"An error occurred: {e}"


__all__ = ["check_website_connectivity", "get_website_content"]
