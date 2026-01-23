"""
Enhanced logging with safety features for the Gold Tier Agentic Loop system.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path


class SafeLogger:
    """
    Enhanced logging with safety features for the system.
    Includes safety mechanisms and kill switch functionality.
    """
    
    def __init__(self, log_file: str = "agentic_loop.log"):
        """
        Initialize the logger.
        
        Args:
            log_file: The file to log to
        """
        self.logger = logging.getLogger('AgenticLoop')
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent adding multiple handlers if logger already has handlers
        if not self.logger.handlers:
            # Create file handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            
            # Create console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # Add handlers to logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        
        # Kill switch state
        self.kill_switch_engaged = False
    
    def info(self, message: str):
        """
        Log an info message.
        
        Args:
            message: The message to log
        """
        if not self.kill_switch_engaged:
            self.logger.info(message)
    
    def warning(self, message: str):
        """
        Log a warning message.
        
        Args:
            message: The message to log
        """
        if not self.kill_switch_engaged:
            self.logger.warning(message)
    
    def error(self, message: str):
        """
        Log an error message.
        
        Args:
            message: The message to log
        """
        if not self.kill_switch_engaged:
            self.logger.error(message)
    
    def debug(self, message: str):
        """
        Log a debug message.
        
        Args:
            message: The message to log
        """
        if not self.kill_switch_engaged:
            self.logger.debug(message)
    
    def critical(self, message: str):
        """
        Log a critical message.
        
        Args:
            message: The message to log
        """
        # Critical messages are always logged, even if kill switch is engaged
        self.logger.critical(message)
    
    def engage_kill_switch(self):
        """
        Engage the kill switch to stop all non-critical logging.
        """
        self.kill_switch_engaged = True
        self.critical("KILL SWITCH ENGAGED - All non-critical operations halted")
    
    def disengage_kill_switch(self):
        """
        Disengage the kill switch to resume normal logging.
        """
        self.kill_switch_engaged = False
        self.info("KILL SWITCH DISENGAGED - Normal operations resumed")
    
    def is_kill_switch_engaged(self) -> bool:
        """
        Check if the kill switch is engaged.
        
        Returns:
            True if kill switch is engaged, False otherwise
        """
        return self.kill_switch_engaged
    
    def log_api_call(self, endpoint: str, method: str, status_code: int, response_time: float):
        """
        Log an API call with safety features.
        
        Args:
            endpoint: The API endpoint
            method: The HTTP method
            status_code: The response status code
            response_time: The response time in seconds
        """
        if not self.kill_switch_engaged:
            self.logger.info(f"API CALL: {method} {endpoint} - Status: {status_code}, Time: {response_time}s")
    
    def log_tool_execution(self, tool_name: str, parameters: dict, result: str, status: str):
        """
        Log a tool execution with safety features.
        
        Args:
            tool_name: The name of the tool
            parameters: The parameters passed to the tool
            result: The result of the tool execution
            status: The status of the execution ('success' or 'failure')
        """
        if not self.kill_switch_engaged:
            self.logger.info(f"TOOL EXECUTION: {tool_name} - Status: {status}")


# Global logger instance
logger_instance = None


def get_logger(log_file: str = "agentic_loop.log") -> SafeLogger:
    """
    Get the global logger instance, creating it if it doesn't exist.
    
    Args:
        log_file: The file to log to
        
    Returns:
        The logger instance
    """
    global logger_instance
    if logger_instance is None:
        logger_instance = SafeLogger(log_file)
    return logger_instance