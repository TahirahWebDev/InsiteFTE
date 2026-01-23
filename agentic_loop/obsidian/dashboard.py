"""
Mission Control dashboard updates for the Gold Tier Agentic Loop system.
"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from ..utils.logger import get_logger
from .api_wrapper import ObsidianAPIWrapper


class DashboardUpdater:
    """
    Component for updating the Mission Control dashboard in Obsidian.
    """

    def __init__(self, obsidian_api: ObsidianAPIWrapper):
        """
        Initialize the dashboard updater.

        Args:
            obsidian_api: Instance of ObsidianAPIWrapper
        """
        self.api = obsidian_api
        self.logger = get_logger()
        self.dashboard_path = "Home.md"  # Default dashboard path

    async def update_dashboard(self) -> bool:
        """
        Update the main dashboard with current system status.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get current status information
            status_info = await self._get_system_status()
            
            # Generate dashboard content
            dashboard_content = self._generate_dashboard_content(status_info)
            
            # Write to the dashboard file
            success = await self.api.write_note(self.dashboard_path, dashboard_content)
            
            if success:
                self.logger.info("Dashboard updated successfully")
            else:
                self.logger.error("Failed to update dashboard")
            
            return success
        except Exception as e:
            self.logger.error(f"Error updating dashboard: {str(e)}")
            return False

    async def _get_system_status(self) -> Dict[str, Any]:
        """
        Get current system status information.

        Returns:
            Dictionary with system status information
        """
        # Get counts for each state/folder
        folder_counts = {}
        
        # Define the folders we want to track
        folders_to_track = [
            "01_Inbox",
            "02_Needs_Action", 
            "03_Pending_Approval",
            "04_Approved",
            "05_Done",
            "06_Researching",
            "07_Reviewing"
        ]
        
        for folder in folders_to_track:
            try:
                notes = await self.api.get_all_notes_in_folder(folder)
                folder_counts[folder] = len(notes)
            except Exception as e:
                self.logger.warning(f"Could not get count for folder {folder}: {str(e)}")
                folder_counts[folder] = 0
        
        # Get recent activity
        recent_activity = await self._get_recent_activity()
        
        # Get memory highlights
        memory_highlights = await self._get_memory_highlights()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "folder_counts": folder_counts,
            "recent_activity": recent_activity,
            "memory_highlights": memory_highlights
        }

    async def _get_recent_activity(self) -> List[Dict[str, str]]:
        """
        Get recent activity in the system.

        Returns:
            List of recent activities
        """
        # For now, return a mock list of recent activities
        # In a real implementation, this would track actual system events
        return [
            {"time": datetime.now().isoformat(), "activity": "System started", "details": "Agentic loop initialized"},
            {"time": datetime.now().isoformat(), "activity": "Task processed", "details": "Processed task from 02_Needs_Action"},
        ]

    async def _get_memory_highlights(self) -> List[str]:
        """
        Get highlights from the memory system.

        Returns:
            List of memory highlights
        """
        # For now, return a mock list of memory highlights
        # In a real implementation, this would connect to the memory system
        try:
            from ..agent.memory import MemoryManager
            memory_manager = MemoryManager()
            highlights = await memory_manager.get_highlights()
            return highlights
        except Exception as e:
            self.logger.warning(f"Could not get memory highlights: {str(e)}")
            return ["Memory system not available", "No recent memories"]

    def _generate_dashboard_content(self, status_info: Dict[str, Any]) -> str:
        """
        Generate the dashboard content based on status information.

        Args:
            status_info: Dictionary with system status information

        Returns:
            String with dashboard content
        """
        content = f"""# Mission Control Dashboard

**Last Updated**: {status_info['timestamp']}

## System Status
- Active Tasks: {status_info['folder_counts']['02_Needs_Action']}
- Pending Approval: {status_info['folder_counts']['03_Pending_Approval']}
- In Research: {status_info['folder_counts']['06_Researching']}
- In Review: {status_info['folder_counts']['07_Reviewing']}

## Task Distribution
| Folder | Count |
|--------|-------|
| 01_Inbox | {status_info['folder_counts']['01_Inbox']} |
| 02_Needs_Action | {status_info['folder_counts']['02_Needs_Action']} |
| 03_Pending_Approval | {status_info['folder_counts']['03_Pending_Approval']} |
| 04_Approved | {status_info['folder_counts']['04_Approved']} |
| 05_Done | {status_info['folder_counts']['05_Done']} |
| 06_Researching | {status_info['folder_counts']['06_Researching']} |
| 07_Reviewing | {status_info['folder_counts']['07_Reviewing']} |

## Recent Activity
"""
        
        for activity in status_info['recent_activity']:
            content += f"- [{activity['time']}] {activity['activity']}: {activity['details']}\n"
        
        content += f"""
## Memory Highlights
"""
        
        for highlight in status_info['memory_highlights']:
            content += f"- {highlight}\n"
        
        content += f"""

## Dataview Queries
```dataview
TABLE created AS "Created Date", status AS "Status"
FROM "02_Needs_Action"
SORT created DESC
LIMIT 10
```

```dataview
TABLE created AS "Created Date", status AS "Status"
FROM "03_Pending_Approval" 
SORT created DESC
LIMIT 10
```

```dataview
TABLE created AS "Created Date", status AS "Status"
FROM "06_Researching"
SORT created DESC
LIMIT 10
```

```dataview
TABLE created AS "Created Date", status AS "Status"
FROM "07_Reviewing"
SORT created DESC
LIMIT 10
```
"""
        
        return content

    async def update_task_status_on_dashboard(self, task_path: str, new_status: str) -> bool:
        """
        Update the dashboard when a task status changes.

        Args:
            task_path: Path to the task file
            new_status: New status of the task

        Returns:
            True if successful, False otherwise
        """
        try:
            # Update the dashboard
            success = await self.update_dashboard()
            
            if success:
                self.logger.info(f"Dashboard updated for task {task_path} status change to {new_status}")
            else:
                self.logger.error(f"Failed to update dashboard for task {task_path} status change")
            
            return success
        except Exception as e:
            self.logger.error(f"Error updating dashboard for task status: {str(e)}")
            return False