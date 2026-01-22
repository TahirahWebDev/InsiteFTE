"""
YAML metadata utilities for the Digital FTE Automation system.
"""

import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from ruamel.yaml import YAML


def add_yaml_frontmatter(
    file_path: str, 
    metadata: Dict[str, Any], 
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
    yaml = YAML()
    yaml.preserve_quotes = True
    
    try:
        # Read the existing content if we need to preserve it
        if preserve_content:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = ""
        
        # Prepare the frontmatter with the metadata
        frontmatter_data = {
            'id': str(uuid.uuid4()),
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat(),
            **metadata
        }
        
        # Write the frontmatter and content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('---\n')
            yaml.dump(frontmatter_data, f)
            f.write('---\n')
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error adding YAML frontmatter to {file_path}: {str(e)}")
        return False


def update_yaml_frontmatter(
    file_path: str, 
    updates: Dict[str, Any]
) -> bool:
    """
    Update existing YAML frontmatter in a file.
    
    Args:
        file_path: Path to the file
        updates: Dictionary of updates to apply
        
    Returns:
        bool: True if successful, False otherwise
    """
    yaml = YAML()
    yaml.preserve_quotes = True
    
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split the content to separate frontmatter and body
        parts = content.split('---', 2)
        if len(parts) < 3:
            # No frontmatter found, add it
            return add_yaml_frontmatter(file_path, updates)
        
        # Parse the existing frontmatter
        frontmatter_str = parts[1].strip()
        frontmatter = yaml.load(frontmatter_str) or {}
        
        # Update the frontmatter with new values
        frontmatter.update(updates)
        frontmatter['updated'] = datetime.now().isoformat()
        
        # Reconstruct the file with updated frontmatter
        body = parts[2]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('---\n')
            yaml.dump(frontmatter, f)
            f.write('---\n')
            f.write(body)
        
        return True
    except Exception as e:
        print(f"Error updating YAML frontmatter in {file_path}: {str(e)}")
        return False


def get_yaml_frontmatter(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Extract YAML frontmatter from a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Optional[Dict]: The frontmatter dictionary if found, None otherwise
    """
    yaml = YAML()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split the content to separate frontmatter and body
        parts = content.split('---', 2)
        if len(parts) < 3:
            # No frontmatter found
            return None
        
        # Parse the frontmatter
        frontmatter_str = parts[1].strip()
        frontmatter = yaml.load(frontmatter_str)
        
        return frontmatter
    except Exception as e:
        print(f"Error reading YAML frontmatter from {file_path}: {str(e)}")
        return None