"""
Core agent logic and thought processes for the Gold Tier Agentic Loop system.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List
from ..utils.logger import get_logger
from ..utils.json_parser import extract_json_blocks, parse_tool_call
from ..tools.registry import ToolRegistry
from ..state_machine.engine import StateMachineEngine
from ..planner.autonomous_planner import AutonomousPlanner
from .critic import CriticModule
from .memory import MemoryManager
from ..config import POLLING_INTERVAL


class CoreAgent:
    """
    Core agent that handles thought processes and coordinates other components.
    """

    def __init__(self):
        """Initialize the core agent."""
        self.logger = get_logger()
        self.tool_registry = ToolRegistry()
        self.state_machine = StateMachineEngine()
        self.planner = AutonomousPlanner()
        self.critic = CriticModule()
        self.memory_manager = MemoryManager()

        # Register default tools
        from ..tools.search_web import WebSearchTool
        from ..tools.send_notification import SendNotificationTool

        self.tool_registry.register_tool(WebSearchTool())
        self.tool_registry.register_tool(SendNotificationTool())

        # Agent state
        self.is_running = False
        self.thought_process_log = []

    async def process_thought(self, task_description: str) -> Dict[str, Any]:
        """
        Process a thought about a task and determine next actions.

        Args:
            task_description: Description of the task to think about

        Returns:
            Dictionary with thought process and next actions
        """
        self.logger.info(f"Processing thought for task: {task_description[:50]}...")

        # Add to thought process log
        thought_entry = {
            "timestamp": asyncio.get_event_loop().time(),
            "task_description": task_description,
            "thought_process": "",
            "next_actions": []
        }

        # Generate a thought process
        thought_process = await self._generate_thought_process(task_description)
        thought_entry["thought_process"] = thought_process

        # Determine next actions based on the task
        next_actions = await self._determine_next_actions(task_description)
        thought_entry["next_actions"] = next_actions

        self.thought_process_log.append(thought_entry)

        return {
            "thought_process": thought_process,
            "next_actions": next_actions,
            "timestamp": thought_entry["timestamp"]
        }

    async def _generate_thought_process(self, task_description: str) -> str:
        """
        Generate a thought process for a given task.

        Args:
            task_description: Description of the task

        Returns:
            String describing the thought process
        """
        # Simulate thinking time
        await asyncio.sleep(0.2)

        # In a real implementation, this would use AI to generate a detailed thought process
        # For this example, we'll return a simple thought process
        thought_process = f"""
Initial Assessment:
- Task: {task_description}
- Category: {self._categorize_task(task_description)}
- Priority: {self._assess_priority(task_description)}

Action Plan:
- Step 1: Analyze the requirements
- Step 2: Gather necessary information
- Step 3: Execute required actions
- Step 4: Review and validate results
- Step 5: Prepare for approval

Potential Challenges:
- {self._identify_potential_challenges(task_description)}

Required Tools:
- {', '.join(self.planner._identify_required_tools(task_description))}
        """.strip()

        return thought_process

    def _categorize_task(self, task_description: str) -> str:
        """
        Categorize a task based on its description.

        Args:
            task_description: Description of the task

        Returns:
            Category of the task
        """
        task_lower = task_description.lower()

        if any(keyword in task_lower for keyword in ["research", "study", "analyze", "investigate", "search", "find"]):
            return "Research"
        elif any(keyword in task_lower for keyword in ["summarize", "summary", "overview", "report"]):
            return "Summarization"
        elif any(keyword in task_lower for keyword in ["create", "develop", "build", "make", "generate"]):
            return "Creation"
        elif any(keyword in task_lower for keyword in ["notify", "inform", "tell", "update", "alert"]):
            return "Communication"
        else:
            return "General"

    def _assess_priority(self, task_description: str) -> str:
        """
        Assess the priority of a task based on its description.

        Args:
            task_description: Description of the task

        Returns:
            Priority level (High, Medium, Low)
        """
        task_lower = task_description.lower()

        # Keywords that indicate high priority
        high_priority_keywords = ["urgent", "asap", "immediately", "critical", "important", "deadline", "today"]

        # Check for high priority indicators
        for keyword in high_priority_keywords:
            if keyword in task_lower:
                return "High"

        # Medium priority indicators
        medium_priority_keywords = ["soon", "this week", "next", "please", "needed"]

        for keyword in medium_priority_keywords:
            if keyword in task_lower:
                return "Medium"

        # Default to low priority
        return "Low"

    def _identify_potential_challenges(self, task_description: str) -> str:
        """
        Identify potential challenges for a task.

        Args:
            task_description: Description of the task

        Returns:
            Description of potential challenges
        """
        task_lower = task_description.lower()

        challenges = []

        if "research" in task_lower or "analyze" in task_lower:
            challenges.append("Finding reliable and up-to-date sources")
        elif "create" in task_lower or "build" in task_lower:
            challenges.append("Ensuring the output meets quality standards")
        elif "communicate" in task_lower or "notify" in task_lower:
            challenges.append("Determining the appropriate communication channel")

        if not challenges:
            challenges.append("Understanding the specific requirements clearly")

        return "; ".join(challenges)

    async def _determine_next_actions(self, task_description: str) -> List[Dict[str, Any]]:
        """
        Determine the next actions to take for a task.

        Args:
            task_description: Description of the task

        Returns:
            List of next actions to take
        """
        # Based on the task description, determine appropriate next actions
        actions = []

        # If it's a research task, add a search action
        if any(keyword in task_description.lower() for keyword in ["research", "find", "search", "analyze"]):
            actions.append({
                "action": "execute_tool",
                "tool_name": "search_web",
                "parameters": {
                    "query": task_description,
                    "num_results": 5
                },
                "reason": "Task requires information gathering"
            })

        # Add a planning action for most tasks
        actions.append({
            "action": "generate_plan",
            "reason": "Generate a structured plan for task completion"
        })

        # Add a review action
        actions.append({
            "action": "review_output",
            "reason": "Ensure quality before submission"
        })

        return actions

    async def execute_task(self, task_file_path: str) -> bool:
        """
        Execute a task from a file.

        Args:
            task_file_path: Path to the task file

        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Executing task from file: {task_file_path}")

            # Read the task file
            with open(task_file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract any tool calls from the file
            json_blocks = extract_json_blocks(content)

            # Process each tool call
            for json_block in json_blocks:
                try:
                    tool_call_info = parse_tool_call(json_block)
                    tool_name = tool_call_info['name']
                    parameters = tool_call_info['parameters']

                    self.logger.info(f"Executing tool call: {tool_name} with parameters {parameters}")

                    # Execute the tool
                    result = await self.tool_registry.execute_tool(tool_name, parameters)

                    self.logger.info(f"Tool {tool_name} executed successfully with result: {result}")

                    # Update the file with the tool result
                    await self._update_file_with_tool_result(task_file_path, tool_name, result)

                except Exception as e:
                    self.logger.error(f"Error executing tool call: {str(e)}")
                    # Continue with other tool calls
                    continue

            # If no tool calls were found, generate a plan
            if not json_blocks:
                self.logger.info("No tool calls found, generating autonomous plan")

                # Generate a plan for the task
                plan = await self.planner.generate_plan(content)

                # Validate the plan
                is_valid = await self.planner.validate_plan(plan)

                if is_valid:
                    self.logger.info("Plan generated and validated successfully")

                    # Update the file with the plan
                    await self._update_file_with_plan(task_file_path, plan)
                else:
                    self.logger.error("Generated plan failed validation")
                    return False

            # Perform quality review using the critic module
            self.logger.info("Performing quality review with critic module")

            evaluation = await self.critic.evaluate_quality(content)
            should_approve = await self.critic.should_approve(evaluation)

            if should_approve:
                self.logger.info("Content passed quality review")
            else:
                self.logger.info("Content did not pass quality review, making improvements")

                # In a real implementation, this would improve the content
                # For now, we'll just log the issues and suggestions
                for issue in evaluation.get("issues_found", []):
                    self.logger.info(f"Issue found: {issue}")

                for suggestion in evaluation.get("suggestions", []):
                    self.logger.info(f"Suggestion: {suggestion}")

            # Add to memory
            await self.memory_manager.add_memory(
                category="task_execution",
                content=f"Executed task: {content[:100]}...",
                tags=["task", "execution", self._categorize_task(content)]
            )

            # Move the file to pending approval after processing
            from ..state_machine.states import State
            await self.state_machine.transition_file(task_file_path, State.PENDING_APPROVAL)

            return True

        except Exception as e:
            self.logger.error(f"Error executing task {task_file_path}: {str(e)}")
            return False

    async def _update_file_with_tool_result(self, file_path: str, tool_name: str, result: Any):
        """
        Update a file with the result of a tool execution.

        Args:
            file_path: Path to the file to update
            tool_name: Name of the tool that was executed
            result: Result of the tool execution
        """
        # Read the current file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Append the tool result to the file
        tool_result_section = f"\n\n## Tool Result: {tool_name}\n"
        tool_result_section += f"Executed at: {asyncio.get_event_loop().time()}\n"
        tool_result_section += f"Result: {json.dumps(result, indent=2, default=str)}\n"

        updated_content = content + tool_result_section

        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        self.logger.info(f"Updated file {file_path} with result from {tool_name}")

    async def _update_file_with_plan(self, file_path: str, plan: Dict[str, Any]):
        """
        Update a file with an autonomous plan.

        Args:
            file_path: Path to the file to update
            plan: The plan to add to the file
        """
        # Read the current file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Append the plan to the file
        plan_section = f"\n\n## Autonomous Plan\n"
        plan_section += f"Generated at: {asyncio.get_event_loop().time()}\n"
        plan_section += f"Task Description: {plan.get('task_description', '')}\n"
        plan_section += f"Estimated Duration: {plan.get('estimated_duration', 'N/A')} hours\n"
        plan_section += f"Required Tools: {', '.join(plan.get('required_tools', []))}\n"
        plan_section += "\n### Steps:\n"

        for step in plan.get('steps', []):
            plan_section += f"- Step {step.get('step', '?')}: {step.get('action', 'N/A')} - {step.get('description', 'N/A')}\n"

        updated_content = content + plan_section

        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        self.logger.info(f"Updated file {file_path} with autonomous plan")

    async def run_agentic_loop(self):
        """
        Run the main agentic loop that periodically checks the 02_Needs_Action folder.
        """
        self.logger.info("Starting agentic loop...")
        self.is_running = True

        from ..config import NEEDS_ACTION_PATH

        while self.is_running:
            try:
                # Check the 02_Needs_Action folder for new tasks
                needs_action_dir = Path(NEEDS_ACTION_PATH)

                if needs_action_dir.exists():
                    # Get all .txt and .md files in the needs_action folder
                    task_files = [
                        f for f in needs_action_dir.iterdir()
                        if f.is_file() and f.suffix.lower() in ['.txt', '.md']
                    ]

                    if task_files:
                        self.logger.info(f"Found {len(task_files)} task files to process")

                        # Process each task file
                        for task_file in task_files:
                            self.logger.info(f"Processing task file: {task_file.name}")

                            # Execute the task
                            success = await self.execute_task(str(task_file))

                            if success:
                                self.logger.info(f"Successfully processed task: {task_file.name}")

                                # Move the file to the next state (e.g., REVIEWING or PENDING_APPROVAL)
                                # For this example, we'll move to REVIEWING if it's research-related
                                content = task_file.read_text(encoding='utf-8')
                                if any(keyword in content.lower() for keyword in ["research", "analyze", "study", "investigate"]):
                                    from ..state_machine.states import State
                                    await self.state_machine.transition_file(str(task_file), State.REVIEWING)
                                else:
                                    # For other tasks, move to PENDING_APPROVAL
                                    from ..state_machine.states import State
                                    await self.state_machine.transition_file(str(task_file), State.PENDING_APPROVAL)
                            else:
                                self.logger.error(f"Failed to process task: {task_file.name}")
                    else:
                        self.logger.info("No task files found in needs_action folder")
                else:
                    self.logger.warning(f"Needs action directory does not exist: {NEEDS_ACTION_PATH}")

                # Wait for the polling interval before checking again
                await asyncio.sleep(POLLING_INTERVAL)

            except Exception as e:
                self.logger.error(f"Error in agentic loop: {str(e)}")
                # Continue the loop despite errors
                await asyncio.sleep(POLLING_INTERVAL)

        self.logger.info("Agentic loop stopped")

    async def stop_agentic_loop(self):
        """
        Stop the agentic loop.
        """
        self.logger.info("Stopping agentic loop...")
        self.is_running = False