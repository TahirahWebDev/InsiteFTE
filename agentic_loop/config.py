"""
Configuration settings for the Gold Tier Agentic Loop system.
"""

import os
from pathlib import Path

# Path to your Obsidian vault
VAULT_PATH = os.getenv("VAULT_PATH", "")

# If VAULT_PATH is not set in environment, use a default path or raise an error
if not VAULT_PATH:
    # Use the current project directory as default for testing purposes
    VAULT_PATH = "F:\\Tahirah\\Hackathon-0\\AI_Employee_Vault"

VAULT_PATH = Path(VAULT_PATH)

# Folder names (can be customized if needed)
INBOX_FOLDER = "01_Inbox"
NEEDS_ACTION_FOLDER = "02_Needs_Action"
PENDING_APPROVAL_FOLDER = "03_Pending_Approval"
APPROVED_FOLDER = "04_Approved"
DONE_FOLDER = "05_Done"
RESEARCHING_FOLDER = "06_Researching"
REVIEWING_FOLDER = "07_Reviewing"

# Full paths for each folder
INBOX_PATH = VAULT_PATH / INBOX_FOLDER
NEEDS_ACTION_PATH = VAULT_PATH / NEEDS_ACTION_FOLDER
PENDING_APPROVAL_PATH = VAULT_PATH / PENDING_APPROVAL_FOLDER
APPROVED_PATH = VAULT_PATH / APPROVED_FOLDER
DONE_PATH = VAULT_PATH / DONE_FOLDER
RESEARCHING_PATH = VAULT_PATH / RESEARCHING_FOLDER
REVIEWING_PATH = VAULT_PATH / REVIEWING_FOLDER

# Ensure all required folders exist
REQUIRED_FOLDERS = [
    INBOX_PATH,
    NEEDS_ACTION_PATH,
    PENDING_APPROVAL_PATH,
    APPROVED_PATH,
    DONE_PATH,
    RESEARCHING_PATH,
    REVIEWING_PATH
]

# File extensions that the system will process
ALLOWED_EXTENSIONS = {'.txt', '.md'}

# Maximum file size allowed (in bytes) - 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024

# Characters to sanitize from filenames
INVALID_CHARS = '<>:"|?*'

# Log file path
LOG_FILE = "agentic_loop.log"

# Polling interval in seconds (default: 60 seconds)
POLLING_INTERVAL = 60

# Tool execution settings
TOOL_EXECUTION_TIMEOUT = 30  # seconds