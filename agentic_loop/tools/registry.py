"""
Tool registry and executor for the Gold Tier Agentic Loop system.
"""

import asyncio
from typing import Dict, Callable, Any, Awaitable
from .base_tool import BaseTool


class ToolRegistry:
    """
    Registry and executor for tools in the system.
    Manages registration of tools and their execution.
    """
    
    def __init__(self):
        """Initialize the tool registry."""
        self.tools: Dict[str, BaseTool] = {}
        self.execution_log = []
    
    def register_tool(self, tool: BaseTool):
        """
        Register a tool in the registry.
        
        Args:
            tool: The tool to register
        """
        self.tools[tool.name] = tool
        print(f"Registered tool: {tool.name}")
    
    def get_tool(self, name: str) -> BaseTool:
        """
        Get a tool by name.
        
        Args:
            name: The name of the tool to retrieve
            
        Returns:
            The tool instance
            
        Raises:
            KeyError: If the tool is not found
        """
        if name not in self.tools:
            raise KeyError(f"Tool '{name}' not found in registry")
        return self.tools[name]
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any] = None) -> Any:
        """
        Execute a tool with the provided parameters.
        
        Args:
            tool_name: The name of the tool to execute
            parameters: Parameters for the tool execution (optional)
            
        Returns:
            The result of the tool execution
        """
        if parameters is None:
            parameters = {}
        
        try:
            # Get the tool from the registry
            tool = self.get_tool(tool_name)
            
            # Validate parameters
            if not tool.validate_parameters(parameters):
                raise ValueError(f"Invalid parameters for tool '{tool_name}'")
            
            # Execute the tool
            result = await tool.execute(**parameters)
            
            # Log the execution
            execution_record = {
                'tool_name': tool_name,
                'parameters': parameters,
                'result': result,
                'status': 'success',
                'timestamp': asyncio.get_event_loop().time()
            }
            self.execution_log.append(execution_record)
            
            return result
        except Exception as e:
            # Log the error
            error_record = {
                'tool_name': tool_name,
                'parameters': parameters,
                'error': str(e),
                'status': 'failed',
                'timestamp': asyncio.get_event_loop().time()
            }
            self.execution_log.append(error_record)
            
            # Re-raise the exception
            raise e
    
    def list_tools(self) -> list:
        """
        List all registered tools.
        
        Returns:
            A list of tool names
        """
        return list(self.tools.keys())
    
    def get_execution_log(self) -> list:
        """
        Get the execution log.
        
        Returns:
            A list of execution records
        """
        return self.execution_log[:]