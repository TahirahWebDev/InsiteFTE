# Technical Branding Assistant Setup

## Overview
The Technical Branding Assistant is an automated system that takes tech topics from your Inbox, researches them online, and generates professional LinkedIn content along with simplified study guides.

## Prerequisites
- Python 3.12+
- Tavily API key for web search functionality

## Setup

1. **Install dependencies**:
   ```bash
   pip install -e .
   ```

2. **Set up your API key**:
   Create a `.env` file in the root directory with your Tavily API key:
   ```
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

3. **Run the file watcher** (in one terminal):
   ```bash
   python -m scripts.watcher
   ```

4. **Run the agent logic** (in another terminal):
   ```bash
   python run_agent.py
   ```

## Usage

1. Place a text file with a tech topic in the `01_Inbox` folder (e.g., "Next.js 15 features.txt") - Note: Only .txt and .md files are processed
2. Run the file watcher in one terminal: `python -m scripts.watcher`
3. Run the agent in another terminal: `python run_agent.py`
4. The file watcher will automatically move the file to `02_Needs_Action`
5. The agent will process the file, research the topic online, and create:
   - A LinkedIn post draft
   - A Simplified Study Guide
6. The results will be saved in the `03_Pending_Approval` folder for review
7. Manually move approved files to `04_Approved` and then to `05_Done` when completed

## Components

- `scripts/tools/web_search.py`: Handles web search functionality using Tavily API
- `scripts/agent_logic.py`: Contains the main logic for processing topics and generating content
- `scripts/watcher.py`: Monitors the Inbox and moves files between folders
- `run_agent.py`: Runs the agent logic to process files in Needs Action folder