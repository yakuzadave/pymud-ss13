#!/bin/bash

# generate_agents_md.sh
# Script to create AGENTS.md with recent changes, test results, and guidance for new team members

set -e  # Exit on any error

# CI environment detection and configuration
if [ "${CI}" = "true" ] || [ "${GITHUB_ACTIONS}" = "true" ]; then
    echo "🤖 Running in CI environment"
    export DEBIAN_FRONTEND=noninteractive
    QUIET_FLAG="--quiet"
    # GitHub Actions specific environment variables
    if [ -n "${GITHUB_REPOSITORY}" ]; then
        GITHUB_REPO_URL="https://github.com/${GITHUB_REPOSITORY}"
    fi
else
    QUIET_FLAG=""
    echo "🖥️  Running in local environment"
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Generating AGENTS.md for new team member onboarding...${NC}"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}Error: Not in a git repository. Please run this script from the project root.${NC}"
    exit 1
fi

# Get project name from git remote or directory name
PROJECT_NAME=$(basename "$(git rev-parse --show-toplevel)")
if git remote get-url origin > /dev/null 2>&1; then
    PROJECT_NAME=$(basename "$(git remote get-url origin)" .git)
fi

echo -e "${YELLOW}📁 Project: ${PROJECT_NAME}${NC}"

# Install Python dependencies
echo -e "${YELLOW}📦 Installing Python testing dependencies...${NC}"
if command -v pip > /dev/null 2>&1; then
    pip install ${QUIET_FLAG} pytest pytest-cov pytest-html 2>/dev/null || {
        echo -e "${YELLOW}⚠️  Could not install pytest dependencies. Continuing anyway...${NC}"
    }
    
    # Install project dependencies if they exist
    if [ -f "requirements.txt" ]; then
        echo -e "${YELLOW}📋 Installing project requirements...${NC}"
        pip install ${QUIET_FLAG} -r requirements.txt 2>/dev/null || {
            echo -e "${YELLOW}⚠️  Could not install all requirements. Continuing anyway...${NC}"
        }
    elif [ -f "setup.py" ]; then
        echo -e "${YELLOW}🔧 Installing project via setup.py...${NC}"
        pip install ${QUIET_FLAG} -e . 2>/dev/null || {
            echo -e "${YELLOW}⚠️  Could not install project. Continuing anyway...${NC}"
        }
    elif [ -f "pyproject.toml" ]; then
        echo -e "${YELLOW}🔧 Installing project via pyproject.toml...${NC}"
        pip install ${QUIET_FLAG} -e . 2>/dev/null || {
            echo -e "${YELLOW}⚠️  Could not install project. Continuing anyway...${NC}"
        }
    fi
else
    echo -e "${YELLOW}⚠️  pip not found. Please ensure pytest and pytest-cov are installed.${NC}"
fi

# Create AGENTS.md file
AGENTS_FILE="AGENTS.md"
echo -e "${YELLOW}📝 Creating ${AGENTS_FILE}...${NC}"

# Initialize the file with header
cat > "$AGENTS_FILE" << EOF
# 🤖 Agent Development Guide

**Project:** ${PROJECT_NAME}  
**Generated:** $(date '+%Y-%m-%d %H:%M:%S')  
**For:** New team member onboarding
$(if [ -n "${GITHUB_REPO_URL}" ]; then echo "**Repository:** ${GITHUB_REPO_URL}"; fi)
$(if [ -n "${GITHUB_SHA}" ]; then echo "**Commit:** ${GITHUB_SHA:0:7}"; fi)
$(if [ -n "${GITHUB_REF_NAME}" ]; then echo "**Branch:** ${GITHUB_REF_NAME}"; fi)

---

EOF

# Add recent changes section
echo -e "${YELLOW}📊 Gathering recent changes from git history...${NC}"
cat >> "$AGENTS_FILE" << EOF
## 📈 Recent Changes (Last 5 Commits)

The following commits show recent development activity. Review these to understand current work:

EOF

# Get last 5 commits with details
git log --oneline -5 --pretty=format:"- **%h** (%cr by %an): %s" >> "$AGENTS_FILE"
echo "" >> "$AGENTS_FILE"
echo "" >> "$AGENTS_FILE"

# Add detailed commit information
cat >> "$AGENTS_FILE" << EOF
### 🔍 Detailed Recent Changes

EOF

# Get more detailed info for last 3 commits
git log -3 --pretty=format:"#### Commit %h - %s%n**Author:** %an <%ae>%n**Date:** %ad%n**Message:**%n%b%n---" --date=format:'%Y-%m-%d %H:%M:%S' >> "$AGENTS_FILE"

echo "" >> "$AGENTS_FILE"

# Add files changed in recent commits
cat >> "$AGENTS_FILE" << EOF

### 📁 Files Modified Recently

EOF

git log -5 --name-only --pretty=format: | sort | uniq | grep -v '^$' | sed 's/^/- /' >> "$AGENTS_FILE"
echo "" >> "$AGENTS_FILE"
echo "" >> "$AGENTS_FILE"

# Run pytest and capture results
echo -e "${YELLOW}🧪 Running pytest with coverage...${NC}"
cat >> "$AGENTS_FILE" << EOF
## 🧪 Test Results

EOF

# Create temp files for test output
TEST_OUTPUT=$(mktemp)
COVERAGE_OUTPUT=$(mktemp)

# Run pytest with coverage
if command -v pytest > /dev/null 2>&1; then
    echo -e "${BLUE}Running tests...${NC}"
    
    # Run pytest and capture output
    if pytest --cov=. --cov-report=term-missing --tb=short > "$TEST_OUTPUT" 2>&1; then
        TEST_STATUS="✅ PASSED"
        echo -e "${GREEN}✅ Tests passed!${NC}"
    else
        TEST_STATUS="❌ FAILED"
        echo -e "${RED}❌ Some tests failed.${NC}"
    fi
    
    # Add test results to markdown
    cat >> "$AGENTS_FILE" << EOF
**Status:** ${TEST_STATUS}  
**Run Date:** $(date '+%Y-%m-%d %H:%M:%S')

### Test Output
\`\`\`
$(cat "$TEST_OUTPUT")
\`\`\`

EOF

else
    cat >> "$AGENTS_FILE" << EOF
**Status:** ⚠️ pytest not available  
**Note:** Please install pytest to run tests

\`\`\`bash
pip install pytest pytest-cov
pytest --cov=.
\`\`\`

EOF
fi

# Add coverage summary if available
if grep -q "TOTAL" "$TEST_OUTPUT" 2>/dev/null; then
    echo "### Coverage Summary" >> "$AGENTS_FILE"
    echo '```' >> "$AGENTS_FILE"
    grep -A 10 -B 5 "TOTAL" "$TEST_OUTPUT" | tail -15 >> "$AGENTS_FILE" 2>/dev/null || true
    echo '```' >> "$AGENTS_FILE"
    echo "" >> "$AGENTS_FILE"
fi

# Add Python environment info
echo "### Environment Info" >> "$AGENTS_FILE"
echo '```' >> "$AGENTS_FILE"
echo "Python Version: $(python --version 2>&1 || echo 'Python not found')" >> "$AGENTS_FILE"
echo "Working Directory: $(pwd)" >> "$AGENTS_FILE"
echo "Git Branch: $(git branch --show-current 2>/dev/null || echo 'unknown')" >> "$AGENTS_FILE"
echo "Git Remote: $(git remote get-url origin 2>/dev/null || echo 'no remote')" >> "$AGENTS_FILE"
echo '```' >> "$AGENTS_FILE"
echo "" >> "$AGENTS_FILE"

# Add guidance section
cat >> "$AGENTS_FILE" << EOF
---

## 🎯 Getting Started Guide

### 🔍 What to Review

1. **Test Results Above**: Check if all tests are passing. If not, these might be good first issues to tackle.

2. **Recent Commits**: Look at the commit history above to understand:
   - What features are being developed
   - What bugs have been fixed recently
   - Coding patterns and conventions used

3. **Modified Files**: The files listed in "Files Modified Recently" are active areas of development.

### 🛠️ Recommended Next Steps

1. **Fix Failing Tests**: If any tests are failing, start by investigating and fixing them.

2. **Code Review**: Review the recent commits to understand the codebase structure and patterns.

3. **Documentation**: Check if any of the recently modified files need documentation updates.

4. **Testing**: Consider adding tests for any code that appears undertested based on coverage reports.

### 🚀 Finding Work

- Look for TODO comments in recently changed files: \`grep -r "TODO\\|FIXME\\|XXX" .\`
- Check for issues in the repository's issue tracker
- Look for functions/modules with low test coverage
- Review commit messages for mentions of "WIP" or "partial" implementations

### 🤝 Contributing

Before making changes:
1. Create a new branch: \`git checkout -b feature/your-feature-name\`
2. Run tests locally: \`pytest --cov=.\`
3. Check code style (if applicable): \`flake8 .\` or \`black .\`
4. Commit with descriptive messages following project conventions

---

**Happy coding! 🎉**

*This file was $(if [ "${CI}" = "true" ]; then echo "automatically "; fi)generated by \`generate_agents_md.sh\` on $(date '+%Y-%m-%d %H:%M:%S')$(if [ -n "${GITHUB_RUN_ID}" ]; then echo " (GitHub Actions Run #${GITHUB_RUN_ID})"; fi)*
EOF

# Cleanup temp files
rm -f "$TEST_OUTPUT" "$COVERAGE_OUTPUT"

echo -e "${GREEN}✅ ${AGENTS_FILE} has been created successfully!${NC}"

# Different messages for CI vs local environments
if [ "${CI}" = "true" ] || [ "${GITHUB_ACTIONS}" = "true" ]; then
    echo -e "${BLUE}🤖 Generated in CI environment - file will be automatically committed${NC}"
    if [ -n "${GITHUB_REPO_URL}" ]; then
        echo -e "${BLUE}📖 View online: ${GITHUB_REPO_URL}/blob/main/AGENTS.md${NC}"
    fi
else
    echo -e "${BLUE}📖 Review the file for an overview of recent changes, test results, and next steps.${NC}"
    echo -e "${YELLOW}💡 Tip: Add this script to your project's README.md setup instructions!${NC}"
    echo -e "${YELLOW}🔄 Consider setting up the GitHub Action for automatic updates!${NC}"
fi

# Display file location and size
if [ -f "$AGENTS_FILE" ]; then
    FILE_SIZE=$(wc -l < "$AGENTS_FILE")
    echo -e "${GREEN}📄 File created: ${AGENTS_FILE} (${FILE_SIZE} lines)${NC}"
    
    # Show file preview in CI for debugging
    if [ "${CI}" = "true" ] && [ "${GITHUB_ACTIONS}" = "true" ]; then
        echo -e "${BLUE}📋 File preview (first 10 lines):${NC}"
        head -10 "$AGENTS_FILE" || true
    fi
fi