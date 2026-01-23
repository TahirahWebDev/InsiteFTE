# Data Model: Gold Tier Agentic Loop

**Feature**: Gold Tier Agentic Loop
**Date**: 2026-01-23
**Author**: AI Assistant

## Overview

This document defines the data model for the Gold Tier Agentic Loop system. It describes the structure of task files, tool execution records, memory entries, and the extended state machine with new states.

## Core Entities

### Task File

The primary entity in the system is the Task File, which represents a unit of work that moves through the extended state machine.

**Attributes**:
- `id` (string): Unique identifier for the task, generated when the file enters the system
- `filename` (string): Original filename with extension
- `sanitized_filename` (string): Cleaned filename that complies with filesystem restrictions
- `content` (string): The actual content of the task file
- `status` (enum): Current status of the task ('inbox', 'needs-action', 'pending-approval', 'approved', 'done', 'researching', 'reviewing')
- `created_date` (datetime): Timestamp when the file was first detected by the system
- `updated_date` (datetime): Timestamp of the last status change
- `source_folder` (string): The folder where the file originated
- `target_folder` (string): The folder where the file is being moved
- `metadata` (dict): Additional key-value pairs for tracking purposes
- `thought_process` (string): The AI's thought process for this task
- `tool_calls` (list): JSON blocks representing tools called during processing

**Validation Rules**:
- `id` must be unique within the system
- `filename` must end with .txt or .md extension
- `status` must be one of the predefined values
- `created_date` must be set when the file enters the system
- `content` must not be empty

### Extended State Machine

The system implements an extended folder-based state machine with seven distinct states:

**States**:
1. `01_Inbox` - Initial state for new tasks
2. `02_Needs_Action` - Tasks awaiting processing by the AI
3. `03_Pending_Approval` - Tasks completed by AI, awaiting human approval
4. `04_Approved` - Tasks approved by human, ready for finalization
5. `05_Done` - Completed tasks
6. `06_Researching` - Tasks requiring research activities
7. `07_Reviewing` - Tasks undergoing quality review

**State Transitions**:
- `01_Inbox` → `02_Needs_Action`: Automatic transition when file is detected
- `02_Needs_Action` → `06_Researching`: When research is required
- `06_Researching` → `07_Reviewing`: When research is complete
- `07_Reviewing` → `03_Pending_Approval`: When review is complete
- `03_Pending_Approval` → `04_Approved`: When human approves the task
- `04_Approved` → `05_Done`: When finalization is complete

**Transition Rules**:
- Files can only move forward in the state machine (except for error recovery)
- Each transition must update the `status` metadata in the file's frontmatter
- Transition to `05_Done` requires both approval and completion of all checklist items

### Tool Execution Record

Records of tool executions initiated by the AI agent.

**Attributes**:
- `id` (string): Unique identifier for the tool execution
- `task_id` (string): ID of the task that initiated the tool call
- `tool_name` (string): Name of the tool executed
- `parameters` (dict): Parameters passed to the tool
- `execution_time` (datetime): When the tool was executed
- `result` (any): Output from the tool execution
- `status` (enum): Status of the execution ('success', 'failed', 'pending')

### Memory Entry

Entries in the Memory.md file for long-term goal tracking.

**Attributes**:
- `id` (string): Unique identifier for the memory entry
- `timestamp` (datetime): When the entry was created
- `category` (string): Category of the memory (e.g., 'goal', 'fact', 'pattern')
- `content` (string): The actual memory content
- `relevance_score` (float): Score indicating how relevant this memory is to current tasks
- `tags` (list): Tags for categorization and retrieval

### Metadata Schema

Each task file includes YAML frontmatter with the following schema:

```yaml
id: string                    # Unique identifier for the task
status: enum                  # Current status (inbox, needs-action, pending-approval, approved, done, researching, reviewing)
created: datetime             # ISO 8601 timestamp when file entered system
updated: datetime             # ISO 8601 timestamp of last status change
original_filename: string     # Original filename before sanitization
processed_by_ai: boolean      # Whether AI has processed the task
approved_by_human: boolean    # Whether human has approved the task
checklist_completed: boolean  # Whether all checklist items are marked complete
thought_process: string       # The AI's thought process for this task
tool_calls: array             # JSON blocks representing tools called during processing
current_state_notes: string   # Additional notes specific to the current state
```

## Relationships

### Task File to Extended State Machine
- Each Task File exists in exactly one folder state at any given time
- The physical location of the file corresponds to its logical state
- Moving a file between folders triggers a state transition

### Task File to Tool Execution Record
- A Task File may have zero or many associated Tool Execution Records
- Tool Execution Records reference the Task File that initiated them
- This relationship enables tracking of all tools used for a specific task

### Task File to Memory Entry
- A Task File may reference zero or many Memory Entries
- Memory Entries may be relevant to multiple Task Files
- This relationship enables the AI to leverage past experiences

## File Formats

### Supported Input Formats
- `.txt` files: Plain text files
- `.md` files: Markdown files

### Output Format
- All files are stored as Markdown files with YAML frontmatter
- The content remains in the original format within the file body
- Metadata is stored in the YAML frontmatter section
- Tool execution results are stored in JSON blocks within the file

## Constraints

### Naming Convention
- Folder names follow the pattern: `NN_FolderName` (e.g., `01_Inbox`, `02_Needs_Action`)
- File names are sanitized to remove problematic characters
- Duplicate files receive timestamp suffixes to ensure uniqueness

### Data Integrity
- All file operations are atomic to prevent corruption
- Metadata is validated before each state transition
- System maintains consistency between file location and status metadata

## Lifecycle Management

### Creation
1. File is placed in `01_Inbox`
2. System detects file creation event
3. File is sanitized and receives initial metadata
4. File is moved to `02_Needs_Action`

### Processing
1. AI processes the task in `02_Needs_Action`
2. If research is needed, status is updated to `researching` and file is moved to `06_Researching`
3. Research is conducted using tools
4. Status is updated to `reviewing` and file is moved to `07_Reviewing`
5. Quality review is performed
6. Status is updated to `pending-approval` and file is moved to `03_Pending_Approval`

### Approval
1. Human reviews and approves the task
2. Status is updated to `approved`
3. File is moved to `04_Approved`

### Completion
1. Finalization process runs
2. Status is updated to `done`
3. File is moved to `05_Done`