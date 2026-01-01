import os
from pathlib import Path
from typing import Optional

def read_file(file_path: str) -> str:
    """
    Read the contents of a file.
    
    Args:
        file_path: Path to the file to read
    
    Returns:
        File contents as a string, or error message if file cannot be read
    """
    try:
        path = Path(file_path).expanduser()
        
        if not path.exists():
            return f"Error: File '{file_path}' does not exist."
        
        if not path.is_file():
            return f"Error: '{file_path}' is not a file."
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content
    
    except Exception as e:
        return f"Error reading file '{file_path}': {str(e)}"


def write_file(file_path: str, content: str, append: bool = False) -> str:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file to write
        content: Content to write to the file
        append: If True, append to file. If False, overwrite (default: False)
    
    Returns:
        Success message or error message
    """
    try:
        path = Path(file_path).expanduser()
        
        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        mode = 'a' if append else 'w'
        with open(path, mode, encoding='utf-8') as f:
            f.write(content)
        
        action = "Appended to" if append else "Wrote to"
        return f"{action} file '{file_path}' successfully. ({len(content)} characters)"
    
    except Exception as e:
        return f"Error writing to file '{file_path}': {str(e)}"
