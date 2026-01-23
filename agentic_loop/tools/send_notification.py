"""
Send notification tool for the Gold Tier Agentic Loop system.
"""

import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
from .base_tool import BaseTool


class SendNotificationTool(BaseTool):
    """
    Tool for sending notifications to users.
    """
    
    def __init__(self):
        super().__init__(
            name="send_notification",
            description="Send notifications to users via email or other methods"
        )
    
    async def execute(self, recipient: str, subject: str, body: str, method: str = "email") -> Dict[str, Any]:
        """
        Execute the notification sending.
        
        Args:
            recipient: The recipient of the notification
            subject: The subject of the notification
            body: The content of the notification
            method: The method to use ("email", "slack", "discord") - default is "email"
            
        Returns:
            Dictionary with success status and message ID
        """
        print(f"Sending notification to: {recipient} via {method}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        
        # Simulate sending delay
        await asyncio.sleep(0.5)
        
        # In a real implementation, we would send the actual notification
        # For this example, we'll return a mock success response
        result = {
            "success": True,
            "message_id": f"mock_msg_{hash(recipient + subject + body) % 10000}",
            "method": method,
            "recipient": recipient
        }
        
        return result
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """
        Validate the parameters for sending a notification.
        
        Args:
            parameters: The parameters to validate
            
        Returns:
            True if parameters are valid, False otherwise
        """
        required_params = ['recipient', 'subject', 'body']
        for param in required_params:
            if param not in parameters:
                return False
        
        recipient = parameters['recipient']
        subject = parameters['subject']
        body = parameters['body']
        
        # Validate that required parameters are strings and not empty
        if not isinstance(recipient, str) or len(recipient.strip()) == 0:
            return False
        if not isinstance(subject, str) or len(subject.strip()) == 0:
            return False
        if not isinstance(body, str) or len(body.strip()) == 0:
            return False
        
        # Validate method if provided
        if 'method' in parameters:
            method = parameters['method']
            if not isinstance(method, str) or method not in ["email", "slack", "discord"]:
                return False
        
        return True