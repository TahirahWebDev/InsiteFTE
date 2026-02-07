# AI Employee Vault - Technical Branding Assistant

AI Employee Vault is an automated system that functions as a Technical Branding Assistant. It takes tech topics from your Inbox, researches them online, and generates professional LinkedIn content along with simplified study guides. The system uses a folder-based state machine to manage the workflow from intake to completion.

## Features

- Automated processing of tech topics from text files
- Online research using Tavily API for comprehensive information gathering
- Generation of professional LinkedIn posts from technical subjects
- Creation of simplified study guides for complex topics
- Folder-based state machine for workflow management (Inbox → Needs Action → Pending Approval → Approved → Done)
- Continuous monitoring of the Inbox folder for new tasks
- YAML frontmatter metadata to track file status and processing state

## Prerequisites

- Python 3.12 or higher
- Tavily API key for web research functionality
- Windows, macOS, or Linux operating system

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd AI_Employee_Vault
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Set up the project structure:
   The following folder structure is used for the state machine:
   ```
   AI_Employee_Vault/
   ├── 01_Inbox/           # New files placed here for processing
   ├── 02_Needs_Action/    # Files awaiting AI processing
   ├── 03_Pending_Approval/ # Files completed by AI, awaiting human review
   ├── 04_Approved/        # Files approved by human reviewer
   ├── 05_Done/            # Completed files
   ├── Home.md             # Dashboard for monitoring tasks
   └── Handbook.md         # Processing guidelines for the AI
   ```

## Configuration

1. Set up your API key:
   Create a `.env` file in the root directory with your Tavily API key:
   ```
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

2. Configure the system paths:
   Edit the `scripts/config.py` file to set the correct paths if needed:
   ```python
   # Path to your project directory (default is current directory)
   VAULT_PATH = "path/to/your/AI_Employee_Vault"
   ```

## Usage

There are multiple ways to run the system:

### Option 1: Separate Processes (Recommended for development)
1. Start the file watcher in one terminal:
   ```bash
   python -m scripts.watcher
   ```
   This monitors the `01_Inbox` folder and moves new `.txt` or `.md` files to `02_Needs_Action`.

2. Start the AI agent in another terminal:
   ```bash
   python run_agent.py
   ```
   This processes files in the `02_Needs_Action` folder, performs research, and creates content.

### Option 2: Combined Runner
Run both the watcher and agent in a single process:
```bash
python combined_runner.py
```

### Option 3: Demo Mode
Run a demonstration of the workflow:
```bash
python demo_agent.py
```

## Example Workflow

1. User creates `Next.js 15 features.txt` with a tech topic
2. User places file in `01_Inbox`
3. Watcher detects file and moves it to `02_Needs_Action` with metadata:
   ```yaml
   ---
   id: task-12345
   status: needs-action
   created: 2026-02-08T10:00:00
   updated: 2026-02-08T10:00:00
   ---
   ```
4. AI agent processes the file, researches "Next.js 15 features" online
5. AI generates:
   - A professional LinkedIn post about Next.js 15 features
   - A simplified study guide explaining the concepts
6. AI updates status to `pending-approval` and moves to `03_Pending_Approval`
7. Human reviewer approves the generated content
8. User moves file to `04_Approved`
9. System finalizes and moves to `05_Done`

## Components

- `scripts/watcher.py`: Monitors the Inbox and moves files between folders based on state
- `scripts/agent_logic.py`: Main AI processing logic for researching topics and generating content
- `scripts/tools/web_search.py`: Handles web search functionality using Tavily API
- `run_agent.py`: Runs the AI agent to process files in Needs Action folder
- `combined_runner.py`: Runs both watcher and agent in a single process
- `demo_agent.py`: Demonstrates the workflow for testing purposes
- `Handbook.md`: Contains processing guidelines for the AI employee
- `Home.md`: Dashboard for monitoring active tasks

## Troubleshooting

### API Key Issues
- Ensure your Tavily API key is correctly set in the `.env` file
- Verify that your API key has sufficient quota for web searches

### Files Not Being Processed
- Check that both the watcher and agent are running
- Verify that the file extension is `.txt` or `.md`
- Ensure the file is not too large (maximum 10MB)

### Agent Not Responding
- Check that the agent script is running: `python run_agent.py`
- Look at the log file (`digital_fte.log`) for error messages
- Verify that your internet connection is working for web searches

### Permission Errors
- Ensure the script has read/write access to all project directories
- On some systems, you may need to run the script with elevated privileges

## Stopping the Service

To stop the watcher or agent service, press `Ctrl+C` in the terminal where it's running.