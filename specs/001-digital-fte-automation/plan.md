# Implementation Plan: Digital FTE Automation

**Branch**: `001-digital-fte-automation` | **Date**: 2026-01-23 | **Spec**: [link]
**Input**: Feature specification from `/specs/001-digital-fte-automation/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a Digital FTE (Full-Time Equivalent) system that automates task management through an Obsidian vault using a folder-based state machine. The system includes a Python-based watcher script that monitors the Inbox folder, automatically moves files to Needs Action, and integrates with Obsidian's Dataview plugin for dashboard display.

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: watchdog, uv for dependency management, Obsidian with Dataview plugin
**Storage**: File system with Markdown files in Obsidian vault structure
**Testing**: pytest for unit tests, manual verification of file movement and dashboard display
**Target Platform**: Cross-platform (Windows, macOS, Linux) for local Obsidian vault
**Project Type**: Standalone Python application with file system monitoring
**Performance Goals**: Process new files within 10 seconds of creation
**Constraints**: Local-first storage, human-in-the-loop approval for completion, YAML frontmatter for metadata
**Scale/Scope**: Individual or small team usage with up to hundreds of tasks per month

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Passed**: All implementation details align with Digital FTE Constitution:
- Python-based watcher scripts (Principle I)
- Obsidian as primary interface (Principle II)  
- Human-in-the-loop workflow (Principle III)
- Modular and documented code (Principle IV)
- Local-first data storage (Principle V)

## Project Structure

### Documentation (this feature)

```text
specs/001-digital-fte-automation/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
scripts/
├── watcher.py           # Main file monitoring script
├── utils/
│   ├── file_handler.py  # File processing utilities
│   ├── sanitizer.py     # Filename sanitization utilities
│   └── metadata.py      # YAML frontmatter utilities
└── config.py            # Configuration settings

tests/
├── unit/
│   ├── test_watcher.py
│   ├── test_file_handler.py
│   ├── test_sanitizer.py
│   └── test_metadata.py
└── integration/
    └── test_end_to_end.py

pyproject.toml            # Project dependencies and configuration
uv.lock                   # Dependency lock file
README.md                 # Project documentation
```

**Structure Decision**: Single project structure with clear separation of concerns. The main watcher script handles file monitoring, while utility modules handle specific responsibilities like file handling, sanitization, and metadata management. Tests are organized by type (unit vs integration) and by corresponding module.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|