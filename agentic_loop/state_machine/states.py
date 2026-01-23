"""
State definitions for the Gold Tier Agentic Loop system.
"""

from enum import Enum


class State(Enum):
    """
    Enumeration of all possible states in the system.
    """
    INBOX = "01_Inbox"
    NEEDS_ACTION = "02_Needs_Action"
    PENDING_APPROVAL = "03_Pending_Approval"
    APPROVED = "04_Approved"
    DONE = "05_Done"
    RESEARCHING = "06_Researching"
    REVIEWING = "07_Reviewing"


class StateTransition:
    """
    Defines valid transitions between states.
    """
    
    # Define valid state transitions
    VALID_TRANSITIONS = {
        State.INBOX: [State.NEEDS_ACTION],
        State.NEEDS_ACTION: [State.RESEARCHING, State.PENDING_APPROVAL],
        State.RESEARCHING: [State.REVIEWING],
        State.REVIEWING: [State.PENDING_APPROVAL],
        State.PENDING_APPROVAL: [State.APPROVED],
        State.APPROVED: [State.DONE],
        State.DONE: []  # Terminal state
    }
    
    @classmethod
    def is_valid_transition(cls, from_state: State, to_state: State) -> bool:
        """
        Check if a transition from one state to another is valid.
        
        Args:
            from_state: The current state
            to_state: The target state
            
        Returns:
            True if the transition is valid, False otherwise
        """
        if from_state in cls.VALID_TRANSITIONS:
            return to_state in cls.VALID_TRANSITIONS[from_state]
        return False
    
    @classmethod
    def get_allowed_transitions(cls, from_state: State) -> list:
        """
        Get all allowed transitions from a given state.
        
        Args:
            from_state: The current state
            
        Returns:
            List of allowed next states
        """
        return cls.VALID_TRANSITIONS.get(from_state, [])