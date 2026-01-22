# Quickstart Guide: Digital FTE Automation

**Feature**: Digital FTE Automation
**Date**: 2026-01-23
**Author**: AI Assistant

## Overview

This guide provides a quick introduction to setting up and using the Digital FTE Automation system. The system automates task management through an Obsidian vault using a folder-based state machine.

## Prerequisites

- Python 3.12 or higher
- Obsidian installed with Dataview plugin enabled
- Windows, macOS, or Linux operating system
- Administrative access to install Python packages

## Installation

### 1. Clone or Download the Repository

```bash
git clone <repository-url>
cd digital-fte-automation
```

### 2. Install uv (if not already installed)

```bash
# On Windows
pip install uv

# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Set up the Project Environment

```bash
# Navigate to the project directory
cd digital-fte-automation

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install project dependencies
uv pip install watchdog ruamel.yaml
```

### 4. Set up the Obsidian Vault Structure

Create the following folder structure in your Obsidian vault:

```
vault-root/
├── 01_Inbox/
├── 02_Needs_Action/
├── 03_Pending_Approval/
├── 04_Approved/
├── 05_Done/
├── Home.md
└── Handbook.md
```

## Configuration

### 1. Configure the Watcher Script

Edit the `config.py` file to set the correct paths:

```python
# Path to your Obsidian vault
VAULT_PATH = "/path/to/your/obsidian/vault"

# Folder names (can be customized if needed)
INBOX_FOLDER = "01_Inbox"
NEEDS_ACTION_FOLDER = "02_Needs_Action"
PENDING_APPROVAL_FOLDER = "03_Pending_Approval"
APPROVED_FOLDER = "04_Approved"
DONE_FOLDER = "05_Done"
```

### 2. Set up the Dashboard

Add the following Dataview query to your `Home.md` file to display tasks:

```javascript
## Tasks Needing Action
TABLE created AS "Created Date"
FROM "02_Needs_Action"
WHERE status = "needs-action"
SORT created DESC

## Tasks Pending Approval
TABLE created AS "Created Date" 
FROM "03_Pending_Approval"
WHERE status = "pending-approval"
SORT created DESC
```

## Usage

### 1. Starting the Watcher

Run the watcher script to begin monitoring the Inbox folder:

```bash
python scripts/watcher.py
```

The script will continuously monitor the `01_Inbox` folder for new `.txt` or `.md` files.

### 2. Submitting a Task

To submit a task to the Digital FTE:

1. Create a new `.txt` or `.md` file
2. Place it in the `01_Inbox` folder in your Obsidian vault
3. The system will automatically:
   - Sanitize the filename
   - Add YAML frontmatter with metadata
   - Move the file to `02_Needs_Action`

### 3. Processing Tasks

The AI will process tasks in the `02_Needs_Action` folder. When processing is complete:

1. The AI updates the file's status to `pending-approval`
2. The file is moved to `03_Pending_Approval`
3. The task appears on your dashboard for review

### 4. Approving Tasks

To approve a task:

1. Review the completed work in the `03_Pending_Approval` folder
2. Move the file to `04_Approved` when satisfied
3. The system will eventually move it to `05_Done` after finalization

## Example Workflow

1. User creates `meeting-notes.txt` with meeting details
2. User places file in `01_Inbox`
3. Watcher detects file and moves it to `02_Needs_Action` with metadata:
   ```yaml
   ---
   id: task-12345
   status: needs-action
   created: 2026-01-23T10:00:00
   updated: 2026-01-23T10:00:00
   ---
   ```
4. AI processes the meeting notes
5. AI updates status to `pending-approval` and moves to `03_Pending_Approval`
6. User reviews the processed notes on the dashboard
7. User moves file to `04_Approved`
8. System finalizes and moves to `05_Done`

## Troubleshooting

### Watcher Not Responding

- Ensure the script is running: `python scripts/watcher.py`
- Check that the vault path in `config.py` is correct
- Verify that the `01_Inbox` folder exists

### Files Not Appearing on Dashboard

- Ensure the Dataview plugin is enabled in Obsidian
- Check that the YAML frontmatter is correctly formatted
- Verify that the Dataview query in `Home.md` is correct

### Permission Errors

- Ensure the script has read/write access to the vault directory
- On some systems, you may need to run the script with elevated privileges

## Stopping the Service

To stop the watcher service, press `Ctrl+C` in the terminal where it's running.