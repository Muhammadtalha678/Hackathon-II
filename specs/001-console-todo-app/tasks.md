---
description: "Task list for Console Todo App implementation"
---

# Tasks: Console Todo App

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests included as per Test-First Development constitution principle.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Console App**: `todo_app/` at repository root
- **Tests**: `tests/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Initialize project with uv init console_todo_app
- [X] T002 Create project structure per implementation plan in todo_app/
- [X] T003 [P] Create todo_app/__init__.py
- [X] T004 [P] Create todo_app/models/__init__.py
- [X] T005 [P] Create todo_app/services/__init__.py
- [X] T006 [P] Create todo_app/cli/__init__.py
- [X] T007 [P] Create tests/__init__.py
- [X] T008 [P] Create tests/unit/__init__.py
- [X] T009 [P] Create tests/integration/__init__.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T010 Create TodoItem model in todo_app/models/todo_item.py
- [X] T011 Create TodoService class in todo_app/services/todo_service.py
- [X] T012 Create main application entry point in todo_app/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Todo Item (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new todo items to their list

**Independent Test**: Can be fully tested by adding a new todo item through the interactive menu and verifying it appears in the list, delivering the core value of task tracking.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T013 [P] [US1] Unit test for TodoItem model in tests/unit/test_todo_item.py
- [X] T014 [P] [US1] Unit test for add_todo functionality in tests/unit/test_todo_service.py

### Implementation for User Story 1

- [X] T015 [US1] Implement TodoItem model with id, description, completed, created_at attributes in todo_app/models/todo_item.py (depends on T010)
- [X] T016 [US1] Implement add_todo method in TodoService in todo_app/services/todo_service.py (depends on T011)
- [X] T017 [US1] Create basic menu interface in todo_app/cli/menu.py
- [X] T018 [US1] Integrate add todo functionality with main menu in todo_app/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Todo List (Priority: P1)

**Goal**: Enable users to view all their todo items with status

**Independent Test**: Can be fully tested by having a list of todos and viewing them through the interactive menu, delivering the value of task visibility.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T019 [P] [US2] Unit test for get_all_todos functionality in tests/unit/test_todo_service.py

### Implementation for User Story 2

- [X] T020 [US2] Implement get_all_todos method in TodoService in todo_app/services/todo_service.py (depends on T011)
- [X] T021 [US2] Implement view todos functionality in menu interface in todo_app/cli/menu.py (depends on T017)
- [X] T022 [US2] Integrate view todos with main menu in todo_app/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 6 - Navigate Menu and Exit (Priority: P1)

**Goal**: Enable users to navigate through the interactive menu and exit the application

**Independent Test**: Can be fully tested by navigating through all menu options and exiting the application, delivering the value of basic app navigation.

### Tests for User Story 6 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T023 [P] [US6] Integration test for menu navigation in tests/integration/test_cli_integration.py

### Implementation for User Story 6

- [X] T024 [US6] Implement complete menu interface with all navigation options in todo_app/cli/menu.py (depends on T021)
- [X] T025 [US6] Implement exit functionality in main menu in todo_app/main.py
- [X] T026 [US6] Add error handling for invalid menu choices in todo_app/cli/menu.py

**Checkpoint**: At this point, User Stories 1, 2, AND 6 should all work independently

---

## Phase 6: User Story 3 - Mark Todo Complete (Priority: P2)

**Goal**: Enable users to mark todo items as complete to track progress

**Independent Test**: Can be fully tested by marking an existing todo as complete and verifying its status changes, delivering the value of progress tracking.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T027 [P] [US3] Unit test for mark_complete functionality in tests/unit/test_todo_service.py

### Implementation for User Story 3

- [X] T028 [US3] Implement mark_complete and mark_incomplete methods in TodoService in todo_app/services/todo_service.py (depends on T011)
- [X] T029 [US3] Implement mark complete functionality in menu interface in todo_app/cli/menu.py
- [X] T030 [US3] Integrate mark complete with main menu in todo_app/main.py

**Checkpoint**: At this point, User Stories 1, 2, 3, AND 6 should all work independently

---

## Phase 7: User Story 5 - Delete Todo Item (Priority: P3)

**Goal**: Enable users to delete todo items to manage their list

**Independent Test**: Can be fully tested by deleting an existing todo and verifying it's removed from the list, delivering the value of list management.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T031 [P] [US5] Unit test for delete_todo functionality in tests/unit/test_todo_service.py

### Implementation for User Story 5

- [X] T032 [US5] Implement delete_todo method in TodoService in todo_app/services/todo_service.py (depends on T011)
- [X] T033 [US5] Implement delete todo functionality in menu interface in todo_app/cli/menu.py
- [X] T034 [US5] Integrate delete todo with main menu in todo_app/main.py

**Checkpoint**: At this point, User Stories 1, 2, 3, 5, AND 6 should all work independently

---

## Phase 8: User Story 4 - Update Todo Description (Priority: P3)

**Goal**: Enable users to update the description of existing todo items for flexibility

**Independent Test**: Can be fully tested by updating an existing todo's description and verifying the change persists, delivering the value of task modification capability.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T035 [P] [US4] Unit test for update_todo functionality in tests/unit/test_todo_service.py

### Implementation for User Story 4

- [X] T036 [US4] Implement update_todo method in TodoService in todo_app/services/todo_service.py (depends on T011)
- [X] T037 [US4] Implement update todo functionality in menu interface in todo_app/cli/menu.py
- [X] T038 [US4] Integrate update todo with main menu in todo_app/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T039 [P] Add input validation for empty descriptions in todo_app/services/todo_service.py
- [X] T040 [P] Add proper error handling and user-friendly messages in todo_app/cli/menu.py
- [X] T041 Add type hints to all functions in todo_app/models/todo_item.py
- [X] T042 Add type hints to all functions in todo_app/services/todo_service.py
- [X] T043 Add docstrings to all public functions in todo_app/models/todo_item.py
- [X] T044 Add docstrings to all public functions in todo_app/services/todo_service.py
- [X] T045 Add docstrings to all public functions in todo_app/cli/menu.py
- [X] T046 Run quickstart validation to ensure app works as expected

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 6 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories

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
Task: "Unit test for TodoItem model in tests/unit/test_todo_item.py"
Task: "Unit test for add_todo functionality in tests/unit/test_todo_service.py"

# Launch all implementation for User Story 1 together:
Task: "Implement TodoItem model with id, description, completed, created_at attributes in todo_app/models/todo_item.py"
Task: "Implement add_todo method in TodoService in todo_app/services/todo_service.py"
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

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 6 → Test independently → Deploy/Demo
5. Add User Story 3 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Add User Story 4 → Test independently → Deploy/Demo
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 6
   - Developer D: User Story 3
   - Developer E: User Story 5
   - Developer F: User Story 4
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