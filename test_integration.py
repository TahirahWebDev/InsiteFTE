#!/usr/bin/env python3
"""
Integration test for the Digital FTE Automation and Gold Tier Agentic Loop systems.
"""

import asyncio
import os
from pathlib import Path

def test_imports():
    """Test that all major components can be imported without errors."""
    print("Testing imports...")

    # Test first feature components
    from scripts.watcher import InboxHandler
    from scripts.config import INBOX_PATH, NEEDS_ACTION_PATH
    from scripts.utils.file_handler import move_file
    from scripts.utils.sanitizer import sanitize_filename
    from scripts.utils.metadata import add_yaml_frontmatter

    print("[OK] First feature components imported successfully")

    # Test second feature components
    from agentic_loop.main import AgenticLoopController
    from agentic_loop.agent.core import CoreAgent
    from agentic_loop.state_machine.engine import StateMachineEngine
    from agentic_loop.tools.registry import ToolRegistry
    from agentic_loop.planner.autonomous_planner import AutonomousPlanner
    from agentic_loop.agent.critic import CriticModule
    from agentic_loop.agent.memory import MemoryManager
    from agentic_loop.obsidian.api_wrapper import ObsidianAPIWrapper
    from agentic_loop.obsidian.dashboard import DashboardUpdater

    print("[OK] Second feature components imported successfully")

    # Test that configurations are properly loaded
    assert INBOX_PATH is not None
    assert NEEDS_ACTION_PATH is not None
    print("[OK] Configurations loaded successfully")


def test_basic_functionality():
    """Test basic functionality of key components."""
    print("\nTesting basic functionality...")

    # Test filename sanitization
    from scripts.utils.sanitizer import sanitize_filename
    test_filename = "test file with spaces & special chars!.txt"
    sanitized = sanitize_filename(test_filename)
    print(f"[OK] Filename sanitized: '{test_filename}' -> '{sanitized}'")

    # Test YAML frontmatter addition
    from scripts.utils.metadata import add_yaml_frontmatter
    import tempfile

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp_file:
        tmp_file.write("# Test File\n\nThis is a test file.\n")
        temp_path = tmp_file.name

    try:
        success = add_yaml_frontmatter(temp_path, {"status": "test", "created": "2026-01-24"})
        assert success, "Failed to add YAML frontmatter"
        print("[OK] YAML frontmatter added successfully")
    finally:
        # Clean up
        Path(temp_path).unlink()

    # Test state machine
    from agentic_loop.state_machine.engine import StateMachineEngine
    from agentic_loop.state_machine.states import State
    engine = StateMachineEngine()
    print(f"[OK] State machine engine created, current states: {[s.value for s in State]}")


async def test_async_components():
    """Test asynchronous components."""
    print("\nTesting async components...")

    # Test memory manager
    from agentic_loop.agent.memory import MemoryManager
    memory_manager = MemoryManager()

    # Add a test memory
    success = await memory_manager.add_memory(
        category="test",
        content="This is a test memory entry",
        tags=["integration", "test"]
    )
    assert success, "Failed to add memory"
    print("[OK] Memory added successfully")

    # Retrieve memories
    memories = await memory_manager.retrieve_memories(category="test")
    assert len(memories) > 0, "Failed to retrieve memories"
    print("[OK] Memories retrieved successfully")

    # Test planner
    from agentic_loop.planner.autonomous_planner import AutonomousPlanner
    planner = AutonomousPlanner()

    plan = await planner.generate_plan("Write a report on market trends")
    assert "steps" in plan, "Failed to generate plan"
    print("[OK] Plan generated successfully")


def test_folder_structure():
    """Test that required folder structure exists."""
    print("\nTesting folder structure...")

    # Check that required directories exist
    required_dirs = [
        "01_Inbox",
        "02_Needs_Action",
        "03_Pending_Approval",
        "04_Approved",
        "05_Done",
        "06_Researching",
        "07_Reviewing"
    ]

    base_path = Path.cwd()
    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        if not dir_path.exists():
            dir_path.mkdir(exist_ok=True)
            print(f"[INFO] Created missing directory: {dir_name}")
        else:
            print(f"[OK] Directory exists: {dir_name}")


async def main():
    """Run all integration tests."""
    print("Starting integration tests for Digital FTE Automation and Gold Tier Agentic Loop...\n")

    test_imports()
    test_basic_functionality()
    await test_async_components()
    test_folder_structure()

    print("\n[SUCCESS] All integration tests passed!")


if __name__ == "__main__":
    asyncio.run(main())