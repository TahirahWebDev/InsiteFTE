<!-- SYNC IMPACT REPORT
Version change: N/A -> 1.0.0
Added sections: All principles and governance sections
Removed sections: None
Templates requiring updates: N/A
Follow-up TODOs: None
-->

# Digital FTE (Bronze Tier) Constitution

## Core Principles

### I. Python-Based Watcher Scripts
All monitoring and automation scripts must be implemented in Python. This ensures consistency, maintainability, and leverages Python's extensive ecosystem for automation tasks. Python provides robust libraries for system monitoring, file operations, and external service integrations.

### II. Obsidian as Primary Interface
Obsidian serves as the primary user interface and database through Markdown files. All data, notes, and documentation must be stored in Markdown format within the Obsidian vault. This creates a unified, searchable, and human-readable knowledge base that supports bidirectional linking and graph visualization.

### III. Human-in-the-Loop Workflow
Any external actions or system modifications must follow a Human-in-the-Loop (HITL) workflow. Automated processes may suggest or queue actions, but human approval is required before executing any external changes. This ensures safety, accountability, and prevents unintended consequences from automated systems.

### IV. Modular and Documented Code
All code must be modular, reusable, and thoroughly documented. Each module should have a clear purpose, well-defined interfaces, and comprehensive documentation including usage examples. This enables maintainability, collaboration, and reduces technical debt.

### V. Local-First Data Storage
Prioritize local data storage solutions over cloud services wherever possible. This ensures data sovereignty, reduces external dependencies, and maintains privacy. Cloud services should only be used when local solutions are technically infeasible or when explicitly required by external systems.

## Additional Constraints

### Technology Stack Requirements
- Python 3.9+ for all automation and processing scripts
- Obsidian with Markdown files as the primary data store
- Git for version control of all Markdown files
- Standard Python libraries for system operations (os, pathlib, json, etc.)

### Data Handling Policies
- All data must be stored locally in Markdown format
- Regular backups of the Obsidian vault must be maintained
- Sensitive information should be encrypted separately if required
- Data synchronization between systems should be explicit and controlled

## Development Workflow

### Code Review Process
- All Python code changes must undergo peer review
- Documentation updates must accompany code changes
- Modularity and reusability must be validated during review
- HITL mechanisms must be preserved during code changes

### Quality Gates
- All Python code must pass static analysis (flake8, mypy)
- Unit tests must cover critical functionality
- Documentation completeness must be verified
- Local-first storage compliance must be confirmed

## Governance

This constitution governs all development and operational practices for the Digital FTE (Bronze Tier). All team members must comply with these principles. Amendments to this constitution require explicit approval from project leadership and must include a migration plan for existing implementations.

**Version**: 1.0.0 | **Ratified**: 2026-01-23 | **Last Amended**: 2026-01-23