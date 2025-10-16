import requests
from bs4 import BeautifulSoup
import re
from langchain.tools import tool
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()

@tool
def scrape_website(url: str) -> str:
    """
    Scrapes the text content of a given website URL. 
    It takes a single URL as input and returns the cleaned text from that page,
    limited to the first 5000 characters to ensure efficiency. This tool
    should be used after the 'search_tool' has found a relevant URL.
    """
    print(f"--- Scraping URL: {url} ---")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        text = soup.get_text(separator=" ", strip=True)
        
        text = re.sub(r'\s+', ' ', text)

        return text[:5000]
    except requests.exceptions.RequestException as e:
        return f"Error during web request: {e}"
    except Exception as e:
        return f"Error scraping website: {e}"

