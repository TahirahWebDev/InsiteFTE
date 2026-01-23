"""
Base tool class for the Gold Tier Agentic Loop system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """
    Abstract base class for all tools in the system.
    All tools should inherit from this class and implement the execute method.
    """
    
    def __init__(self, name: str, description: str):
        """
        Initialize the tool with a name and description.
        
        Args:
            name: The name of the tool
            description: A description of what the tool does
        """
        self.name = name
        self.description = description
    
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """
        Execute the tool with the provided parameters.
        
        Args:
            **kwargs: Parameters for the tool execution
            
        Returns:
            The result of the tool execution
        """
        pass
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """
        Validate the parameters for the tool execution.
        Override this method in subclasses to implement specific validation.
        
        Args:
            parameters: The parameters to validate
            
        Returns:
            True if parameters are valid, False otherwise
        """
        # Default implementation - always return True
        # Subclasses should override this to implement specific validation
        return True