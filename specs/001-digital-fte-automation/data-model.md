# Data Model: Digital FTE Automation

**Feature**: Digital FTE Automation
**Date**: 2026-01-23
**Author**: AI Assistant

## Overview

This document defines the data model for the Digital FTE Automation system. It describes the structure of task files, their metadata, and the state transitions within the folder-based system.

## Core Entities

### Task File

The primary entity in the system is the Task File, which represents a unit of work that moves through the state machine.

**Attributes**:
- `id` (string): Unique identifier for the task, generated when the file enters the system
- `filename` (string): Original filename with extension
- `sanitized_filename` (string): Cleaned filename that complies with filesystem restrictions
- `content` (string): The actual content of the task file
- `status` (enum): Current status of the task ('inbox', 'needs-action', 'pending-approval', 'approved', 'done')
- `created_date` (datetime): Timestamp when the file was first detected by the system
- `updated_date` (datetime): Timestamp of the last status change
- `source_folder` (string): The folder where the file originated
- `target_folder` (string): The folder where the file is being moved
- `metadata` (dict): Additional key-value pairs for tracking purposes

**Validation Rules**:
- `id` must be unique within the system
- `filename` must end with .txt or .md extension
- `status` must be one of the predefined values
- `created_date` must be set when the file enters the system
- `content` must not be empty

### Folder State Machine

The system implements a folder-based state machine with five distinct states:

**States**:
1. `01_Inbox` - Initial state for new tasks
2. `02_Needs_Action` - Tasks awaiting processing by the AI
3. `03_Pending_Approval` - Tasks completed by AI, awaiting human approval
4. `04_Approved` - Tasks approved by human, ready for finalization
5. `05_Done` - Completed tasks

**State Transitions**:
- `01_Inbox` → `02_Needs_Action`: Automatic transition when file is detected
- `02_Needs_Action` → `03_Pending_Approval`: When AI completes initial processing
- `03_Pending_Approval` → `04_Approved`: When human approves the task
- `04_Approved` → `05_Done`: When finalization is complete

**Transition Rules**:
- Files can only move forward in the state machine (except for error recovery)
- Each transition must update the `status` metadata in the file's frontmatter
- Transition to `05_Done` requires both approval and completion of all checklist items

### Metadata Schema

Each task file includes YAML frontmatter with the following schema:

```yaml
id: string           # Unique identifier for the task
status: enum         # Current status (inbox, needs-action, pending-approval, approved, done)
created: datetime    # ISO 8601 timestamp when file entered system
updated: datetime    # ISO 8601 timestamp of last status change
original_filename: string  # Original filename before sanitization
processed_by_ai: boolean   # Whether AI has processed the task
approved_by_human: boolean # Whether human has approved the task
checklist_completed: boolean # Whether all checklist items are marked complete
```

## Relationships

### Task File to Folder State
- Each Task File exists in exactly one folder state at any given time
- The physical location of the file corresponds to its logical state
- Moving a file between folders triggers a state transition

### Task File to Metadata
- Each Task File has exactly one associated metadata object
- The metadata is stored in the YAML frontmatter of the file
- The metadata reflects the current state of the task

## File Formats

### Supported Input Formats
- `.txt` files: Plain text files
- `.md` files: Markdown files

### Output Format
- All files are stored as Markdown files with YAML frontmatter
- The content remains in the original format within the file body
- Metadata is stored in the YAML frontmatter section

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
2. Status is updated to `pending-approval`
3. File is moved to `03_Pending_Approval`

### Approval
1. Human reviews and approves the task
2. Status is updated to `approved`
3. File is moved to `04_Approved`

### Completion
1. Finalization process runs
2. Status is updated to `done`
3. File is moved to `05_Done`