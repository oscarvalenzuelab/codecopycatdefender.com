#!/bin/bash

# Setup script to install Git hooks for the project

echo "🔧 Setting up Git hooks for Code Copycat Defender..."

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create the pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Pre-commit hook to check for forbidden words
# Reads forbidden words from .forbidden-words.txt file

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Path to forbidden words file
FORBIDDEN_WORDS_FILE=".forbidden-words.txt"

# Check if forbidden words file exists
if [ ! -f "$FORBIDDEN_WORDS_FILE" ]; then
    echo -e "${YELLOW}Warning: $FORBIDDEN_WORDS_FILE not found. Skipping forbidden words check.${NC}"
    exit 0
fi

# Get list of staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

# Read forbidden words from file (excluding comments and empty lines)
FORBIDDEN_WORDS=$(grep -v '^#' "$FORBIDDEN_WORDS_FILE" 2>/dev/null | grep -v '^$' | tr '\n' '|' | sed 's/|$//')

if [ -z "$FORBIDDEN_WORDS" ]; then
    # No forbidden words configured
    exit 0
fi

# Check each staged file for forbidden words
FOUND_VIOLATIONS=0
VIOLATION_DETAILS=""

for FILE in $STAGED_FILES; do
    # Skip binary files
    if file "$FILE" | grep -q "text"; then
        # Check for forbidden words (case-insensitive)
        MATCHES=$(git diff --cached --no-color "$FILE" | grep -i -E "^\+" | grep -i -E "($FORBIDDEN_WORDS)" 2>/dev/null)
        
        if [ ! -z "$MATCHES" ]; then
            FOUND_VIOLATIONS=1
            VIOLATION_DETAILS="${VIOLATION_DETAILS}\n${RED}❌ Found forbidden words in $FILE:${NC}"
            
            # Show which forbidden words were found
            while IFS= read -r line; do
                for word in $(echo "$FORBIDDEN_WORDS" | tr '|' '\n'); do
                    if echo "$line" | grep -i -q "$word"; then
                        VIOLATION_DETAILS="${VIOLATION_DETAILS}\n  ${YELLOW}→ Found: \"$word\"${NC}"
                        VIOLATION_DETAILS="${VIOLATION_DETAILS}\n    ${line}"
                    fi
                done
            done <<< "$MATCHES"
        fi
    fi
done

if [ $FOUND_VIOLATIONS -eq 1 ]; then
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}⚠️  COMMIT BLOCKED: Forbidden words detected${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "$VIOLATION_DETAILS"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}💡 To proceed, remove the forbidden words from your changes.${NC}"
    echo -e "${YELLOW}   Forbidden words list: $FORBIDDEN_WORDS_FILE${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 1
fi

echo -e "${GREEN}✅ No forbidden words found. Proceeding with commit...${NC}"
exit 0
EOF

# Make the hook executable
chmod +x .git/hooks/pre-commit

echo "✅ Git hooks installed successfully!"
echo ""
echo "📝 To add forbidden words:"
echo "   1. Edit .forbidden-words.txt through GitHub web UI"
echo "   2. Pull the changes locally"
echo ""
echo "The pre-commit hook will automatically check for forbidden words before each commit."