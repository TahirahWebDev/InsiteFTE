"""
Web search tool for the Technical Branding Assistant.
Uses Tavily API to fetch information from the web.
"""

import os
import json
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def search_web(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Search the web using Tavily API to fetch information about a topic.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return (default 5)
        
    Returns:
        List of dictionaries containing search results with 'title', 'url', and 'content'
    """
    if not TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY environment variable is not set")
    
    url = "https://api.tavily.com/search"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": max_results,
        "include_answer": True,  # Include AI-generated answer
        "include_raw_content": True,  # Include raw content
        "include_images": False,  # Don't include images
        "search_depth": "advanced"  # Use advanced search
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract results
        results = []
        for result in data.get("results", []):
            results.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", ""),
                "raw_content": result.get("raw_content", "")
            })
        
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request to Tavily API: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error during web search: {e}")
        return []


def simple_search(query: str) -> str:
    """
    Perform a simple web search and return a formatted string with results.
    
    Args:
        query: The search query
        
    Returns:
        Formatted string containing search results
    """
    results = search_web(query)
    
    if not results:
        return f"No results found for query: {query}"
    
    formatted_results = f"Search results for: {query}\n\n"
    
    for i, result in enumerate(results, 1):
        formatted_results += f"Result {i}:\n"
        formatted_results += f"Title: {result['title']}\n"
        formatted_results += f"URL: {result['url']}\n"
        formatted_results += f"Content: {result['content'][:500]}...\n\n"  # Limit content length
    
    return formatted_results


if __name__ == "__main__":
    # Example usage
    query = "Python programming best practices"
    results = simple_search(query)
    print(results)