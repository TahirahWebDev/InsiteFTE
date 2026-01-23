---

description: "Task list template for feature implementation"
---

# Tasks: Gold Tier Agentic Loop

**Input**: Design documents from `/specs/002-gold-tier-enhancements/`
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

- [X] T001 Create project structure per implementation plan in agentic_loop/ directory
- [X] T002 [P] Initialize pyproject.toml with Python 3.12+ and dependencies (watchdog, ruamel.yaml, obsidian-api-wrapper)
- [X] T003 [P] Create agentic_loop/ directory structure with main.py, agent/, tools/, obsidian/, state_machine/, planner/, config.py, and utils/ subdirectories

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T004 Create agentic_loop/config.py with vault path and folder configuration settings
- [X] T005 [P] Create agentic_loop/utils/json_parser.py module for JSON command parsing
- [X] T006 [P] Create agentic_loop/utils/file_operations.py module for file handling operations
- [X] T007 Create agentic_loop/tools/base_tool.py with base tool class definition
- [X] T008 Create agentic_loop/tools/registry.py for tool registration and execution
- [X] T009 Create agentic_loop/utils/logger.py with enhanced logging and safety features

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Tool Integration (Priority: P1) 🎯 MVP

**Goal**: Enable the AI Employee to access external tools like web search and notification systems through a 'Toolbox' that allows the AI to call scripts like search_web.py or send_notification.py when needed for task completion.

**Independent Test**: Can be fully tested by triggering the AI to use a tool (e.g., search the web for information) and verifying the tool executes properly and returns results to the AI. This delivers the core value of expanded AI capabilities.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T010 [P] [US1] Unit test for tool registry in tests/unit/test_tools.py
- [ ] T011 [P] [US1] Unit test for JSON parser in tests/unit/test_json_parser.py

### Implementation for User Story 1

- [X] T012 [P] [US1] Create agentic_loop/tools/search_web.py with web search functionality
- [X] T013 [P] [US1] Create agentic_loop/tools/send_notification.py with notification functionality
- [X] T014 [US1] Implement tool registration in agentic_loop/tools/registry.py
- [X] T015 [US1] Implement JSON command parser in agentic_loop/utils/json_parser.py to extract tool calls
- [X] T016 [US1] Create agentic_loop/tools/__init__.py to expose tools
- [X] T017 [US1] Add tool execution logging to agentic_loop/utils/logger.py
- [X] T018 [US1] Update agentic_loop/config.py with tool execution settings

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Enhanced State Machine (Priority: P2)

**Goal**: Support more complex task processing workflows by adding new states to the existing folder structure, including 06_Researching for tasks requiring research and 07_Reviewing for quality assessment.

**Independent Test**: Can be tested by creating a task that goes through the new states and verifying it progresses correctly through 06_Researching and 07_Reviewing before reaching approval. This delivers the value of more nuanced task management.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T019 [P] [US2] Unit test for state machine engine in tests/unit/test_state_machine.py

### Implementation for User Story 2

- [X] T020 [P] [US2] Create agentic_loop/state_machine/states.py with definitions for all states (01-07)
- [X] T021 [US2] Implement agentic_loop/state_machine/engine.py with state transition logic
- [X] T022 [US2] Update agentic_loop/config.py with new state folder paths
- [X] T023 [US2] Modify file handling utilities to recognize new states
- [X] T024 [US2] Update YAML metadata schema to support new state transitions

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Autonomous Planning (Priority: P3)

**Goal**: When a task enters 02_Needs_Action, the AI should automatically generate a multi-step project plan without waiting for manual prompts, enabling proactive task management.

**Independent Test**: Can be tested by placing a task in 02_Needs_Action and verifying that a multi-step plan is automatically generated. This delivers the value of reduced manual planning overhead.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T025 [P] [US3] Unit test for autonomous planner in tests/unit/test_planner.py

### Implementation for User Story 3

- [X] T026 [P] [US3] Create agentic_loop/planner/autonomous_planner.py with planning functionality
- [X] T027 [US3] Integrate planner with state machine to trigger on 02_Needs_Action entry
- [X] T028 [US3] Implement plan validation before execution
- [X] T029 [US3] Update task file metadata to include generated plans
- [X] T030 [US3] Add planning metrics to logging system

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Feedback Loop (Critic Mode) (Priority: P4)

**Goal**: Support a 'Critic' mode where the AI reviews its own output for quality before moving it to 03_Pending_Approval, ensuring quality control before human review.

**Independent Test**: Can be tested by having the AI complete a task and then run critic mode on its output before submission for approval. This delivers the value of improved output quality.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T031 [P] [US4] Unit test for critic module in tests/unit/test_critic.py

### Implementation for User Story 4

- [X] T032 [P] [US4] Create agentic_loop/agent/critic.py with quality assessment functionality
- [X] T033 [US4] Integrate critic mode with state transitions to review before approval
- [X] T034 [US4] Implement configurable quality thresholds
- [X] T035 [US4] Add critic assessment to task file metadata
- [X] T036 [US4] Update logging to capture critic evaluations

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Agentic Loop Integration

**Goal**: Implement the main agentic loop that periodically checks the 02_Needs_Action folder every 60 seconds and orchestrates the agent, tools, state machine, and Obsidian integration.

### Implementation for Agentic Loop

- [X] T037 [P] Create agentic_loop/agent/core.py with core agent logic and thought processes
- [X] T038 Create agentic_loop/agent/__init__.py to expose agent components
- [X] T039 Create agentic_loop/obsidian/api_wrapper.py for Obsidian API integration
- [X] T040 Create agentic_loop/obsidian/dashboard.py for Mission Control dashboard updates
- [X] T041 Implement main agentic loop in agentic_loop/main.py with periodic polling
- [X] T042 Integrate all components (agent, tools, state machine, planner, critic) in the main loop
- [X] T043 Add kill switch mechanism to main loop for safety
- [X] T044 Implement error handling and self-correction in the main loop

---

## Phase 8: Memory Management

**Goal**: Implement the memory system to maintain Memory.md file for long-term goal tracking across different tasks.

### Implementation for Memory Management

- [X] T045 Create agentic_loop/agent/memory.py with memory management system
- [X] T046 Update agentic_loop/config.py with memory file path settings
- [X] T047 Integrate memory system with agent core for context retention
- [X] T048 Implement memory cleanup and compression routines

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T049 [P] Documentation updates in README.md
- [ ] T050 Code cleanup and refactoring
- [ ] T051 [P] Add comprehensive logging across all modules
- [ ] T052 [P] Additional unit tests (if requested) in tests/unit/
- [ ] T053 Security hardening for tool execution
- [ ] T054 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Agentic Loop Integration (Phase 7)**: Depends on all user stories being complete
- **Memory Management (Phase 8)**: Depends on agentic loop being implemented
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable

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
Task: "Unit test for tool registry in tests/unit/test_tools.py"
Task: "Unit test for JSON parser in tests/unit/test_json_parser.py"

# Launch all components for User Story 1 together:
Task: "Create agentic_loop/tools/search_web.py with web search functionality"
Task: "Create agentic_loop/tools/send_notification.py with notification functionality"
Task: "Implement tool registration in agentic_loop/tools/registry.py"
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
   - Add User Story 4 → Test independently → Deploy/Demo
3. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
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