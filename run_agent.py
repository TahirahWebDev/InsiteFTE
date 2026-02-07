"""
Main runner for the Technical Branding Assistant.
Monitors the Needs Action folder and processes files when they appear.
"""

import time
import logging
import sys
from pathlib import Path

from scripts.agent_logic import monitor_and_process_needs_action
from scripts.config import NEEDS_ACTION_PATH, LOG_FILE


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


def main():
    """Main entry point for the Technical Branding Assistant."""
    logger.info("Starting Technical Branding Assistant...")
    
    # Verify the Needs Action folder exists
    if not NEEDS_ACTION_PATH.exists():
        logger.error(f"Needs Action folder does not exist: {NEEDS_ACTION_PATH}")
        return
    
    logger.info(f"Monitoring Needs Action folder: {NEEDS_ACTION_PATH}")
    
    try:
        while True:
            # Process any files in the Needs Action folder
            monitor_and_process_needs_action()
            
            # Wait for a bit before checking again
            time.sleep(10)  # Check every 10 seconds
            
    except KeyboardInterrupt:
        logger.info("Stopping Technical Branding Assistant...")
        print("\nTechnical Branding Assistant stopped.")


if __name__ == "__main__":
    main()