from langchain.tools import tool
import requests
from tavily import TavilyClient
from bs4 import BeautifulSoup
from rich import print
import os 
from dotenv import load_dotenv
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str :
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets"""

    
    results = tavily.search(query=query , max_results= 1)
    """ print("\nRAW TAVILY RESPONSE:")
    print(results) """
    

    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Snippet: {r['content'][:300]}\n"
        )

    """ print("\nFORMATTED RESULTS:")
    print(out) """

    return "\n------\n".join(out)




# 2nd tool 
@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""

    try:
        # Send HTTP request
        resp = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        # Raise error for HTTP failures (404, 403, 500, etc.)
        resp.raise_for_status()

        # Parse HTML content
        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove unnecessary HTML elements
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        # Extract clean text
        text = soup.get_text(separator=" ", strip=True)

        # Limit output length
        return text[:1000]

    except requests.exceptions.Timeout:
        return "Error: Website took too long to respond."

    except requests.exceptions.RequestException as e:
        return f"Error while fetching URL: {str(e)}"

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"



