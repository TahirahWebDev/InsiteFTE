"""
State machine engine for the Gold Tier Agentic Loop system.
"""

import asyncio
from pathlib import Path
from typing import Dict, Any
from .states import State, StateTransition
from ..utils.file_operations import move_file, add_yaml_frontmatter
from ..utils.logger import get_logger


class StateMachineEngine:
    """
    Engine that manages state transitions for task files.
    """
    
    def __init__(self):
        """Initialize the state machine engine."""
        self.logger = get_logger()
    
    async def transition_file(self, file_path: str, target_state: State) -> bool:
        """
        Transition a file to a new state.
        
        Args:
            file_path: Path to the file to transition
            target_state: The target state to transition to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get the current state from the file path
            current_state = self.get_state_from_path(file_path)
            
            # Validate the transition
            if not StateTransition.is_valid_transition(current_state, target_state):
                self.logger.error(f"Invalid state transition from {current_state.value} to {target_state.value} for file {file_path}")
                return False
            
            # Determine the target folder path
            from ..config import (
                INBOX_PATH, NEEDS_ACTION_PATH, PENDING_APPROVAL_PATH,
                APPROVED_PATH, DONE_PATH, RESEARCHING_PATH, REVIEWING_PATH
            )
            
            target_paths = {
                State.INBOX: INBOX_PATH,
                State.NEEDS_ACTION: NEEDS_ACTION_PATH,
                State.PENDING_APPROVAL: PENDING_APPROVAL_PATH,
                State.APPROVED: APPROVED_PATH,
                State.DONE: DONE_PATH,
                State.RESEARCHING: RESEARCHING_PATH,
                State.REVIEWING: REVIEWING_PATH
            }
            
            target_folder = target_paths[target_state]
            
            # Update the file's metadata to reflect the new state
            metadata = {"status": target_state.value.lower().replace('-', '_')}
            success = add_yaml_frontmatter(file_path, metadata, preserve_content=True)
            
            if not success:
                self.logger.error(f"Failed to update metadata for file {file_path}")
                return False
            
            # Move the file to the appropriate folder
            file_name = Path(file_path).name
            target_file_path = target_folder / file_name
            
            move_success = move_file(file_path, target_file_path)
            
            if move_success:
                self.logger.info(f"Successfully transitioned file {file_name} from {current_state.value} to {target_state.value}")
                return True
            else:
                self.logger.error(f"Failed to move file {file_path} to {target_file_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error transitioning file {file_path} to {target_state.value}: {str(e)}")
            return False
    
    def get_state_from_path(self, file_path: str) -> State:
        """
        Determine the current state of a file based on its path.
        
        Args:
            file_path: Path to the file
            
        Returns:
            The current state of the file
        """
        path = Path(file_path)
        
        # Map folder names to states
        folder_to_state = {
            "01_Inbox": State.INBOX,
            "02_Needs_Action": State.NEEDS_ACTION,
            "03_Pending_Approval": State.PENDING_APPROVAL,
            "04_Approved": State.APPROVED,
            "05_Done": State.DONE,
            "06_Researching": State.RESEARCHING,
            "07_Reviewing": State.REVIEWING
        }
        
        # Check parent directory name to determine state
        parent_dir = path.parent.name
        return folder_to_state.get(parent_dir, State.INBOX)  # Default to INBOX if unknown
    
    async def get_allowed_transitions(self, file_path: str) -> list:
        """
        Get all allowed transitions for a file in its current state.
        
        Args:
            file_path: Path to the file
            
        Returns:
            List of allowed next states
        """
        current_state = self.get_state_from_path(file_path)
        return StateTransition.get_allowed_transitions(current_state)
    
    async def process_file(self, file_path: str) -> bool:
        """
        Process a file based on its current state and determine next action.
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            True if processing was successful, False otherwise
        """
        current_state = self.get_state_from_path(file_path)
        self.logger.info(f"Processing file {Path(file_path).name} in state {current_state.value}")
        
        # Depending on the current state, determine what action to take
        if current_state == State.INBOX:
            # Move to Needs Action
            return await self.transition_file(file_path, State.NEEDS_ACTION)
        elif current_state == State.NEEDS_ACTION:
            # This is where the AI would analyze the task and decide next state
            # For now, we'll just move to PENDING_APPROVAL as an example
            # In a real implementation, this would involve AI decision-making
            return await self.transition_file(file_path, State.PENDING_APPROVAL)
        elif current_state == State.RESEARCHING:
            # After research is complete, move to REVIEWING
            return await self.transition_file(file_path, State.REVIEWING)
        elif current_state == State.REVIEWING:
            # After review is complete, move to PENDING_APPROVAL
            return await self.transition_file(file_path, State.PENDING_APPROVAL)
        elif current_state == State.PENDING_APPROVAL:
            # After approval, move to APPROVED
            # In a real system, this would wait for human approval
            return await self.transition_file(file_path, State.APPROVED)
        elif current_state == State.APPROVED:
            # After finalization, move to DONE
            return await self.transition_file(file_path, State.DONE)
        else:
            # For DONE state or any other state, no further action
            return True