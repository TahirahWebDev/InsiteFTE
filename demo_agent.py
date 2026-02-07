"""
Demonstration script showing how to run the Technical Branding Assistant workflow.
"""

import time
from scripts.agent_logic import process_needs_action_file
from scripts.config import NEEDS_ACTION_PATH, PENDING_APPROVAL_PATH
import shutil
from pathlib import Path


def demo_workflow():
    print("Technical Branding Assistant Demo")
    print("=" * 40)
    
    # Show the current state of folders
    print(f"Inbox contains: {len(list((Path('.') / '01_Inbox').glob('*')))} files")
    print(f"Needs Action contains: {len(list(NEEDS_ACTION_PATH.glob('*')))} files")
    print(f"Pending Approval contains: {len(list(PENDING_APPROVAL_PATH.glob('*')))} files")
    
    # Check if there are any files in Needs Action to process
    needs_action_files = list(NEEDS_ACTION_PATH.glob("*.txt"))
    needs_action_files.extend(list(NEEDS_ACTION_PATH.glob("*.md")))
    
    if needs_action_files:
        print(f"\nFound {len(needs_action_files)} file(s) in Needs Action to process:")
        for file_path in needs_action_files:
            print(f"  - {file_path.name}")
            
        print("\nProcessing files...")
        for file_path in needs_action_files:
            print(f"Processing: {file_path.name}")
            success = process_needs_action_file(str(file_path))
            if success:
                print(f"  ✓ Successfully processed {file_path.name}")
            else:
                print(f"  ✗ Failed to process {file_path.name}")
    else:
        print("\nNo files found in Needs Action folder.")
        print("Tip: Add a text file with a tech topic to the 01_Inbox folder,")
        print("then run the watcher.py script to move it to Needs Action.")
    
    # Show the final state
    print(f"\nFinal state:")
    print(f"Needs Action contains: {len(list(NEEDS_ACTION_PATH.glob('*')))} files")
    print(f"Pending Approval contains: {len(list(PENDING_APPROVAL_PATH.glob('*')))} files")
    
    pending_files = list(PENDING_APPROVAL_PATH.glob("*.md"))
    if pending_files:
        print("\nFiles created in Pending Approval:")
        for file_path in pending_files:
            print(f"  - {file_path.name}")


if __name__ == "__main__":
    demo_workflow()