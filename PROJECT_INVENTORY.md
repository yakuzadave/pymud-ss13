# PROJECT_INVENTORY.md — PyMUD-SS13 Work Units

> Complete enumeration of all improvement work units for pymud-ss13 project.
> Each unit tagged with status: [TODO], [IN_PROGRESS], or [COMPLETED]

**Last Updated**: 2026-01-13  
**Total Work Units**: 42  
**Completed**: 19  
**In Progress**: 0  
**Todo**: 23

---

## Category 1: Core Tracking & Documentation [COMPLETED]

### Tracking Infrastructure
- [COMPLETED] TASKS.md — Authoritative task ledger created [TASKS.md](TASKS.md)
- [COMPLETED] PROJECT_INVENTORY.md — This file, work unit enumeration [PROJECT_INVENTORY.md](PROJECT_INVENTORY.md)
- [COMPLETED] STATUS.md — Current state narrative and progress summary [STATUS.md](STATUS.md)
- [COMPLETED] CHANGELOG.md — Per-batch change log [CHANGELOG.md](CHANGELOG.md)

### Project Documentation
- [IN_PROGRESS] Update TUI_IMPROVEMENTS.md — Mark completed items, add new plans (pending next batch selection)
- [TODO] Update roadmap.md — Reflect Phase 8 progress
- [TODO] Update README.md — Document new features and capabilities
- [TODO] Create IMPLEMENTATION_NOTES.md — Technical decisions and patterns

---

## Category 2: Pull Request Resolution [COMPLETED]

### PR #188 - GameClient Async Coverage
- [COMPLETED] Review changes in PR #188 ✅
- [COMPLETED] Identify conflicting files with main branch ✅
- [COMPLETED] Assess quality of test implementations ✅
- [COMPLETED] Document conflicts and resolution approach ✅ [PR_ANALYSIS.md](PR_ANALYSIS.md)

### PR #189 - GameClient Async Coverage (Duplicate)
- [COMPLETED] Review changes in PR #189 ✅
- [COMPLETED] Compare with PR #188 to identify differences ✅
- [COMPLETED] Determine best approach ✅ (Close both - changes already in main)
- [COMPLETED] Document decision rationale ✅ [PR_ANALYSIS.md](PR_ANALYSIS.md)

### Conflict Resolution Strategy
- [COMPLETED] Analyze git diff between PRs and main ✅
- [COMPLETED] Extract non-conflicting improvements ✅ (All already present)
- [COMPLETED] Create clean implementation on current branch ✅ (Not needed)
- [COMPLETED] Document resolution in CHANGELOG.md ✅

**Resolution**: Both PRs contain identical changes that are already incorporated in main. Close both with explanation.

---

## Category 3: Testing Infrastructure [TODO]

### Playwright E2E Testing
- [TODO] Install and configure Playwright
- [TODO] Create playwright.config.js
- [TODO] Setup test fixtures and utilities
- [TODO] Implement visual regression framework
- [TODO] Create screenshot baseline directory
- [TODO] Add screenshot comparison utilities
- [TODO] Write first E2E test (login flow)
- [TODO] Write E2E test for game commands
- [TODO] Write E2E test for view switching
- [TODO] Document E2E testing in TESTING_GUIDE.md

### BDD Feature Expansion
- [COMPLETED] Create features/tui_map_navigation.feature ✅
- [COMPLETED] Create features/tui_chat_system.feature ✅
- [COMPLETED] Create features/tui_help_system.feature ✅
- [COMPLETED] Add 65+ step definitions for new scenarios ✅
- [COMPLETED] Update TESTING_GUIDE.md with new scenarios ✅ [TESTING_GUIDE.md](docs/TESTING_GUIDE.md)

### Unit Test Coverage
- [TODO] Run coverage analysis to identify <90% modules
- [TODO] Write tests for low-coverage modules
- [TODO] Add tests for edge cases
- [TODO] Add tests for error handling
- [TODO] Update coverage reports in CI

---

## Category 4: TUI Enhancements [TODO]

### External Logging Integration
- [TODO] Research Sentry integration for error tracking
- [TODO] Research LogDNA/DataDog for log aggregation
- [TODO] Design integration architecture (pluggable)
- [TODO] Implement Sentry error handler (optional)
- [TODO] Implement external log shipper (optional)
- [TODO] Add configuration options in config.yaml
- [TODO] Update LOGGING_GUIDE.md with integration docs
- [TODO] Add error notification examples

### TUI Screen Improvements
- [TODO] Enhance Map view with zoom controls
- [TODO] Add Map view minimap overlay
- [TODO] Improve Chat view with channel tabs
- [TODO] Add Chat view message filtering
- [TODO] Expand Help view with command examples
- [TODO] Add Help view search functionality

---

## Category 5: Robotics & Cyborg System [TODO]

### Remote Control Implementation
- [TODO] Design remote control protocol (WebSocket messages)
- [TODO] Add cyborg control panel component
- [TODO] Implement cyborg command interface
- [TODO] Add power management system
- [TODO] Implement battery status monitoring
- [TODO] Add remote camera feeds
- [TODO] Create integration tests for remote control
- [TODO] Document robotics system in docs/robotics_guide.md

### Module System Expansion
- [TODO] Design module plugin architecture
- [TODO] Implement module hot-swapping
- [TODO] Add medical module capabilities
- [TODO] Add engineering module capabilities
- [TODO] Add security module capabilities
- [TODO] Create module configuration system
- [TODO] Write tests for module switching

---

## Category 6: Account Management [TODO]

### Authentication Enhancement
- [TODO] Review current account_system.py implementation
- [TODO] Design improved auth architecture
- [TODO] Implement JWT token system
- [TODO] Add token refresh mechanism
- [TODO] Implement password reset flow
- [TODO] Add email verification (optional)
- [TODO] Create account recovery system
- [TODO] Write authentication tests
- [TODO] Document auth flow in docs/auth_guide.md

### Permission System
- [TODO] Design granular permission model
- [TODO] Implement role-based access control (RBAC)
- [TODO] Add permission decorators for commands
- [TODO] Create admin permission UI
- [TODO] Add permission audit logging
- [TODO] Write permission system tests
- [TODO] Document permissions in docs/admin_guide.md

---

## Category 7: Code Quality & Maintenance [TODO]

### Code Quality
- [TODO] Run full test suite validation
- [TODO] Check for deprecation warnings
- [TODO] Verify code style consistency
- [TODO] Add type hints where missing
- [TODO] Run linter and fix issues

### Documentation Quality
- [TODO] Review all docstrings for completeness
- [TODO] Verify all examples run correctly
- [TODO] Check for broken links in docs
- [TODO] Update API documentation
- [TODO] Create troubleshooting guide

### Cleanup
- [TODO] Remove old temporary files
- [TODO] Clean up unused imports
- [TODO] Remove commented-out code
- [TODO] Update .gitignore patterns
- [TODO] Archive old feature branches

---

## Status Summary

### Completed (19)
- Core tracking files: TASKS.md, PROJECT_INVENTORY.md, STATUS.md, CHANGELOG.md ✓
- PR analysis and resolution strategy for #188 and #189 ✓
- Comprehensive analysis document created ✓
- BDD feature files for Map, Chat, and Help systems ✓
- 65+ step definitions added ✓
- Testing documentation updated ✓
- Test organization guide created (16KB) ✓
- pytest configuration enhanced (13 markers) ✓
- Help screen search functionality added ✓
- Map and Chat screen features verified ✓

### In Progress (0)
- None

### High Priority Next (Top 5)
1. **BATCH-006**: Additional TUI enhancements (logging, shortcuts, animations)
2. Code quality improvements (type hints, docstrings)
3. Implement Playwright E2E testing framework
4. External logging integration
5. Robotics remote control implementation

### Dependencies
- ~~PR conflict resolution blocks GameClient async improvements~~ **RESOLVED**: Changes already in main
- Playwright setup required before E2E tests
- External service API keys needed for logging integration (optional)
- Robotics work depends on stable component system

---

## Notes

- All work units are designed to avoid merge conflicts by working on separate areas
- Testing improvements can proceed independently of PR resolution
- Documentation updates should happen after each feature batch
- External integrations (logging, monitoring) are optional enhancements

**Inventory Status**: BATCH-005 complete, TUI help screen enhanced with search (27+ commands indexed), Map and Chat features verified, ready for additional TUI work or code quality improvements
