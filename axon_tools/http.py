"""
HTTP/API tools for making REST API requests.
"""
import requests
from typing import Optional, Dict, Any

def http_get(
    url: str, 
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, str]] = None
) -> str:
    """
    Make a GET request to a URL.
    
    Args:
        url: The URL to request
        headers: Optional HTTP headers dictionary
        params: Optional query parameters dictionary
    
    Returns:
        Response text or error message
    """
    try:
        response = requests.get(
            url, 
            headers=headers or {}, 
            params=params or {},
            timeout=10
        )
        response.raise_for_status()
        
        # Try to return JSON if available, otherwise text
        try:
            return str(response.json())
        except:
            return response.text
            
    except requests.exceptions.Timeout:
        return f"Error: Request to {url} timed out after 10 seconds"
    except requests.exceptions.RequestException as e:
        return f"Error making GET request to {url}: {str(e)}"

def http_post(
    url: str,
    data: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None
) -> str:
    """
    Make a POST request to a URL.
    
    Args:
        url: The URL to request
        data: Optional form data dictionary
        json_data: Optional JSON data dictionary
        headers: Optional HTTP headers dictionary
    
    Returns:
        Response text or error message
    """
    try:
        response = requests.post(
            url,
            data=data,
            json=json_data,
            headers=headers or {},
            timeout=10
        )
        response.raise_for_status()
        
        # Try to return JSON if available, otherwise text
        try:
            return str(response.json())
        except:
            return response.text
            
    except requests.exceptions.Timeout:
        return f"Error: Request to {url} timed out after 10 seconds"
    except requests.exceptions.RequestException as e:
        return f"Error making POST request to {url}: {str(e)}"
