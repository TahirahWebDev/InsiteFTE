"""
Main file monitoring script for the Digital FTE Automation system.
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import Optional

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .config import (
    INBOX_PATH, 
    NEEDS_ACTION_PATH, 
    PENDING_APPROVAL_PATH, 
    APPROVED_PATH, 
    DONE_PATH,
    ALLOWED_EXTENSIONS,
    LOG_FILE
)
from .utils.file_handler import move_file, is_valid_file_type
from .utils.sanitizer import sanitize_filename, handle_duplicate_filename
from .utils.metadata import add_yaml_frontmatter, update_yaml_frontmatter
from .exceptions import FileProcessingError, ConfigurationError


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class InboxHandler(FileSystemEventHandler):
    """Handles file creation events in the Inbox folder."""
    
    def on_created(self, event):
        """Called when a file is created in the monitored directory."""
        if not event.is_directory and event.src_path.endswith(('.txt', '.md')):
            logger.info(f"New file detected: {event.src_path}")
            try:
                process_inbox_file(event.src_path)
            except Exception as e:
                logger.error(f"Error processing file {event.src_path}: {str(e)}")


def process_inbox_file(file_path: str) -> bool:
    """
    Process a file from the inbox: sanitize, add metadata, and move to needs action.
    
    Args:
        file_path: Path to the file in the inbox
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate file type
        if not is_valid_file_type(file_path):
            logger.warning(f"Invalid file type: {file_path}")
            return False
        
        # Sanitize the filename
        original_path = Path(file_path)
        sanitized_name = sanitize_filename(original_path.name)
        sanitized_path = original_path.with_name(sanitized_name)
        
        # Handle potential duplicate filenames
        unique_path = handle_duplicate_filename(str(sanitized_path))
        
        # If we had to change the filename, move it first
        if str(original_path) != unique_path:
            move_file(original_path, unique_path)
            file_path = unique_path
        
        # Add YAML frontmatter with initial metadata
        initial_metadata = {
            'status': 'needs-action',
            'original_filename': original_path.name
        }
        
        if not add_yaml_frontmatter(file_path, initial_metadata):
            logger.error(f"Failed to add metadata to {file_path}")
            return False
        
        # Move the file to the Needs Action folder
        target_path = NEEDS_ACTION_PATH / Path(file_path).name
        if move_file(file_path, target_path):
            logger.info(f"Successfully moved {file_path} to {target_path}")
            return True
        else:
            logger.error(f"Failed to move {file_path} to {target_path}")
            return False
            
    except Exception as e:
        logger.error(f"Error processing inbox file {file_path}: {str(e)}")
        raise FileProcessingError(f"Failed to process inbox file: {str(e)}")


def update_file_status(file_path: str, new_status: str) -> bool:
    """
    Update the status of a file in its YAML frontmatter.
    
    Args:
        file_path: Path to the file
        new_status: The new status value
        
    Returns:
        bool: True if successful, False otherwise
    """
    updates = {'status': new_status}
    return update_yaml_frontmatter(file_path, updates)


def move_to_pending_approval(file_path: str) -> bool:
    """
    Move a file to the pending approval folder and update its status.
    
    Args:
        file_path: Path to the file
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Update status to pending approval
    if not update_file_status(file_path, 'pending-approval'):
        logger.error(f"Failed to update status for {file_path}")
        return False
    
    # Move to pending approval folder
    target_path = PENDING_APPROVAL_PATH / Path(file_path).name
    if move_file(file_path, target_path):
        logger.info(f"Moved {file_path} to pending approval: {target_path}")
        return True
    else:
        logger.error(f"Failed to move {file_path} to pending approval folder")
        return False


def move_to_approved(file_path: str) -> bool:
    """
    Move a file to the approved folder and update its status.
    
    Args:
        file_path: Path to the file
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Update status to approved
    if not update_file_status(file_path, 'approved'):
        logger.error(f"Failed to update status for {file_path}")
        return False
    
    # Move to approved folder
    target_path = APPROVED_PATH / Path(file_path).name
    if move_file(file_path, target_path):
        logger.info(f"Moved {file_path} to approved: {target_path}")
        return True
    else:
        logger.error(f"Failed to move {file_path} to approved folder")
        return False


def move_to_done(file_path: str) -> bool:
    """
    Move a file to the done folder and update its status.
    
    Args:
        file_path: Path to the file
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Update status to done
    if not update_file_status(file_path, 'done'):
        logger.error(f"Failed to update status for {file_path}")
        return False
    
    # Move to done folder
    target_path = DONE_PATH / Path(file_path).name
    if move_file(file_path, target_path):
        logger.info(f"Moved {file_path} to done: {target_path}")
        return True
    else:
        logger.error(f"Failed to move {file_path} to done folder")
        return False


def main():
    """Main entry point for the file watcher."""
    # Verify required folders exist
    for folder in [INBOX_PATH, NEEDS_ACTION_PATH, PENDING_APPROVAL_PATH, APPROVED_PATH, DONE_PATH]:
        if not folder.exists():
            try:
                folder.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created folder: {folder}")
            except Exception as e:
                logger.error(f"Failed to create folder {folder}: {str(e)}")
                raise ConfigurationError(f"Required folder does not exist and could not be created: {folder}")
    
    # Create the event handler and observer
    event_handler = InboxHandler()
    observer = Observer()
    observer.schedule(event_handler, str(INBOX_PATH), recursive=False)
    
    # Start the observer
    observer.start()
    logger.info(f"Started watching inbox folder: {INBOX_PATH}")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping file watcher...")
        observer.stop()
    
    observer.join()
    logger.info("File watcher stopped.")


if __name__ == "__main__":
    main()