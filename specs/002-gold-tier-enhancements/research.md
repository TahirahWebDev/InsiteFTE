# Research: Gold Tier Agentic Loop

**Feature**: Gold Tier Agentic Loop
**Date**: 2026-01-23
**Author**: AI Assistant

## Overview

This document captures the research findings for implementing the Gold Tier Agentic Loop system. It addresses all technical unknowns and clarifies implementation decisions based on the feature specification and project requirements.

## Key Decisions

### 1. Agentic Loop Implementation Approach

**Decision**: Implement a periodic polling loop with configurable interval (default 60 seconds)

**Rationale**: A periodic polling approach provides predictable behavior and allows for consistent monitoring of the 02_Needs_Action folder. While event-based monitoring is more responsive, a polling approach gives the AI agent more control over timing and allows for batching operations.

**Alternatives considered**:
- Pure event-driven: More responsive but harder to control timing
- Hybrid approach: Combines both but adds complexity
- Push notifications: Would require external infrastructure

### 2. Tool Execution Mechanism

**Decision**: JSON command blocks in Markdown files for tool execution

**Rationale**: Using JSON blocks within Markdown files allows the AI to express tool calls in a structured way while maintaining compatibility with the Obsidian ecosystem. This approach is transparent and auditable.

**Example format**:
```json
{
  "tool_call": {
    "name": "search_web",
    "parameters": {
      "query": "latest developments in AI agents"
    }
  }
}
```

**Alternatives considered**:
- Function calling APIs: More complex to implement
- Natural language parsing: Less reliable and harder to validate
- Separate command files: Would complicate the file structure

### 3. Obsidian DataviewJS Integration

**Decision**: Use DataviewJS for dynamic dashboard updates

**Rationale**: DataviewJS provides powerful scripting capabilities within Obsidian, allowing for real-time updates of the Mission Control dashboard. It can track thought processes and tool outputs dynamically.

**Alternatives considered**:
- Static Dataview queries: Less dynamic and informative
- External dashboard: Would break the local-first principle
- Manual updates: Not scalable or automated

### 4. State Machine Extension

**Decision**: Extend existing state machine with 06_Researching and 07_Reviewing states

**Rationale**: Building on the existing state machine maintains consistency while adding the required capabilities for research and review phases. This preserves backward compatibility.

**Alternatives considered**:
- Separate workflow system: Would create complexity
- Modifying existing states: Would break existing functionality

### 5. Memory Management Implementation

**Decision**: Maintain Memory.md file with structured entries for long-term goal tracking

**Rationale**: A dedicated memory file allows the AI to maintain context across different tasks and sessions. The structured approach enables efficient retrieval of relevant information.

**Alternatives considered**:
- Embedding in task files: Would分散 information
- Database storage: Would violate local-first principle
- Temporary storage: Would lose information between sessions

## Technical Deep Dive

### Agentic Loop Controller Implementation

The main controller will implement a loop that periodically checks the 02_Needs_Action folder:

```python
import asyncio
import time
from pathlib import Path

async def agentic_loop(interval_seconds=60):
    while True:
        await process_needs_action_folder()
        await asyncio.sleep(interval_seconds)
```

### Tool Registry and Execution

The system will implement a registry pattern for tools:

```python
class ToolRegistry:
    def __init__(self):
        self.tools = {}
    
    def register_tool(self, name, tool_func):
        self.tools[name] = tool_func
    
    async def execute_tool(self, tool_name, parameters):
        if tool_name in self.tools:
            return await self.tools[tool_name](**parameters)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
```

### JSON Parser for Tool Calls

The system will include a parser to extract and validate tool calls from Markdown content:

```python
import json
import re

def extract_json_blocks(markdown_content):
    pattern = r'```json\s*\n(\{(?:[^{}]|{[^{}]*})*\})\s*\n```'
    matches = re.findall(pattern, markdown_content, re.MULTILINE)
    return [json.loads(match) for match in matches]
```

### Obsidian Mission Control Dashboard

The dashboard will use DataviewJS to display real-time information:

```javascript
// Example DataviewJS query for Mission Control
dv.header(2, "Current Thought Process");
let thoughtProcess = dv.pages().file.lists.where(l => l.status == "thinking").text;
dv.list(thoughtProcess);

dv.header(2, "Recent Tool Outputs");
let toolOutputs = dv.pages().file.lists.where(l => l.tool_output != undefined);
dv.table(["Tool", "Output", "Time"], 
    toolOutputs.map(t => [t.tool_name, t.tool_output, t.completed_time]));
```

## Risk Assessment

### Potential Issues

1. **Resource consumption**: Continuous polling could consume system resources
   - *Mitigation*: Configurable polling interval and idle detection

2. **Tool execution security**: Executing arbitrary tools could pose security risks
   - *Mitigation*: Strict tool registration, parameter validation, and sandboxing

3. **JSON parsing vulnerabilities**: Malformed JSON could crash the system
   - *Mitigation*: Robust error handling and input validation

4. **Memory file bloat**: Accumulation of memory entries could slow performance
   - *Mitigation*: Periodic cleanup and compression of older entries

## Dependencies Summary

- `watchdog`: For file system monitoring (existing)
- `ruamel.yaml`: For YAML frontmatter manipulation (existing)
- `asyncio`: For asynchronous operations (built-in)
- `json`: For JSON parsing (built-in)
- `re`: For pattern matching (built-in)
- `obsidian-api-wrapper`: For Obsidian integration (new requirement)

## Next Steps

1. Implement the main agentic loop controller
2. Create the tool registry and execution system
3. Develop the JSON parser for tool calls
4. Build the state machine extensions
5. Implement the memory management system
6. Integrate with Obsidian DataviewJS for dashboard
7. Create comprehensive tests