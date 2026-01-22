---

description: "Task list template for feature implementation"
---

# Tasks: Digital FTE Automation

**Input**: Design documents from `/specs/001-digital-fte-automation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in root directory
- [X] T002 [P] Initialize pyproject.toml with Python 3.12+ and dependencies (watchdog, ruamel.yaml)
- [X] T003 [P] Create scripts/ directory structure with watcher.py, config.py, and utils/ subdirectory

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T004 Create utils/file_handler.py module for file processing operations
- [X] T005 [P] Create utils/sanitizer.py module for filename sanitization operations
- [X] T006 [P] Create utils/metadata.py module for YAML frontmatter operations
- [X] T007 Create config.py with vault path and folder configuration settings
- [X] T008 Create base exception classes for the system in scripts/exceptions.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - File Processing Automation (Priority: P1) 🎯 MVP

**Goal**: Enable seamless task intake by automatically moving files from 01_Inbox to 02_Needs_Action when detected

**Independent Test**: Can be fully tested by placing a .txt or .md file in the 01_Inbox folder and verifying it gets moved to 02_Needs_Action and appears on the dashboard. This delivers the core value of automated task intake.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [X] T009 [P] [US1] Unit test for file_handler.py in tests/unit/test_file_handler.py
- [X] T010 [P] [US1] Unit test for sanitizer.py in tests/unit/test_sanitizer.py

### Implementation for User Story 1

- [X] T011 [P] [US1] Create InboxHandler class in scripts/watcher.py that extends FileSystemEventHandler
- [X] T012 [US1] Implement on_created event handler in scripts/watcher.py to detect new .txt/.md files
- [X] T013 [US1] Implement filename sanitization in scripts/utils/sanitizer.py with character replacement
- [X] T014 [US1] Implement YAML frontmatter addition in scripts/utils/metadata.py with required fields
- [X] T015 [US1] Implement file movement from 01_Inbox to 02_Needs_Action in scripts/utils/file_handler.py
- [X] T016 [US1] Create main execution loop in scripts/watcher.py with Observer pattern
- [X] T017 [US1] Add error handling for file processing in scripts/watcher.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Monitoring Dashboard (Priority: P2)

**Goal**: Allow users to view the Obsidian 'Home' dashboard to see all files currently in 02_Needs_Action and 03_Pending_Approval

**Independent Test**: Can be tested by verifying that the dashboard accurately displays files in the 02_Needs_Action and 03_Pending_Approval folders. This delivers the value of task visibility and status tracking.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T018 [P] [US2] Unit test for metadata.py in tests/unit/test_metadata.py

### Implementation for User Story 2

- [X] T019 [P] [US2] Create Home.md with Dataview queries for displaying tasks needing action
- [X] T020 [US2] Create Home.md with Dataview queries for displaying tasks pending approval
- [X] T021 [US2] Enhance metadata.py to ensure proper status field formatting for Dataview queries
- [X] T022 [US2] Update watcher.py to ensure proper status metadata is added to files

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Human-in-the-Loop Approval (Priority: P3)

**Goal**: When the AI employee completes work on a task, it creates a plan in the 04_Approved folder that requires human approval before the task can be marked as done

**Independent Test**: Can be tested by verifying that files don't move to 05_Done without first having an approved plan in 04_Approved. This delivers the value of quality assurance and human oversight.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T023 [P] [US3] Integration test for end-to-end workflow in tests/integration/test_workflow.py

### Implementation for User Story 3

- [X] T024 [P] [US3] Create Handbook.md with operating instructions for the AI
- [X] T025 [US3] Implement logic in watcher.py to update status to "planning-ready" when AI completes initial processing
- [X] T026 [US3] Implement file movement from 02_Needs_Action to 03_Pending_Approval when ready for approval
- [X] T027 [US3] Implement logic to move files from 03_Pending_Approval to 04_Approved when human approves
- [X] T028 [US3] Implement finalization logic to move files from 04_Approved to 05_Done when all checklist items are complete

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T029 [P] Documentation updates in README.md
- [X] T030 Code cleanup and refactoring
- [X] T031 [P] Add logging functionality across all modules
- [X] T032 [P] Additional unit tests (if requested) in tests/unit/
- [X] T033 Security hardening
- [X] T034 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for file_handler.py in tests/unit/test_file_handler.py"
Task: "Unit test for sanitizer.py in tests/unit/test_sanitizer.py"

# Launch all components for User Story 1 together:
Task: "Create InboxHandler class in scripts/watcher.py that extends FileSystemEventHandler"
Task: "Implement filename sanitization in scripts/utils/sanitizer.py with character replacement"
Task: "Implement YAML frontmatter addition in scripts/utils/metadata.py with required fields"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Add User Story 1 → Test independently → Deploy/Demo (MVP!)
   - Add User Story 2 → Test independently → Deploy/Demo
   - Add User Story 3 → Test independently → Deploy/Demo
3. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence