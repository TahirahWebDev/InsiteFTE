"""
File handling utilities for the Digital FTE Automation system.
"""

import shutil
from pathlib import Path
from typing import Union
from ..exceptions import FileProcessingError


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
        raise FileProcessingError(f"Failed to move file from {source} to {destination}: {str(e)}")


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
        raise FileProcessingError(f"Failed to copy file from {source} to {destination}: {str(e)}")


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
        raise FileProcessingError(f"Failed to create directory {path}: {str(e)}")


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