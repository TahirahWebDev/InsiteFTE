# Quickstart Guide: Gold Tier Agentic Loop

**Feature**: Gold Tier Agentic Loop
**Date**: 2026-01-23
**Author**: AI Assistant

## Overview

This guide provides instructions for setting up and using the Gold Tier Agentic Loop system. The system transforms the Digital FTE from a simple watcher to an autonomous agent that periodically checks the 02_Needs_Action folder, executes tools via JSON commands, and integrates with Obsidian's DataviewJS for advanced dashboard capabilities.

## Prerequisites

- Python 3.12 or higher
- Obsidian installed with Dataview plugin enabled
- Windows, macOS, or Linux operating system
- Administrative access to install Python packages

## Installation

### 1. Clone or Download the Repository

```bash
git clone <repository-url>
cd gold-tier-agentic-loop
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
cd gold-tier-agentic-loop

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install project dependencies
uv pip install -e .
```

### 4. Set up the Extended Obsidian Vault Structure

Create the following folder structure in your Obsidian vault:

```
vault-root/
├── 01_Inbox/
├── 02_Needs_Action/
├── 03_Pending_Approval/
├── 04_Approved/
├── 05_Done/
├── 06_Researching/
├── 07_Reviewing/
├── Home.md
├── Mission-Control.md
└── Memory.md
```

## Configuration

### 1. Configure the Agentic Loop

Edit the `config.py` file to set the correct paths and parameters:

```python
# Path to your Obsidian vault
VAULT_PATH = "/path/to/your/obsidian/vault"

# Polling interval in seconds (default: 60 seconds)
POLLING_INTERVAL = 60

# Folder names (can be customized if needed)
INBOX_FOLDER = "01_Inbox"
NEEDS_ACTION_FOLDER = "02_Needs_Action"
PENDING_APPROVAL_FOLDER = "03_Pending_Approval"
APPROVED_FOLDER = "04_Approved"
DONE_FOLDER = "05_Done"
RESEARCHING_FOLDER = "06_Researching"
REVIEWING_FOLDER = "07_Reviewing"

# Memory file path
MEMORY_FILE = "Memory.md"
```

### 2. Set up the Mission Control Dashboard

Add the following DataviewJS code to your `Mission-Control.md` file to create the dashboard:

```javascript
<div class="mission-control">

## 🤖 AI Status
Status: Active | Last Check: <% dv.current().file.cday %> | Next Check: <% new Date(Date.now() + 60000) %>

## 📋 Current Tasks
```dataview
TABLE status AS "Status", created AS "Created"
FROM "02_Needs_Action"
SORT created DESC
```

## 🧠 Active Thought Processes
```dataviewjs
const pages = dv.pages('"02_Needs_Action"');
for (let page of pages) {
    if (page.thought_process) {
        dv.header(4, page.file.name);
        dv.paragraph(page.thought_process);
    }
}
```

## 🔧 Recent Tool Executions
```dataview
TABLE tool_name AS "Tool", execution_time AS "Time", status AS "Status"
FROM "06_Researching" OR "07_Reviewing"
WHERE tool_executions
SORT execution_time DESC
LIMIT 10
```

## 📚 Memory Highlights
```dataviewjs
const memoryFile = dv.page("Memory.md");
if (memoryFile && memoryFile.highlights) {
    dv.list(memoryFile.highlights);
}
```

</div>
```

## Usage

### 1. Starting the Agentic Loop

Run the agentic loop to begin monitoring the 02_Needs_Action folder:

```bash
python agentic_loop/main.py
```

The script will continuously monitor the `02_Needs_Action` folder every 60 seconds (or as configured) for tasks to process.

### 2. Using Tool Execution

To have the AI execute tools, include JSON blocks in the task files:

```json
{
  "tool_call": {
    "name": "search_web",
    "parameters": {
      "query": "latest developments in AI agents",
      "num_results": 3
    }
  }
}
```

### 3. Submitting a Task

To submit a task to the Gold Tier Agentic Loop:

1. Create a new `.txt` or `.md` file with your task
2. Place it in the `01_Inbox` folder in your Obsidian vault
3. The system will automatically:
   - Sanitize the filename
   - Add YAML frontmatter with metadata
   - Move the file to `02_Needs_Action`
   - The agentic loop will pick it up during its next cycle

### 4. Monitoring Progress

Monitor the AI's progress using the Mission Control dashboard:
- Check the `Mission-Control.md` page in Obsidian
- View current tasks, thought processes, and tool executions
- Track the AI's progress through the state machine

## Example Workflow

1. User creates `research-project.md` with a research request
2. User places file in `01_Inbox`
3. System detects file and moves it to `02_Needs_Action` with metadata:
   ```yaml
   ---
   id: task-12345
   status: needs-action
   created: 2026-01-23T10:00:00
   updated: 2026-01-23T10:00:00
   thought_process: "Need to research the latest developments in AI agents..."
   ---
   ```
4. Agentic loop picks up the task during its next cycle
5. AI decides it needs to search the web and adds a tool call:
   ```json
   {
     "tool_call": {
       "name": "search_web",
       "parameters": {
         "query": "latest developments in AI agents",
         "num_results": 5
       }
   }
   ```
6. Tool executes and results are added to the file
7. Task moves to `06_Researching` based on AI's assessment
8. After research, task moves to `07_Reviewing` for quality assessment
9. After review, task moves to `03_Pending_Approval` for human review
10. User approves the task, and it moves to `04_Approved` and eventually `05_Done`

## Troubleshooting

### Agentic Loop Not Responding

- Ensure the script is running: `python agentic_loop/main.py`
- Check that the vault path in `config.py` is correct
- Verify that the `02_Needs_Action` folder exists

### Tools Not Executing

- Ensure the JSON blocks are properly formatted
- Check that the tool names are registered in the system
- Verify that the parameters are valid for the specific tool

### Files Not Appearing on Dashboard

- Ensure the Dataview plugin is enabled in Obsidian
- Check that the YAML frontmatter is correctly formatted
- Verify that the DataviewJS code in `Mission-Control.md` is correct

### Permission Errors

- Ensure the script has read/write access to the vault directory
- On some systems, you may need to run the script with elevated privileges

## Stopping the Service

To stop the agentic loop service, press `Ctrl+C` in the terminal where it's running.