"""
Web scraping tools for Axon agents.
Requires: beautifulsoup4, requests
"""
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup


def scrape_url(url: str, extract_links: bool = False, timeout: int = 10) -> str:
    """
    Scrape a webpage and extract text content.
    
    Args:
        url: The URL to scrape
        extract_links: Whether to include links in output
        timeout: Request timeout in seconds
        
    Returns:
        Formatted string with page content
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; AxonBot/1.0)'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get title
        title = soup.title.string if soup.title else "No title"
        
        # Get main text
        text = soup.get_text(separator='\n', strip=True)
        
        # Limit text length
        if len(text) > 5000:
            text = text[:5000] + "...[truncated]"
        
        result = f"Title: {title}\n\nContent:\n{text}"
        
        # Extract links if requested
        if extract_links:
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                link_text = link.get_text(strip=True)
                if href.startswith('http'):
                    links.append(f"{link_text}: {href}")
            
            if links:
                result += f"\n\nLinks found ({len(links)}):\n"
                result += "\n".join(links[:20])  # Limit to 20 links
        
        return result
        
    except requests.RequestException as e:
        return f"Error scraping {url}: {str(e)}"
    except Exception as e:
        return f"Error parsing {url}: {str(e)}"


def scrape_multiple(urls: List[str], timeout: int = 10) -> Dict[str, str]:
    """
    Scrape multiple URLs.
    
    Args:
        urls: List of URLs to scrape
        timeout: Request timeout per URL
        
    Returns:
        Dictionary mapping URLs to their content
    """
    results = {}
    for url in urls:
        results[url] = scrape_url(url, timeout=timeout)
    return results
