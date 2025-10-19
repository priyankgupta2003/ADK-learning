"""Web search and content extraction tools for Research Assistant Agent.

Note: For learning purposes, this uses a simplified search implementation.
For production, consider using Google Custom Search API or other paid search APIs.
"""

import requests
from typing import List, Dict, Optional
from urllib.parse import quote, urlparse
import time
import re

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

from config import (
    GOOGLE_SEARCH_API_KEY,
    GOOGLE_SEARCH_ENGINE_ID,
    MAX_SEARCH_RESULTS,
    SEARCH_TIMEOUT,
    CONTENT_TIMEOUT,
    USER_AGENT,
    MAX_CONTENT_LENGTH,
    MIN_CONTENT_LENGTH
)


class SearchError(Exception):
    """Custom exception for search-related errors."""
    pass


def search_google_custom(query: str, num_results: int = 5) -> List[Dict]:
    """
    Search using Google Custom Search API.
    
    Args:
        query: Search query string
        num_results: Number of results to return (max 10 per request)
    
    Returns:
        List of search results with title, link, and snippet
    """
    if not GOOGLE_SEARCH_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
        raise SearchError("Google Custom Search API credentials not configured")
    
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_SEARCH_API_KEY,
            "cx": GOOGLE_SEARCH_ENGINE_ID,
            "q": query,
            "num": min(num_results, 10)
        }
        
        response = requests.get(url, params=params, timeout=SEARCH_TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        
        results = []
        for item in data.get("items", []):
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "source": urlparse(item.get("link", "")).netloc
            })
        
        return results
    
    except requests.exceptions.RequestException as e:
        raise SearchError(f"Search API error: {str(e)}")


def search_duckduckgo(query: str, num_results: int = 5) -> List[Dict]:
    """
    Search using DuckDuckGo HTML scraping (fallback method).
    
    Note: Requires BeautifulSoup4. Install with: pip install beautifulsoup4
    
    Args:
        query: Search query string
        num_results: Number of results to return
    
    Returns:
        List of search results
    """
    if not BS4_AVAILABLE:
        raise SearchError("BeautifulSoup4 not installed. Run: pip install beautifulsoup4")
    
    try:
        headers = {"User-Agent": USER_AGENT}
        url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
        
        response = requests.get(url, headers=headers, timeout=SEARCH_TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        for result in soup.find_all('div', class_='result')[:num_results]:
            title_elem = result.find('a', class_='result__a')
            snippet_elem = result.find('a', class_='result__snippet')
            
            if title_elem:
                link = title_elem.get('href', '')
                title = title_elem.get_text(strip=True)
                snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                
                results.append({
                    "title": title,
                    "link": link,
                    "snippet": snippet,
                    "source": urlparse(link).netloc if link else ""
                })
        
        return results
    
    except Exception as e:
        raise SearchError(f"DuckDuckGo search error: {str(e)}")


def search_web(query: str, num_results: int = 5) -> List[Dict]:
    """
    Search the web using available methods (Custom Search API or fallback).
    
    Args:
        query: Search query string
        num_results: Number of results to return
    
    Returns:
        List of search results
    """
    # Try Custom Search API first
    if GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_ENGINE_ID:
        try:
            return search_google_custom(query, num_results)
        except SearchError:
            pass
    
    # Fallback to DuckDuckGo (requires BeautifulSoup)
    if BS4_AVAILABLE:
        try:
            return search_duckduckgo(query, num_results)
        except SearchError as e:
            print(f"Warning: Search failed - {str(e)}")
    
    # If nothing works, return simulated results for learning purposes
    print(f"Note: Real search not available. Returning simulated results for learning.")
    return _get_simulated_search_results(query, num_results)


def _get_simulated_search_results(query: str, num_results: int = 5) -> List[Dict]:
    """
    Return simulated search results for learning purposes.
    This allows the project to work without requiring web scraping dependencies.
    
    Args:
        query: Search query
        num_results: Number of results to return
    
    Returns:
        List of simulated search results
    """
    # Generate educational mock results
    results = []
    for i in range(min(num_results, 5)):
        results.append({
            "title": f"Article {i+1}: {query}",
            "link": f"https://example.com/article-{i+1}-{query.replace(' ', '-')}",
            "snippet": f"This is a sample article about {query}. It provides comprehensive information on the topic, including key concepts, recent developments, and practical applications. For learning purposes, this is a simulated search result.",
            "source": "example.com"
        })
    
    return results


def extract_article_content(url: str) -> Dict:
    """
    Extract the main content from a web page.
    
    Args:
        url: URL of the web page
    
    Returns:
        Dictionary containing extracted content
    """
    if not BS4_AVAILABLE:
        # Return simulated content for learning
        return _get_simulated_article_content(url)
    
    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(url, headers=headers, timeout=CONTENT_TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Try to find the main content
        article = soup.find('article') or soup.find('main') or soup.find('div', class_=re.compile('content|article|post'))
        
        if article:
            content_elem = article
        else:
            content_elem = soup.find('body')
        
        # Extract text
        if content_elem:
            text = content_elem.get_text(separator='\n', strip=True)
            # Clean up multiple newlines
            text = re.sub(r'\n\s*\n', '\n\n', text)
            text = text[:MAX_CONTENT_LENGTH]
        else:
            text = ""
        
        # Extract title
        title_elem = soup.find('title') or soup.find('h1')
        title = title_elem.get_text(strip=True) if title_elem else ""
        
        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '') if meta_desc else ""
        
        # Basic validation
        if len(text) < MIN_CONTENT_LENGTH:
            raise SearchError("Insufficient content extracted")
        
        return {
            "url": url,
            "title": title,
            "description": description,
            "content": text,
            "length": len(text),
            "source": urlparse(url).netloc
        }
    
    except requests.exceptions.RequestException as e:
        raise SearchError(f"Failed to fetch URL {url}: {str(e)}")
    except Exception as e:
        raise SearchError(f"Content extraction error: {str(e)}")


def _get_simulated_article_content(url: str) -> Dict:
    """
    Return simulated article content for learning purposes.
    This allows the project to work without web scraping dependencies.
    
    Args:
        url: URL (for reference)
    
    Returns:
        Dictionary with simulated content
    """
    # Extract topic from URL
    topic = urlparse(url).path.split('/')[-1].replace('-', ' ').replace('.html', '')
    
    content = f"""
{topic.title()}

This is simulated article content for learning purposes. In a production environment, 
this would contain the actual extracted content from the web page.

Key Points:
- This demonstrates how the research agent processes article content
- Real implementation would use BeautifulSoup4 or similar libraries
- For production, consider using APIs or paid content extraction services

The agent can use this content to synthesize information and generate reports.
This simulated content allows you to learn the Google ADK agent patterns without 
dealing with the complexity of web scraping.

To enable real web scraping:
1. Install: pip install beautifulsoup4
2. The agent will automatically use real web content extraction
"""
    
    return {
        "url": url,
        "title": f"Article about {topic}",
        "description": f"Information about {topic}",
        "content": content.strip(),
        "length": len(content),
        "source": urlparse(url).netloc
    }


def extract_multiple_articles(urls: List[str], delay: float = 1.0) -> List[Dict]:
    """
    Extract content from multiple URLs with rate limiting.
    
    Args:
        urls: List of URLs to extract content from
        delay: Delay between requests in seconds
    
    Returns:
        List of extracted content dictionaries
    """
    articles = []
    
    for i, url in enumerate(urls):
        try:
            if i > 0:
                time.sleep(delay)  # Rate limiting
            
            article = extract_article_content(url)
            articles.append(article)
        except SearchError as e:
            print(f"Warning: Failed to extract {url}: {str(e)}")
            continue
    
    return articles


def summarize_search_results(results: List[Dict]) -> str:
    """
    Create a text summary of search results.
    
    Args:
        results: List of search result dictionaries
    
    Returns:
        Formatted string summary
    """
    if not results:
        return "No search results found."
    
    lines = [f"Found {len(results)} results:\n"]
    
    for i, result in enumerate(results, 1):
        lines.append(f"{i}. {result['title']}")
        lines.append(f"   URL: {result['link']}")
        lines.append(f"   {result['snippet']}\n")
    
    return "\n".join(lines)


def validate_url(url: str) -> bool:
    """
    Validate if a URL is properly formatted and accessible.
    
    Args:
        url: URL string to validate
    
    Returns:
        True if valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

