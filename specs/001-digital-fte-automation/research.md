# Research: Digital FTE Automation

**Feature**: Digital FTE Automation
**Date**: 2026-01-23
**Author**: AI Assistant

## Overview

This document captures the research findings for implementing the Digital FTE Automation system. It addresses all technical unknowns and clarifies implementation decisions based on the feature specification and project requirements.

## Key Decisions

### 1. File System Monitoring Approach

**Decision**: Use the `watchdog` library for file system monitoring

**Rationale**: The `watchdog` library is a robust, cross-platform Python library specifically designed for monitoring file system events. It provides an Observer pattern implementation that efficiently watches directories for changes without consuming excessive resources. It's well-maintained and widely adopted in the Python community.

**Alternatives considered**:
- Polling file system at intervals: Less efficient and introduces delays
- Using platform-specific APIs directly: Would require separate implementations for each OS
- Using `inotify` directly on Linux: Not cross-platform compatible

### 2. Dependency Management

**Decision**: Use `uv` for dependency management

**Rationale**: `uv` is a modern, lightning-fast Python package installer and resolver written in Rust. It offers significant performance improvements over pip and pip-tools, making development cycles faster. It's becoming increasingly popular in the Python ecosystem for its speed and reliability.

**Alternatives considered**:
- Traditional pip + requirements.txt: Slower, less reliable dependency resolution
- Poetry: Good but heavier than needed for this project
- Pipenv: Good but slower than uv

### 3. Obsidian Integration

**Decision**: Use YAML frontmatter for metadata and Dataview plugin for dashboard queries

**Rationale**: YAML frontmatter is the standard way to add metadata to Obsidian notes. The Dataview plugin is the most popular and powerful way to query and display data in Obsidian. Together, they provide a flexible and powerful way to track task status and other metadata.

**Alternatives considered**:
- Using tags only: Less structured and harder to query
- Using properties in document body: Less standardized than frontmatter
- Other Obsidian plugins: Dataview is the most mature and capable

### 4. File Movement Strategy

**Decision**: Direct file movement with atomic operations

**Rationale**: Moving files directly between folders is the most straightforward approach for implementing the state machine. Python's `shutil.move()` provides atomic operations that are safe and reliable across platforms.

**Alternatives considered**:
- Copy + delete: More complex and uses more disk space temporarily
- Symbolic links: More complex and might confuse users
- Database tracking: Contradicts the local-first principle

### 5. Filename Sanitization

**Decision**: Remove or replace problematic characters while preserving readability

**Rationale**: Different operating systems have different restrictions on valid filename characters. Sanitizing filenames prevents errors when moving files across the system. The approach should maintain readability while ensuring compatibility.

**Characters to sanitize**:
- `< > : " | ? *` (Windows restrictions)
- Control characters (ASCII 0-31)
- Leading/trailing spaces and periods (some systems)

### 6. Timestamp Format for Duplicates

**Decision**: Use ISO 8601 format with microseconds for uniqueness

**Rationale**: ISO 8601 format is internationally recognized and sortable. Including microseconds minimizes the chance of collisions even with rapid file creation.

**Format**: `{original_name}_{YYYYMMDDHHMMSSffffff}.{extension}`

## Technical Deep Dive

### Watchdog Event Handler Implementation

The core of the system will be an event handler that extends `FileSystemEventHandler` from the `watchdog` library. It will specifically listen for `on_created` events in the 01_Inbox folder.

```python
from watchdog.events import FileSystemEventHandler

class InboxHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(('.txt', '.md')):
            # Process the new file
            process_inbox_file(event.src_path)
```

### YAML Frontmatter Addition

For adding metadata to files, we'll use the `ruamel.yaml` library which preserves formatting better than other YAML libraries:

```python
from ruamel.yaml import YAML
import io

def add_frontmatter(file_path, metadata):
    yaml = YAML()
    yaml.preserve_quotes = True
    
    with open(file_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        
        # Create frontmatter
        frontmatter_block = {'status': 'needs-action', 'created': datetime.now().isoformat()}
        
        # Write frontmatter and original content back
        f.seek(0)
        f.write('---\n')
        yaml.dump(frontmatter_block, f)
        f.write('---\n')
        f.write(content)
        f.truncate()
```

### Dataview Query for Dashboard

The dashboard will use a Dataview query to show files in different states:

```javascript
TABLE created AS "Created Date"
WHERE status = "needs-action" OR status = "pending-approval"
SORT created DESC
```

## Risk Assessment

### Potential Issues

1. **Race conditions**: Multiple files created simultaneously could cause issues
   - *Mitigation*: Use thread-safe operations and consider queuing

2. **Permission errors**: Insufficient permissions to move files
   - *Mitigation*: Proper error handling and logging

3. **Corrupted files**: Files that can't be processed
   - *Mitigation*: Isolate problematic files and log errors

4. **Large files**: Very large files taking too long to process
   - *Mitigation*: Set file size limits or process asynchronously

## Dependencies Summary

- `watchdog`: For file system monitoring
- `ruamel.yaml`: For YAML frontmatter manipulation
- `pathlib`: For cross-platform path operations (built-in)
- `datetime`: For timestamp generation (built-in)
- `re`: For filename sanitization (built-in)

## Next Steps

1. Implement the core watcher script
2. Create utility functions for file handling, sanitization, and metadata
3. Set up the Obsidian vault structure
4. Test with sample files
5. Create comprehensive tests