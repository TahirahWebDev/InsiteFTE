"""
Combined runner for both the file watcher and the Technical Branding Assistant.
"""

import threading
import time
import logging
import sys
from pathlib import Path

from scripts.watcher import main as watcher_main
from scripts.agent_logic import monitor_and_process_needs_action
from scripts.config import NEEDS_ACTION_PATH, LOG_FILE
import logging


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


def agent_worker():
    """Worker function for the agent logic."""
    logger.info("Technical Branding Agent started...")
    try:
        while True:
            # Process any files in the Needs Action folder
            monitor_and_process_needs_action()
            
            # Wait for a bit before checking again
            time.sleep(10)  # Check every 10 seconds
            
    except KeyboardInterrupt:
        logger.info("Stopping Technical Branding Agent...")


def main():
    """Main entry point for the combined runner."""
    logger.info("Starting combined Technical Branding Assistant...")
    
    # Start the agent in a separate thread
    agent_thread = threading.Thread(target=agent_worker, daemon=True)
    agent_thread.start()
    
    logger.info("Both watcher and agent are running...")
    logger.info("Press Ctrl+C to stop.")
    
    try:
        # Run the watcher in the main thread
        watcher_main()
    except KeyboardInterrupt:
        logger.info("Stopping combined runner...")
        print("\nCombined runner stopped.")


if __name__ == "__main__":
    main()