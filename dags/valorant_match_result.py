"""
This module contains functions and classes for web scraping.
It demonstrates how to fetch a webpage and parse its HTML content
using the requests and BeautifulSoup libraries.

source = www.tunwalai.com
"""
from typing import Optional
import logging
from bs4 import BeautifulSoup
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

def fetch_web_content(url: str) -> Optional[str]:
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
        logger_err("Request failed for " + url)
        raise
    except RequestException as e:
        logger_err("An error occurred while fetching data from " + url)
        raise


def extract_web_data(web_data: str) -> Optional[str] :
    """
    Extract and returns the HTML content of the web_data.

    Args:
        web_data (str): The content in web page.

    Returns:
        Optional[str]: The HTML content of the page as a string, or None if the request fails.

    Raises:
        ValueError: If the URL is not a valid string.
        RequestException: For any issues during the HTTP request.
    """
    if not isinstance(web_data, str) or not web_data.strip():
        raise ValueError("The web_data must be a non-empty string.")

    try:
        web_content = BeautifulSoup(web_data, 'html.parser')
        # print(web_content.text)
        wrapper_body = web_content.find('div', attrs={'id': 'wrapper'})
        col_container = wrapper_body.find(class_='col-container')
        col_mod_1 = col_container.find(class_='col mod-1')
        # content area
        date = None
        
        for row in col_mod_1.find_all('div'):
            if row is not None and row.has_attr('class'):
                # print(row['class'])
                if 'wf-label' in row['class']:
                    print("At => " + row.text.strip())
                    date = row.text.strip()
                elif 'wf-card' in row['class'] and date is not None:
                    print("found match!")
                    matches = row.find_all('a')
                    for match in matches:
                        time_match = match.find('div', class_='match-item-time').text.strip()
                        teams = match.find_all('div', class_='match-item-vs-team')

                        team_name_class = 'match-item-vs-team-name'
                        team_score_class = 'match-item-vs-team-score'
                        t1_name = teams[0].find('div', class_=team_name_class).text.strip()
                        t1_score = teams[0].find('div', class_=team_score_class).text.strip()
                        t2_name = teams[1].find('div', class_=team_name_class).text.strip()
                        t2_score = teams[1].find('div', class_=team_score_class).text.strip()
                        event_name = match.find('div', class_='match-item-event').text.strip()
                        print(f"Time: {time_match}")
                        print(f"Team 1: {t1_name} - Score: {t1_score}")
                        print(f"Team 2: {t2_name} - Score: {t2_score}")
                        print(f"Event: {event_name.strip()}")
                        print("-" * 40)
                        date = None
    except:
        logger_err("someting went wrong")
        raise
    return ""

def valorant_match_result():
    web_data = fetch_web_content('https://www.vlr.gg/matches/results')
    extract_web_data(web_data)


valorant_match_result()
