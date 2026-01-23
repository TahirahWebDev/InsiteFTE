"""
File handling utilities for the Gold Tier Agentic Loop system.
"""

import shutil
from pathlib import Path
from typing import Union
import os
from datetime import datetime


def move_file(source: Union[str, Path], destination: Union[str, Path]) -> bool:
    """
    Move a file from source to destination.
    
    Args:
        source: Path to the source file
        destination: Path to the destination
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        source_path = Path(source)
        dest_path = Path(destination)
        
        # Ensure destination directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Move the file
        shutil.move(str(source_path), str(dest_path))
        return True
    except Exception as e:
        print(f"Failed to move file from {source} to {destination}: {str(e)}")
        return False


def copy_file(source: Union[str, Path], destination: Union[str, Path]) -> bool:
    """
    Copy a file from source to destination.
    
    Args:
        source: Path to the source file
        destination: Path to the destination
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        source_path = Path(source)
        dest_path = Path(destination)
        
        # Ensure destination directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy the file
        shutil.copy2(str(source_path), str(dest_path))
        return True
    except Exception as e:
        print(f"Failed to copy file from {source} to {destination}: {str(e)}")
        return False


def ensure_directory_exists(path: Union[str, Path]) -> bool:
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        path: Path to the directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Failed to create directory {path}: {str(e)}")
        return False


def is_valid_file_type(filepath: Union[str, Path]) -> bool:
    """
    Check if the file has an allowed extension.
    
    Args:
        filepath: Path to the file
        
    Returns:
        bool: True if the file type is allowed, False otherwise
    """
    path = Path(filepath)
    return path.suffix.lower() in {'.txt', '.md'}


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
    import re
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


def add_yaml_frontmatter(
    file_path: str, 
    metadata: dict, 
    preserve_content: bool = True
) -> bool:
    """
    Add YAML frontmatter to a file.
    
    Args:
        file_path: Path to the file
        metadata: Dictionary of metadata to add
        preserve_content: Whether to preserve the existing content
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read the existing content if we need to preserve it
        if preserve_content:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = ""
        
        # Prepare the frontmatter with the metadata
        import uuid
        from datetime import datetime
        frontmatter_data = {
            'id': str(uuid.uuid4()),
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat(),
            **metadata
        }
        
        # Write the frontmatter and content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('---\n')
            import yaml
            from ruamel.yaml import YAML
            yaml = YAML()
            yaml.preserve_quotes = True
            yaml.dump(frontmatter_data, f)
            f.write('---\n')
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error adding YAML frontmatter to {file_path}: {str(e)}")
        return False