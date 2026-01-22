# File System Interface Contract: Digital FTE Automation

**Feature**: Digital FTE Automation
**Date**: 2026-01-23
**Author**: AI Assistant

## Overview

This document defines the contract for the file system interface of the Digital FTE Automation system. Since the system operates primarily through file system events and folder-based state management, the interface is defined by file structure, naming conventions, and metadata requirements.

## File System Events

### Event: File Created in Inbox
- **Trigger**: A new file is created in the `01_Inbox` folder
- **Conditions**: File must have `.txt` or `.md` extension
- **Guarantee**: File will be processed within 10 seconds
- **Post-condition**: File will be moved to `02_Needs_Action` folder with YAML frontmatter added

### Event: File Status Update
- **Trigger**: Internal state change or external action
- **Conditions**: Valid status transition according to state machine rules
- **Guarantee**: Metadata in YAML frontmatter will be updated consistently
- **Post-condition**: File location and metadata will reflect the new state

## File Structure Contract

### Input Files
- **Location**: `01_Inbox` folder
- **Format**: `.txt` or `.md` files
- **Requirements**: Valid filename (compliant with filesystem restrictions)
- **Size Limit**: Up to 10MB per file

### Output Files
- **Location**: Determined by state in folder-based system
- **Format**: Markdown with YAML frontmatter
- **Metadata Requirements**: Must include `id`, `status`, `created`, `updated` fields

## Folder State Contract

### 01_Inbox
- **Purpose**: Entry point for new tasks
- **Operations**: Read-only for system, write for users
- **Guarantees**: Files will be processed in order of creation
- **Error Handling**: Invalid files will be logged and ignored

### 02_Needs_Action
- **Purpose**: Tasks awaiting AI processing
- **Operations**: Read by AI, moved by system
- **Guarantees**: Files will remain until AI processes them
- **Error Handling**: Processing errors will be logged

### 03_Pending_Approval
- **Purpose**: Tasks completed by AI, awaiting human approval
- **Operations**: Read by humans, moved by system upon approval
- **Guarantees**: Files will remain until approved
- **Error Handling**: Approval errors will be logged

### 04_Approved
- **Purpose**: Approved tasks ready for finalization
- **Operations**: Read by system, moved by system
- **Guarantees**: Files will be processed to completion
- **Error Handling**: Finalization errors will be logged

### 05_Done
- **Purpose**: Completed tasks
- **Operations**: Read-only archive
- **Guarantees**: Files will remain unchanged
- **Error Handling**: Archive integrity maintained

## Metadata Contract

### Required Fields
Each file must contain the following YAML frontmatter fields:

```yaml
id: string           # Unique identifier (UUID format recommended)
status: string       # Current status (inbox|needs-action|pending-approval|approved|done)
created: string      # ISO 8601 timestamp of creation
updated: string      # ISO 8601 timestamp of last update
```

### Optional Fields
Files may contain additional fields as needed:

```yaml
original_filename: string     # Original filename before sanitization
processed_by_ai: boolean      # Whether AI has processed the task
approved_by_human: boolean    # Whether human has approved the task
checklist_completed: boolean  # Whether all checklist items are marked complete
```

## Error Conditions

### File Processing Error
- **Condition**: File cannot be processed due to corruption or invalid format
- **Response**: File is moved to `errors` folder with error details in metadata
- **Notification**: Error is logged to system log

### State Transition Error
- **Condition**: Attempt to make invalid state transition
- **Response**: Operation is rejected, file remains in current state
- **Notification**: Error is logged to system log

### File System Error
- **Condition**: Cannot access or modify files due to permissions or disk issues
- **Response**: System pauses processing and logs error
- **Notification**: Error is logged to system log

## Performance Guarantees

- **Processing Time**: New files will be moved from Inbox to Needs Action within 10 seconds
- **Availability**: System will maintain 99% uptime during standard business hours
- **Throughput**: System can handle up to 100 file operations per minute
- **Consistency**: File state and metadata will remain synchronized

## Security Considerations

- **Access Control**: Only authorized users can write to the Inbox folder
- **Data Validation**: All file contents are treated as untrusted input
- **Audit Trail**: All state changes are recorded in system logs
- **Privacy**: No personal information is stored beyond what's provided in the files