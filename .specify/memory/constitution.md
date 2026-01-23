<!-- SYNC IMPACT REPORT
Version change: 1.0.0 -> 2.0.0
Modified principles: 
- III. Human-in-the-Loop Workflow (updated to include autonomy guidelines)
- Added new principles VI-VIII for Gold Tier
Added sections: VI. Autonomous Tool Usage, VII. Self-Correction Protocol, VIII. Memory Management, IX. Safety and Kill Switch Mechanism
Removed sections: None
Templates requiring updates: ✅ .specify/templates/plan-template.md, ✅ .specify/templates/spec-template.md, ✅ .specify/templates/tasks-template.md
Follow-up TODOs: None
-->

# Digital FTE (Gold Tier) Constitution

## Core Principles

### I. Python-Based Watcher Scripts
All monitoring and automation scripts must be implemented in Python. This ensures consistency, maintainability, and leverages Python's extensive ecosystem for automation tasks. Python provides robust libraries for system monitoring, file operations, and external service integrations.

### II. Obsidian as Primary Interface
Obsidian serves as the primary user interface and database through Markdown files. All data, notes, and documentation must be stored in Markdown format within the Obsidian vault. This creates a unified, searchable, and human-readable knowledge base that supports bidirectional linking and graph visualization.

### III. Human-in-the-Loop Workflow
Any external actions or system modifications must follow a Human-in-the-Loop (HITL) workflow. Automated processes may suggest or queue actions, but human approval is required before executing any external changes. This ensures safety, accountability, and prevents unintended consequences from automated systems. However, for routine operations and approved tools, the system may operate with increased autonomy as defined in Principle VI.

### IV. Modular and Documented Code
All code must be modular, reusable, and thoroughly documented. Each module should have a clear purpose, well-defined interfaces, and comprehensive documentation including usage examples. This enables maintainability, collaboration, and reduces technical debt.

### V. Local-First Data Storage
Prioritize local data storage solutions over cloud services wherever possible. This ensures data sovereignty, reduces external dependencies, and maintains privacy. Cloud services should only be used when local solutions are technically infeasible or when explicitly required by external systems.

### VI. Autonomous Tool Usage
The agent must be able to use tools (Python scripts) to perform external tasks like searching the web or sending emails. This autonomy is limited to pre-approved tools and operations that have been vetted for safety and security. The agent may execute these tools within defined parameters without requiring real-time human approval for each execution, but must log all such activities for audit purposes.

### VII. Self-Correction Protocol
If a tool execution fails, the agent must analyze the error and attempt a fix before asking the human. This includes: identifying the root cause of the failure, implementing appropriate corrective measures, retrying the operation if appropriate, and documenting the issue and resolution for future reference. Only after exhausting reasonable self-correction attempts should the agent escalate to human intervention.

### VIII. Memory Management
The agent must maintain a Memory.md file to track long-term goals across different tasks. This memory system enables continuity of context, persistence of objectives over extended periods, and learning from past interactions. The Memory.md file should be structured to allow efficient retrieval of relevant information while maintaining data integrity and preventing information overload.

### IX. Safety and Kill Switch Mechanism
All external API calls must be logged, and a 'Kill Switch' mechanism must be defined. The logging system must capture all external communications for security auditing and troubleshooting. The Kill Switch provides an immediate way to halt all autonomous operations in case of emergencies or unexpected behavior. The mechanism must be accessible to human operators and should safely terminate all active processes when activated.

## Additional Constraints

### Technology Stack Requirements
- Python 3.9+ for all automation and processing scripts
- Obsidian with Markdown files as the primary data store
- Git for version control of all Markdown files
- Standard Python libraries for system operations (os, pathlib, json, etc.)
- Logging framework for API call tracking
- Memory management system for long-term goal tracking

### Data Handling Policies
- All data must be stored locally in Markdown format
- Regular backups of the Obsidian vault must be maintained
- API call logs must be stored securely and reviewed periodically
- Memory.md file must be backed up regularly
- Sensitive information should be encrypted separately if required
- Data synchronization between systems should be explicit and controlled

## Development Workflow

### Code Review Process
- All Python code changes must undergo peer review
- Documentation updates must accompany code changes
- Modularity and reusability must be validated during review
- HITL mechanisms must be preserved during code changes
- New autonomous tools must undergo additional security review

### Quality Gates
- All Python code must pass static analysis (flake8, mypy)
- Unit tests must cover critical functionality
- Documentation completeness must be verified
- Local-first storage compliance must be confirmed
- Safety mechanisms must be validated before deployment

## Governance

This constitution governs all development and operational practices for the Digital FTE (Gold Tier). All team members must comply with these principles. Amendments to this constitution require explicit approval from project leadership and must include a migration plan for existing implementations.

**Version**: 2.0.0 | **Ratified**: 2026-01-23 | **Last Amended**: 2026-01-23