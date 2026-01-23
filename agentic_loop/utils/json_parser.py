"""
JSON command parser for the Gold Tier Agentic Loop system.
"""

import json
import re
from typing import Dict, List, Any


def extract_json_blocks(markdown_content: str) -> List[Dict[str, Any]]:
    """
    Extract JSON blocks from markdown content that represent tool calls.
    
    Args:
        markdown_content: The markdown content to parse
        
    Returns:
        List of parsed JSON objects representing tool calls
    """
    # Pattern to match JSON blocks in markdown
    pattern = r'```json\s*\n(\{(?:[^{}]|{[^{}]*})*\})\s*\n```'
    matches = re.findall(pattern, markdown_content, re.MULTILINE)
    
    json_objects = []
    for match in matches:
        try:
            json_obj = json.loads(match)
            json_objects.append(json_obj)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            continue
    
    return json_objects


def validate_tool_call(tool_call: Dict[str, Any]) -> bool:
    """
    Validate that a tool call has the required structure.
    
    Args:
        tool_call: The tool call to validate
        
    Returns:
        True if valid, False otherwise
    """
    if 'tool_call' not in tool_call:
        return False
    
    tool_data = tool_call['tool_call']
    if not isinstance(tool_data, dict):
        return False
    
    if 'name' not in tool_data:
        return False
    
    return True


def parse_tool_call(json_block: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a JSON block to extract tool call information.
    
    Args:
        json_block: The JSON block to parse
        
    Returns:
        Dictionary with tool name and parameters
    """
    if not validate_tool_call(json_block):
        raise ValueError("Invalid tool call format")
    
    tool_data = json_block['tool_call']
    return {
        'name': tool_data['name'],
        'parameters': tool_data.get('parameters', {})
    }