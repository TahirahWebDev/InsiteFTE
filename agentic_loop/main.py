#!/usr/bin/env python3
"""
Main entry point for the Gold Tier Agentic Loop system.
"""

import asyncio
import signal
import sys
from pathlib import Path
import logging

# Add the project root to the path so we can import modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agentic_loop.agent.core import CoreAgent
from agentic_loop.config import (
    VAULT_PATH,
    INBOX_PATH,
    NEEDS_ACTION_PATH,
    PENDING_APPROVAL_PATH,
    APPROVED_PATH,
    DONE_PATH,
    RESEARCHING_PATH,
    REVIEWING_PATH
)
from agentic_loop.utils.logger import get_logger
from agentic_loop.state_machine.engine import StateMachineEngine
from agentic_loop.state_machine.states import State


class AgenticLoopController:
    """
    Controller for the main agentic loop that monitors the 02_Needs_Action folder.
    """

    def __init__(self):
        """Initialize the agentic loop controller."""
        self.agent = CoreAgent()
        self.state_machine = StateMachineEngine()
        self.logger = get_logger()
        self.running = False

        # Ensure required directories exist
        self._setup_directories()

    def _setup_directories(self):
        """Ensure all required directories exist."""
        required_dirs = [
            INBOX_PATH,
            NEEDS_ACTION_PATH,
            PENDING_APPROVAL_PATH,
            APPROVED_PATH,
            DONE_PATH,
            RESEARCHING_PATH,
            REVIEWING_PATH
        ]

        for directory in required_dirs:
            directory.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Ensured directory exists: {directory}")

    async def start(self):
        """Start the agentic loop."""
        self.logger.info("Starting the Gold Tier Agentic Loop...")
        self.running = True

        # Set up signal handlers for graceful shutdown
        def signal_handler(signum, frame):
            self.logger.info(f"Received signal {signum}, initiating graceful shutdown...")
            self.running = False

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        try:
            # Start the main processing loop
            await self._main_loop()
        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received, shutting down...")
        finally:
            await self.stop()

    async def _main_loop(self):
        """Main processing loop that periodically checks all relevant folders."""
        from .config import POLLING_INTERVAL

        self.logger.info(f"Starting main loop with polling interval: {POLLING_INTERVAL}s")

        while self.running:
            try:
                # Process the needs action folder
                await self._process_needs_action_folder()

                # Process the approved folder (to move files to done)
                await self._process_approved_folder()

                # Wait for the next polling cycle
                for _ in range(POLLING_INTERVAL):
                    if not self.running:
                        break
                    await asyncio.sleep(1)

            except Exception as e:
                self.logger.error(f"Error in main loop: {str(e)}")
                # Continue the loop despite errors
                await asyncio.sleep(min(POLLING_INTERVAL, 10))  # Brief pause before continuing

    async def _process_needs_action_folder(self):
        """Process all files in the needs action folder."""
        self.logger.info(f"Checking {NEEDS_ACTION_PATH} for new tasks...")

        # Get all .txt and .md files in the needs action folder
        task_files = [
            f for f in NEEDS_ACTION_PATH.iterdir()
            if f.is_file() and f.suffix.lower() in ['.txt', '.md']
        ]

        if not task_files:
            self.logger.info("No new tasks found in needs action folder")
            return

        self.logger.info(f"Found {len(task_files)} task(s) to process")

        # Process each task file
        for task_file in task_files:
            try:
                self.logger.info(f"Processing task: {task_file.name}")

                # Use the agent to execute the task
                success = await self.agent.execute_task(str(task_file))

                if success:
                    self.logger.info(f"Successfully processed task: {task_file.name}")
                else:
                    self.logger.error(f"Failed to process task: {task_file.name}")

            except Exception as e:
                self.logger.error(f"Error processing task {task_file.name}: {str(e)}")

    async def _process_approved_folder(self):
        """Process all files in the approved folder to move them to done."""
        self.logger.info(f"Checking {APPROVED_PATH} for approved tasks...")

        # Get all .txt and .md files in the approved folder
        task_files = [
            f for f in APPROVED_PATH.iterdir()
            if f.is_file() and f.suffix.lower() in ['.txt', '.md']
        ]

        if not task_files:
            self.logger.info("No approved tasks found")
            return

        self.logger.info(f"Found {len(task_files)} approved task(s) to finalize")

        # Process each task file
        for task_file in task_files:
            try:
                self.logger.info(f"Moving approved task to done: {task_file.name}")

                # Move the file to the done folder
                success = await self.state_machine.transition_file(str(task_file), State.DONE)

                if success:
                    self.logger.info(f"Successfully moved to done: {task_file.name}")
                else:
                    self.logger.error(f"Failed to move to done: {task_file.name}")

            except Exception as e:
                self.logger.error(f"Error moving approved task {task_file.name} to done: {str(e)}")

    async def stop(self):
        """Stop the agentic loop."""
        self.logger.info("Stopping the agentic loop...")
        self.running = False
        self.logger.info("Agentic loop stopped.")


async def main():
    """Main entry point."""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create and start the controller
    controller = AgenticLoopController()
    await controller.start()


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())