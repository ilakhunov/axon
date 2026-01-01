"""
Retry decorator for automatic error recovery.
"""
import time
import functools
from typing import Callable, Optional, Type, Tuple
from .utils import get_logger

logger = get_logger()

def retry(
    max_attempts: int = 3,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator that retries a function on failure with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        backoff: Multiplier for exponential backoff in seconds (default: 2.0)
        exceptions: Tuple of exception types to catch (default: all Exception)
    
    Example:
        @retry(max_attempts=3, backoff=2.0)
        def flaky_api_call():
            return requests.get("https://api.example.com/data").json()
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts:
                        # Last attempt failed, raise the exception
                        logger.error(
                            f"[bold red]Function {func.__name__} failed after {max_attempts} attempts[/]: {e}"
                        )
                        raise
                    
                    # Calculate backoff time
                    wait_time = backoff ** (attempt - 1)
                    
                    logger.warning(
                        f"[yellow]Attempt {attempt}/{max_attempts} failed for {func.__name__}[/]: {e}. "
                        f"Retrying in {wait_time:.1f}s..."
                    )
                    
                    time.sleep(wait_time)
            
            # Should never reach here, but just in case
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator


def retry_on_rate_limit(max_attempts: int = 5, initial_wait: float = 1.0):
    """
    Specialized retry decorator for API rate limits.
    Uses exponential backoff starting from initial_wait.
    
    Args:
        max_attempts: Maximum retry attempts (default: 5)
        initial_wait: Initial wait time in seconds (default: 1.0)
    
    Example:
        @retry_on_rate_limit(max_attempts=5, initial_wait=1.0)
        def call_openai_api():
            return client.chat.completions.create(...)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    # Check if it's a rate limit error
                    error_msg = str(e).lower()
                    is_rate_limit = any(keyword in error_msg for keyword in [
                        'rate limit', 'too many requests', '429', 'quota exceeded'
                    ])
                    
                    if not is_rate_limit or attempt == max_attempts:
                        raise
                    
                    # Exponential backoff for rate limits
                    wait_time = initial_wait * (2 ** (attempt - 1))
                    
                    logger.warning(
                        f"[yellow]Rate limit hit on {func.__name__}[/]. "
                        f"Waiting {wait_time:.1f}s before retry {attempt}/{max_attempts}..."
                    )
                    
                    time.sleep(wait_time)
        
        return wrapper
    return decorator
