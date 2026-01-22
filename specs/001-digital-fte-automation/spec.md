# Feature Specification: Digital FTE Automation

**Feature Branch**: `001-digital-fte-automation`
**Created**: 2026-01-23
**Status**: Draft
**Input**: User description: "Specify a Digital FTE (Full-Time Equivalent) System for the Bronze Tier hackathon requirement. Project Goal: To create an autonomous AI employee that manages tasks via an Obsidian vault using a folder-based state machine. Functional Requirements: Folder Architecture: Create a system with five core folders: 01_Inbox, 02_Needs_Action, 03_Pending_Approval, 04_Approved, and 05_Done. Watcher Automation: A Python-based 'Watcher' script that monitors the 01_Inbox folder. When a new .txt or .md file is added, the script must automatically move it to 02_Needs_Action. Dashboard UI: An Obsidian 'Home' dashboard that lists the files currently sitting in 02_Needs_Action and 03_Pending_Approval. Handbook: A 'Handbook.md' file that contains operating instructions for the AI on how to process different types of requests (e.g., meeting summaries vs. task lists). Technical Constraints: Use Python 3.12+ and the watchdog library for file system events. All data must be stored in Markdown format to ensure the vault remains the single source of truth. The system must follow a Human-in-the-Loop model: no file should move to 'Done' without a plan being created and approved in the 'Approved' folder. User Experience: > The user should be able to drop a note into the Inbox and see it reflected on the Obsidian Dashboard as a task ready for the AI to process."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - File Processing Automation (Priority: P1)

A user drops a note into the 01_Inbox folder, and the system automatically moves it to 02_Needs_Action where it appears on the Obsidian Dashboard for the AI to process. This enables seamless task intake without manual intervention.

**Why this priority**: This is the core functionality of the system - allowing users to easily submit tasks to the AI employee through the Obsidian vault.

**Independent Test**: Can be fully tested by placing a .txt or .md file in the 01_Inbox folder and verifying it gets moved to 02_Needs_Action and appears on the dashboard. This delivers the core value of automated task intake.

**Acceptance Scenarios**:

1. **Given** a new .txt or .md file is added to the 01_Inbox folder, **When** the Watcher script detects the file, **Then** the file is automatically moved to the 02_Needs_Action folder
2. **Given** a file has been moved to 02_Needs_Action, **When** the user views the Obsidian Dashboard, **Then** the file appears in the list of tasks needing action

---

### User Story 2 - Task Monitoring Dashboard (Priority: P2)

A user can view the Obsidian 'Home' dashboard to see all files currently in 02_Needs_Action and 03_Pending_Approval, allowing them to monitor the status of tasks being processed by the AI employee.

**Why this priority**: This provides visibility into the system's workload and allows users to track the progress of their requests.

**Independent Test**: Can be tested by verifying that the dashboard accurately displays files in the 02_Needs_Action and 03_Pending_Approval folders. This delivers the value of task visibility and status tracking.

**Acceptance Scenarios**:

1. **Given** files exist in the 02_Needs_Action folder, **When** the user opens the Obsidian Dashboard, **Then** those files are listed on the dashboard
2. **Given** files exist in the 03_Pending_Approval folder, **When** the user opens the Obsidian Dashboard, **Then** those files are listed on the dashboard

---

### User Story 3 - Human-in-the-Loop Approval (Priority: P3)

When the AI employee completes work on a task, it creates a plan in the 04_Approved folder that requires human approval before the task can be marked as done, ensuring quality control and human oversight.

**Why this priority**: This ensures quality and maintains human oversight of the AI's work, which is critical for trust and accuracy.

**Independent Test**: Can be tested by verifying that files don't move to 05_Done without first having an approved plan in 04_Approved. This delivers the value of quality assurance and human oversight.

**Acceptance Scenarios**:

1. **Given** a task is completed by the AI, **When** the AI creates an approval plan, **Then** the file is moved to 03_Pending_Approval
2. **Given** a file is in 03_Pending_Approval, **When** a human approves the plan, **Then** the file is moved to 04_Approved and eventually to 05_Done

---

### Edge Cases

- What happens when the Watcher script encounters a corrupted file in the inbox?
- How does the system handle multiple files being added to the inbox simultaneously?
- What occurs if the destination folder is full or inaccessible?
- How does the system handle files with special characters in their names? (Answer: Sanitize special characters during file movement)
- What happens when there are duplicate filenames in the workflow? (Answer: Append timestamp to duplicate filenames)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST monitor the 01_Inbox folder for new .txt or .md files using a Python-based Watcher script
- **FR-002**: System MUST automatically move new .txt or .md files from 01_Inbox to 02_Needs_Action when detected. When duplicate filenames exist, append timestamp to ensure uniqueness.
- **FR-003**: System MUST maintain a dashboard in Obsidian that lists files in 02_Needs_Action and 03_Pending_Approval folders
- **FR-004**: System MUST store all data in Markdown format to ensure the vault remains the single source of truth. All files MUST include standard YAML frontmatter with ID, creation date, and status for proper tracking.
- **FR-005**: System MUST follow a Human-in-the-Loop model where no file moves to 05_Done without a plan being created and approved in 04_Approved folder. Additionally, all checklist items in the task must be marked complete.
- **FR-006**: System MUST include a Handbook.md file containing operating instructions for the AI on how to process different types of requests
- **FR-007**: System MUST use Python 3.12+ and the watchdog library for file system event detection
- **FR-008**: System MUST ensure that the folder-based state machine operates reliably with five core folders: 01_Inbox, 02_Needs_Action, 03_Pending_Approval, 04_Approved, and 05_Done
- **FR-009**: System MUST sanitize special characters in filenames during file movement operations to maintain system stability
- **FR-010**: System MUST update the status in the file's frontmatter to "planning-ready" when the AI has completed initial processing and the task is ready for the planning phase

### Key Entities

- **Task File**: A .txt or .md file representing a unit of work that moves through the state machine; contains the original request or information to be processed by the AI. Includes standard YAML frontmatter with ID, creation date, and status for proper tracking.
- **Folder State Machine**: Five core folders (01_Inbox, 02_Needs_Action, 03_Pending_Approval, 04_Approved, 05_Done) that represent the lifecycle stages of a task
- **Watcher Script**: A Python-based monitoring component that detects new files in the 01_Inbox folder and moves them to 02_Needs_Action. When duplicate filenames exist, appends timestamp to ensure uniqueness. Sanitizes special characters in filenames during movement.
- **Dashboard**: The Obsidian 'Home' interface that displays files currently in 02_Needs_Action and 03_Pending_Approval folders
- **Handbook**: The Handbook.md file containing operating instructions for the AI on how to process different types of requests
- **Approval Plan**: A document created by the AI that outlines the work completed and requires human approval before finalizing the task

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can drop a note into the Inbox and see it reflected on the Obsidian Dashboard as a task ready for the AI to process within 10 seconds
- **SC-002**: The system processes 100% of new .txt and .md files dropped into the 01_Inbox folder without manual intervention
- **SC-003**: The dashboard accurately displays all files in 02_Needs_Action and 03_Pending_Approval folders in real-time
- **SC-004**: 100% of tasks follow the Human-in-the-Loop model with proper approval before reaching the 05_Done state
- **SC-005**: The system maintains 99% uptime during standard business hours for file monitoring and processing

## Clarifications

### Session 2026-01-23

- Q: How should the Python watcher script handle duplicate filenames in the workflow? → A: Append timestamp to duplicate filenames
- Q: What specific metadata or frontmatter format is required for the Obsidian files so the dashboard can track them correctly? → A: Standard YAML frontmatter with ID, creation date, and status
- Q: How should the AI signal to the user that a task in 02_Needs_Action is ready for the 'Planning' phase? → A: Update status in frontmatter to "planning-ready"
- Q: What are the specific criteria for a task to be considered 'Completed' and moved to 05_Done? → A: Approved plan exists AND all checklist items marked complete
- Q: How should the system handle files with special characters in their names? → A: Sanitize special characters during file movement