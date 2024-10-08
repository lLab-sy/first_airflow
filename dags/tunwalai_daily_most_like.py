"""
This module contains functions and classes for web scraping.
It demonstrates how to fetch a webpage and parse its HTML content
using the requests and BeautifulSoup libraries.

source = www.tunwalai.com
"""
import logging
from typing import Optional
import requests
from requests.exceptions import RequestException, Timeout, HTTPError

def logger_info(msg:str):
    """
    Log the message as info

    Args:
        msg (str): The message that want to log
    """
    logging.info(msg)

def logger_err(msg:str):
    """
    Log the message as error

    Args:
        msg (str): The message that want to log
    """
    logging.error(msg)

def extract_web_content(url: str) -> Optional[str]:
    """
    Fetches and returns the HTML content of the specified URL.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        Optional[str]: The HTML content of the page as a string, or None if the request fails.

    Raises:
        ValueError: If the URL is not a valid string.
        RequestException: For any issues during the HTTP request.
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("The URL must be a non-empty string.")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        logger_info("Successfully retrieved content from" + url)
        return response.text

    except (HTTPError, Timeout) as e:
        logger_err("Request failed for " + url + ": " + e)
        raise
    except RequestException as e:
        logger_err("An error occurred while fetching data from " + url + ": " + e)
        raise

    return None


# URL = 'https://www.tunwalai.com/story/type/toplike?period=daily'