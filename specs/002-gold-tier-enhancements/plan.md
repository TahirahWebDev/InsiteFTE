# Implementation Plan: Gold Tier Agentic Loop

**Branch**: `002-gold-tier-enhancements` | **Date**: 2026-01-23 | **Spec**: [link]
**Input**: Feature specification from `/specs/002-gold-tier-enhancements/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a Gold Tier Agentic Loop system that transforms the Digital FTE from a simple watcher to an autonomous agent that periodically checks the 02_Needs_Action folder, executes tools via JSON commands, and integrates with Obsidian's DataviewJS for advanced dashboard capabilities.

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: watchdog, ruamel.yaml, obsidian-api-wrapper, dataviewjs, asyncio
**Storage**: File system with Markdown files in Obsidian vault structure
**Testing**: pytest for unit tests, manual verification of agentic loop and dashboard display
**Target Platform**: Cross-platform (Windows, macOS, Linux) for local Obsidian vault
**Project Type**: Standalone Python application with periodic polling and tool execution capabilities
**Performance Goals**: Process new tasks within 60 seconds of creation, execute tools with minimal latency
**Constraints**: Local-first storage, human-in-the-loop approval for critical actions, YAML frontmatter for metadata, JSON-based tool execution
**Scale/Scope**: Individual or small team usage with up to hundreds of tasks per month

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Passed**: All implementation details align with Digital FTE Constitution:
- Python-based watcher scripts (Principle I)
- Obsidian as primary interface (Principle II)  
- Human-in-the-loop workflow (Principle III)
- Modular and documented code (Principle IV)
- Local-first data storage (Principle V)
- Autonomous tool usage within defined parameters (Principle VI)
- Self-correction protocols (Principle VII)
- Memory management (Principle VIII)
- Safety and kill switch mechanisms (Principle IX)

## Project Structure

### Documentation (this feature)

```text
specs/002-gold-tier-enhancements/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
agentic_loop/
├── main.py              # Main agentic loop controller
├── agent/
│   ├── __init__.py
│   ├── core.py          # Core agent logic and thought processes
│   ├── memory.py        # Memory management system
│   └── critic.py        # Critic module for quality assessment
├── tools/
│   ├── __init__.py
│   ├── base_tool.py     # Base tool class
│   ├── search_web.py    # Web search tool
│   ├── send_notification.py  # Notification tool
│   └── registry.py      # Tool registry and executor
├── obsidian/
│   ├── __init__.py
│   ├── api_wrapper.py   # Obsidian API wrapper
│   └── dashboard.py     # Mission control dashboard updater
├── state_machine/
│   ├── __init__.py
│   ├── engine.py        # State transition engine
│   └── states.py        # Definitions for all states (01-07)
├── planner/
│   ├── __init__.py
│   └── autonomous_planner.py  # Autonomous planning module
├── config.py            # Configuration settings
└── utils/
    ├── __init__.py
    ├── file_operations.py  # File handling utilities
    ├── json_parser.py   # JSON command parser
    └── logger.py        # Enhanced logging with safety features

tests/
├── unit/
│   ├── test_agent_core.py
│   ├── test_tools.py
│   ├── test_state_machine.py
│   └── test_planner.py
├── integration/
│   ├── test_agentic_loop.py
│   └── test_obsidian_integration.py
└── e2e/
    └── test_complete_workflow.py

memory/
├── Memory.md            # Long-term memory file
└── memory_backup.md     # Backup of memory

pyproject.toml            # Project dependencies and configuration
uv.lock                   # Dependency lock file
README.md                 # Project documentation
```

**Structure Decision**: Modular architecture with clear separation of concerns. The main agentic loop orchestrates the agent, tools, state machine, and Obsidian integration. Each component has a specific responsibility and can be developed and tested independently.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|