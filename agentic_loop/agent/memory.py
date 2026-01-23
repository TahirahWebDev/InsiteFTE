"""
Memory management system for the Gold Tier Agentic Loop system.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from ..utils.logger import get_logger


class MemoryManager:
    """
    Component that manages long-term memory for the AI agent.
    Maintains a Memory.md file to track long-term goals across different tasks.
    """
    
    def __init__(self, memory_file_path: str = "../memory/Memory.md"):
        """Initialize the memory manager."""
        self.memory_file_path = Path(memory_file_path)
        self.logger = get_logger()
        
        # Ensure the memory file exists
        self._initialize_memory_file()
    
    def _initialize_memory_file(self):
        """Initialize the memory file if it doesn't exist."""
        if not self.memory_file_path.exists():
            # Create the memory directory if it doesn't exist
            self.memory_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create an initial memory file with basic structure
            initial_content = f"""# Memory File for AI Agent

**Created**: {datetime.now().isoformat()}

## Categories
- Goals
- Facts
- Patterns
- Preferences

## Recent Memories
None yet.

"""
            with open(self.memory_file_path, 'w', encoding='utf-8') as f:
                f.write(initial_content)
            
            self.logger.info(f"Initialized memory file at {self.memory_file_path}")
    
    async def add_memory(self, category: str, content: str, tags: List[str] = None) -> bool:
        """
        Add a new memory entry to the memory file.
        
        Args:
            category: The category of the memory (e.g., 'goal', 'fact', 'pattern')
            content: The content of the memory
            tags: Optional list of tags for categorization and retrieval
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create the memory entry
            memory_entry = {
                "id": f"mem_{int(datetime.now().timestamp())}_{hash(content) % 10000}",
                "timestamp": datetime.now().isoformat(),
                "category": category,
                "content": content,
                "relevance_score": 1.0,  # New memories are highly relevant initially
                "tags": tags or []
            }
            
            # Read the current memory file content
            with open(self.memory_file_path, 'r', encoding='utf-8') as f:
                current_content = f.read()
            
            # Add the new memory entry to the content
            new_entry_text = f"\n### {memory_entry['id']}\n"
            new_entry_text += f"- **Category**: {category}\n"
            new_entry_text += f"- **Timestamp**: {memory_entry['timestamp']}\n"
            new_entry_text += f"- **Content**: {content}\n"
            if tags:
                new_entry_text += f"- **Tags**: {', '.join(tags)}\n"
            new_entry_text += f"- **Relevance**: {memory_entry['relevance_score']}\n\n"
            
            # Write the updated content back to the file
            with open(self.memory_file_path, 'w', encoding='utf-8') as f:
                f.write(current_content + new_entry_text)
            
            self.logger.info(f"Added new memory entry: {memory_entry['id']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding memory entry: {str(e)}")
            return False
    
    async def retrieve_memories(self, category: str = None, tags: List[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve memories based on category and/or tags.
        
        Args:
            category: Optional category to filter by
            tags: Optional list of tags to filter by (memories with any of these tags will be returned)
            limit: Maximum number of memories to return (default 10)
            
        Returns:
            List of memory entries matching the criteria
        """
        try:
            memories = []
            
            # Read the memory file
            with open(self.memory_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the memory entries from the file
            # This is a simplified parser - in a real implementation, you might use a more robust approach
            lines = content.split('\n')
            current_entry = None
            
            for line in lines:
                if line.startswith('### mem_'):  # Start of a new memory entry
                    if current_entry is not None:
                        memories.append(current_entry)
                    
                    # Extract the ID from the header
                    entry_id = line[4:].strip()  # Remove '### ' prefix
                    current_entry = {"id": entry_id}
                
                elif current_entry is not None and line.startswith('- **Category**:'):
                    current_entry["category"] = line.split(':', 1)[1].strip()
                
                elif current_entry is not None and line.startswith('- **Timestamp**:'):
                    current_entry["timestamp"] = line.split(':', 1)[1].strip()
                
                elif current_entry is not None and line.startswith('- **Content**:'):
                    current_entry["content"] = line.split(':', 1)[1].strip()
                
                elif current_entry is not None and line.startswith('- **Tags**:'):
                    tag_str = line.split(':', 1)[1].strip()
                    current_entry["tags"] = [tag.strip() for tag in tag_str.split(',')]
                
                elif current_entry is not None and line.startswith('- **Relevance**:'):
                    relevance_str = line.split(':', 1)[1].strip()
                    current_entry["relevance_score"] = float(relevance_str)
            
            # Add the last entry if it exists
            if current_entry is not None:
                memories.append(current_entry)
            
            # Filter memories based on criteria
            filtered_memories = []
            for memory in memories:
                # Check category if specified
                if category and memory.get("category", "").lower() != category.lower():
                    continue
                
                # Check tags if specified
                if tags:
                    memory_tags = [t.lower() for t in memory.get("tags", [])]
                    if not any(tag.lower() in memory_tags for tag in tags):
                        continue
                
                filtered_memories.append(memory)
            
            # Sort by relevance score (descending) and return limited results
            sorted_memories = sorted(filtered_memories, 
                                   key=lambda x: x.get("relevance_score", 0), 
                                   reverse=True)
            
            result = sorted_memories[:limit]
            self.logger.info(f"Retrieved {len(result)} memories matching criteria")
            return result
            
        except Exception as e:
            self.logger.error(f"Error retrieving memories: {str(e)}")
            return []
    
    async def update_memory_relevance(self, memory_id: str, relevance_score: float) -> bool:
        """
        Update the relevance score of a specific memory.
        
        Args:
            memory_id: The ID of the memory to update
            relevance_score: The new relevance score (0.0 to 1.0)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read the current memory file content
            with open(self.memory_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Find and update the relevance score for the specified memory
            updated_lines = []
            in_target_memory = False
            relevance_updated = False
            
            for line in lines:
                if line.startswith(f'### {memory_id}'):
                    in_target_memory = True
                    updated_lines.append(line)
                elif in_target_memory and line.startswith('- **Relevance**:'):
                    updated_lines.append(f'- **Relevance**: {relevance_score}\n')
                    in_target_memory = False  # Reset after updating relevance
                    relevance_updated = True
                elif in_target_memory and line.startswith('### ') and not line.startswith(f'### {memory_id}'):
                    # We've moved to a different memory entry, reset the flag
                    in_target_memory = False
                    updated_lines.append(line)
                else:
                    updated_lines.append(line)
            
            # Write the updated content back to the file
            with open(self.memory_file_path, 'w', encoding='utf-8') as f:
                f.writelines(updated_lines)
            
            if relevance_updated:
                self.logger.info(f"Updated relevance score for memory {memory_id} to {relevance_score}")
                return True
            else:
                self.logger.warning(f"Memory {memory_id} not found for relevance update")
                return False
                
        except Exception as e:
            self.logger.error(f"Error updating memory relevance: {str(e)}")
            return False
    
    async def search_memories(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search memories for content matching the query.
        
        Args:
            query: The search query
            limit: Maximum number of results to return
            
        Returns:
            List of memory entries matching the query
        """
        try:
            # Retrieve all memories
            all_memories = await self.retrieve_memories(limit=1000)  # Large limit to search all
            
            # Filter memories based on query match in content
            matching_memories = []
            query_lower = query.lower()
            
            for memory in all_memories:
                content = memory.get("content", "").lower()
                category = memory.get("category", "").lower()
                
                # Calculate a simple relevance score based on query matches
                relevance_score = 0
                if query_lower in content:
                    relevance_score += 1
                if query_lower in category:
                    relevance_score += 0.5  # Lower weight for category matches
                
                # Also check tags
                tags = memory.get("tags", [])
                for tag in tags:
                    if query_lower in tag.lower():
                        relevance_score += 0.3  # Lower weight for tag matches
                
                if relevance_score > 0:
                    memory["search_relevance"] = relevance_score
                    matching_memories.append(memory)
            
            # Sort by search relevance and return limited results
            sorted_memories = sorted(matching_memories, 
                                   key=lambda x: x.get("search_relevance", 0), 
                                   reverse=True)
            
            result = sorted_memories[:limit]
            self.logger.info(f"Found {len(result)} memories matching query '{query}'")
            return result
            
        except Exception as e:
            self.logger.error(f"Error searching memories: {str(e)}")
            return []
    
    async def get_highlights(self) -> List[str]:
        """
        Get highlights from the memory file for dashboard display.
        
        Returns:
            List of highlight strings
        """
        try:
            highlights = []
            
            # Retrieve recent memories
            recent_memories = await self.retrieve_memories(limit=5)
            
            for memory in recent_memories:
                content = memory.get("content", "")
                if len(content) > 100:
                    content_preview = content[:100] + "..."
                else:
                    content_preview = content
                highlights.append(f"{memory['id']}: {content_preview}")
            
            return highlights
            
        except Exception as e:
            self.logger.error(f"Error getting memory highlights: {str(e)}")
            return []