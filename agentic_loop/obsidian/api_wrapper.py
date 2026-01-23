"""
Obsidian API wrapper for the Gold Tier Agentic Loop system.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from ..utils.logger import get_logger


class ObsidianAPIWrapper:
    """
    Wrapper for interacting with Obsidian's API and file system.
    """

    def __init__(self, vault_path: str):
        """
        Initialize the Obsidian API wrapper.

        Args:
            vault_path: Path to the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.logger = get_logger()
        
        # Verify vault path exists
        if not self.vault_path.exists():
            raise ValueError(f"Vault path does not exist: {vault_path}")

    async def read_note(self, note_path: str) -> Optional[str]:
        """
        Read the content of a note from the vault.

        Args:
            note_path: Path to the note relative to vault root

        Returns:
            Content of the note or None if not found
        """
        full_path = self.vault_path / note_path
        
        try:
            if full_path.exists():
                content = full_path.read_text(encoding='utf-8')
                self.logger.info(f"Read note: {note_path}")
                return content
            else:
                self.logger.warning(f"Note not found: {note_path}")
                return None
        except Exception as e:
            self.logger.error(f"Error reading note {note_path}: {str(e)}")
            return None

    async def write_note(self, note_path: str, content: str, append: bool = False) -> bool:
        """
        Write content to a note in the vault.

        Args:
            note_path: Path to the note relative to vault root
            content: Content to write to the note
            append: Whether to append to existing content (default: False)

        Returns:
            True if successful, False otherwise
        """
        full_path = self.vault_path / note_path
        
        try:
            # Ensure parent directory exists
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            mode = 'a' if append else 'w'
            with open(full_path, mode, encoding='utf-8') as f:
                f.write(content)
            
            action = "Appended to" if append else "Wrote to"
            self.logger.info(f"{action} note: {note_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error writing note {note_path}: {str(e)}")
            return False

    async def update_yaml_frontmatter(self, note_path: str, metadata: Dict[str, Any]) -> bool:
        """
        Update the YAML frontmatter of a note.

        Args:
            note_path: Path to the note relative to vault root
            metadata: Dictionary of metadata to update

        Returns:
            True if successful, False otherwise
        """
        content = await self.read_note(note_path)
        if content is None:
            return False

        try:
            # Import ruamel.yaml here to avoid dependency issues if not installed
            from ruamel.yaml import YAML
            
            yaml = YAML()
            yaml.preserve_quotes = True
            
            # Split content into frontmatter and body
            lines = content.split('\n')
            frontmatter_start_idx = -1
            frontmatter_end_idx = -1
            
            for i, line in enumerate(lines):
                if line.strip() == '---':
                    if frontmatter_start_idx == -1:
                        frontmatter_start_idx = i
                    elif frontmatter_end_idx == -1:
                        frontmatter_end_idx = i
                        break
            
            if frontmatter_start_idx != -1 and frontmatter_end_idx != -1:
                # Extract frontmatter
                frontmatter_str = '\n'.join(lines[frontmatter_start_idx + 1:frontmatter_end_idx])
                
                # Parse existing frontmatter
                existing_frontmatter = yaml.load(frontmatter_str) or {}
                
                # Update with new metadata
                existing_frontmatter.update(metadata)
                
                # Reconstruct the content
                before_frontmatter = '\n'.join(lines[:frontmatter_start_idx])
                after_frontmatter = '\n'.join(lines[frontmatter_end_idx + 1:])
                
                # Create new frontmatter string
                import io
                stream = io.StringIO()
                yaml.dump(existing_frontmatter, stream)
                new_frontmatter_str = stream.getvalue().strip()
                
                new_content = f"{before_frontmatter}\n---\n{new_frontmatter_str}\n---\n{after_frontmatter}"
            else:
                # No existing frontmatter, create new one
                import io
                yaml = YAML()
                yaml.preserve_quotes = True
                stream = io.StringIO()
                yaml.dump(metadata, stream)
                frontmatter_str = stream.getvalue().strip()
                
                new_content = f"---\n{frontmatter_str}\n---\n{content}"
            
            # Write the updated content back
            return await self.write_note(note_path, new_content)
        except ImportError:
            self.logger.error("ruamel.yaml not available, cannot update YAML frontmatter")
            return False
        except Exception as e:
            self.logger.error(f"Error updating YAML frontmatter for {note_path}: {str(e)}")
            return False

    async def search_notes_by_tag(self, tag: str) -> List[str]:
        """
        Search for notes that contain a specific tag.

        Args:
            tag: Tag to search for (without # symbol)

        Returns:
            List of note paths that contain the tag
        """
        results = []
        
        # Walk through all markdown files in the vault
        for md_file in self.vault_path.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
                if f"#{tag}" in content or f"# {tag}" in content or f"#{tag} " in content:
                    # Return path relative to vault root
                    relative_path = md_file.relative_to(self.vault_path)
                    results.append(str(relative_path))
            except Exception as e:
                self.logger.warning(f"Could not read file {md_file}: {str(e)}")
        
        self.logger.info(f"Found {len(results)} notes with tag #{tag}")
        return results

    async def get_all_notes_in_folder(self, folder_path: str) -> List[str]:
        """
        Get all note paths in a specific folder.

        Args:
            folder_path: Path to the folder relative to vault root

        Returns:
            List of note paths in the folder
        """
        folder_full_path = self.vault_path / folder_path
        results = []
        
        if folder_full_path.exists() and folder_full_path.is_dir():
            for md_file in folder_full_path.rglob("*.md"):
                relative_path = md_file.relative_to(self.vault_path)
                results.append(str(relative_path))
        
        self.logger.info(f"Found {len(results)} notes in folder: {folder_path}")
        return results