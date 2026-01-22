"""
Filename sanitization utilities for the Digital FTE Automation system.
"""

import re
from pathlib import Path
from typing import Tuple
from datetime import datetime


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing or replacing problematic characters.
    
    Args:
        filename: The original filename
        
    Returns:
        str: The sanitized filename
    """
    # Replace invalid characters with underscores
    invalid_chars_pattern = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars_pattern, '_', filename)
    
    # Remove control characters (ASCII 0-31)
    sanitized = ''.join(char for char in sanitized if ord(char) >= 32)
    
    # Handle leading/trailing spaces and periods on Windows
    sanitized = sanitized.strip(' .')
    
    # Ensure the filename is not empty after sanitization
    if not sanitized:
        sanitized = f"unnamed_file_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Limit filename length (most filesystems limit to 255 characters)
    if len(sanitized) > 250:  # Leave some room for extension
        name, ext = Path(sanitized).stem, Path(sanitized).suffix
        sanitized = name[:250-len(ext)] + ext
    
    return sanitized


def handle_duplicate_filename(filepath: str, max_attempts: int = 100) -> str:
    """
    Handle duplicate filenames by appending a timestamp.
    
    Args:
        filepath: The original file path
        max_attempts: Maximum number of attempts to find a unique name
        
    Returns:
        str: A unique file path
    """
    path_obj = Path(filepath)
    stem = path_obj.stem
    suffix = path_obj.suffix
    parent = path_obj.parent
    
    # If the file doesn't exist, return the original path
    if not path_obj.exists():
        return str(path_obj)
    
    # Try to find a unique filename by appending a timestamp
    for i in range(max_attempts):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")  # Include microseconds
        new_stem = f"{stem}_{timestamp}"
        new_path = parent / f"{new_stem}{suffix}"
        
        if not new_path.exists():
            return str(new_path)
    
    # If we couldn't find a unique name within max_attempts, raise an error
    raise FileExistsError(f"Could not create a unique filename after {max_attempts} attempts")