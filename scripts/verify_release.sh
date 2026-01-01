#!/bin/bash
set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🔍 Starting Clean Release Verification...${NC}"

# Create temp directory
TEMP_DIR=$(mktemp -d)
echo "Created temp workspace: $TEMP_DIR"

# Cleanup on exit
function cleanup {
  rm -rf "$TEMP_DIR"
  echo "Cleaned up temp workspace."
}
trap cleanup EXIT

cd "$TEMP_DIR"

# 1. Create venv
echo "1. Creating fresh virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 2. Install Package
# If argument provided, install from there (e.g. local dist), else install from TestPyPI/PyPI
if [ -z "$1" ]; then
    echo "No package path provided. Installing from local source..."
    pip install /home/tandyvip/Desktop/1102
else
    echo "Installing from: $1"
    pip install "$1"
fi

# 3. Verify Version
echo "2. Verifying version..."
INSTALLED_VERSION=$(python -c "import pkg_resources; print(pkg_resources.get_distribution('axon-framework').version)")
echo "Installed version: $INSTALLED_VERSION"

# 4. Verify Import
echo "3. Verifying import..."
python -c "import axon; print('✅ axon imported successfully')"

# 5. Verify CLI
echo "4. Verifying CLI..."
if axon --help > /dev/null; then
    echo -e "${GREEN}✅ CLI is working${NC}"
else
    echo -e "${RED}❌ CLI failed${NC}"
    exit 1
fi

echo -e "${GREEN}🎉 Release Verification PASSED!${NC}"
