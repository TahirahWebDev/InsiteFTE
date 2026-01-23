"""
Autonomous planner for the Gold Tier Agentic Loop system.
"""

import asyncio
from typing import Dict, List, Any
from ..utils.logger import get_logger


class AutonomousPlanner:
    """
    Component that automatically generates multi-step project plans when tasks enter 02_Needs_Action.
    """
    
    def __init__(self):
        """Initialize the autonomous planner."""
        self.logger = get_logger()
    
    async def generate_plan(self, task_description: str) -> Dict[str, Any]:
        """
        Generate a multi-step project plan for a given task.
        
        Args:
            task_description: Description of the task to plan for
            
        Returns:
            Dictionary containing the generated plan
        """
        self.logger.info(f"Generating plan for task: {task_description[:50]}...")
        
        # Simulate AI processing time
        await asyncio.sleep(0.5)
        
        # In a real implementation, this would use AI to generate a detailed plan
        # For this example, we'll return a mock plan based on common patterns
        
        # Simple keyword-based plan generation for demonstration
        plan_steps = []
        
        if any(keyword in task_description.lower() for keyword in ["research", "study", "analyze", "investigate"]):
            plan_steps.extend([
                {"step": 1, "action": "conduct_research", "description": "Research the topic in depth"},
                {"step": 2, "action": "gather_sources", "description": "Gather relevant sources and materials"},
                {"step": 3, "action": "analyze_data", "description": "Analyze the collected data"},
                {"step": 4, "action": "synthesize_findings", "description": "Synthesize findings into coherent points"},
                {"step": 5, "action": "draft_report", "description": "Draft a comprehensive report"}
            ])
        elif any(keyword in task_description.lower() for keyword in ["summarize", "summary", "overview"]):
            plan_steps.extend([
                {"step": 1, "action": "collect_information", "description": "Collect relevant information"},
                {"step": 2, "action": "identify_key_points", "description": "Identify key points to include"},
                {"step": 3, "action": "organize_structure", "description": "Organize information in logical structure"},
                {"step": 4, "action": "draft_summary", "description": "Draft the summary"},
                {"step": 5, "action": "review_and_edit", "description": "Review and edit for clarity"}
            ])
        elif any(keyword in task_description.lower() for keyword in ["create", "develop", "build", "make"]):
            plan_steps.extend([
                {"step": 1, "action": "define_requirements", "description": "Define requirements and specifications"},
                {"step": 2, "action": "design_solution", "description": "Design the solution architecture"},
                {"step": 3, "action": "implement_solution", "description": "Implement the solution"},
                {"step": 4, "action": "test_implementation", "description": "Test the implementation"},
                {"step": 5, "action": "refine_solution", "description": "Refine and optimize the solution"}
            ])
        else:
            # Default plan for other types of tasks
            plan_steps.extend([
                {"step": 1, "action": "analyze_task", "description": "Analyze the task requirements"},
                {"step": 2, "action": "break_down_steps", "description": "Break down the task into manageable steps"},
                {"step": 3, "action": "prioritize_steps", "description": "Prioritize steps based on dependencies"},
                {"step": 4, "action": "execute_plan", "description": "Execute the planned steps"},
                {"step": 5, "action": "review_completion", "description": "Review task completion"}
            ])
        
        # Create the plan structure
        plan = {
            "task_description": task_description,
            "generated_at": asyncio.get_event_loop().time(),
            "steps": plan_steps,
            "estimated_duration": len(plan_steps) * 2,  # Estimated duration in hours
            "required_tools": self._identify_required_tools(task_description),
            "dependencies": self._identify_dependencies(plan_steps)
        }
        
        self.logger.info(f"Plan generated with {len(plan_steps)} steps")
        return plan
    
    def _identify_required_tools(self, task_description: str) -> List[str]:
        """
        Identify which tools might be needed for the task.
        
        Args:
            task_description: Description of the task
            
        Returns:
            List of required tools
        """
        required_tools = []
        
        if any(keyword in task_description.lower() for keyword in ["research", "study", "analyze", "investigate", "search", "find"]):
            required_tools.append("search_web")
        
        if any(keyword in task_description.lower() for keyword in ["notify", "inform", "tell", "update", "alert"]):
            required_tools.append("send_notification")
        
        # If no specific tools identified, return a default set
        if not required_tools:
            required_tools = ["search_web"]  # Default tool for most tasks
        
        return required_tools
    
    def _identify_dependencies(self, plan_steps: List[Dict[str, Any]]) -> Dict[int, List[int]]:
        """
        Identify dependencies between steps in the plan.
        
        Args:
            plan_steps: List of steps in the plan
            
        Returns:
            Dictionary mapping step numbers to their dependencies
        """
        dependencies = {}
        
        # In this simple model, each step depends on the previous one
        for i in range(1, len(plan_steps)):
            dependencies[i + 1] = [i]  # Each step depends on the previous step
        
        return dependencies
    
    async def validate_plan(self, plan: Dict[str, Any]) -> bool:
        """
        Validate that the generated plan is reasonable and executable.
        
        Args:
            plan: The plan to validate
            
        Returns:
            True if the plan is valid, False otherwise
        """
        # Check if plan has required fields
        required_fields = ["task_description", "steps", "generated_at"]
        for field in required_fields:
            if field not in plan:
                self.logger.error(f"Plan validation failed: Missing required field '{field}'")
                return False
        
        # Check if steps exist and are properly formatted
        if not isinstance(plan["steps"], list) or len(plan["steps"]) == 0:
            self.logger.error("Plan validation failed: No steps in plan")
            return False
        
        for step in plan["steps"]:
            if not isinstance(step, dict) or "step" not in step or "action" not in step:
                self.logger.error("Plan validation failed: Invalid step format")
                return False
        
        # If all checks pass, the plan is valid
        self.logger.info("Plan validation passed")
        return True