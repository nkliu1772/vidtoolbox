#!/bin/bash

# Define colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Clean up previous build files
echo -e "${GREEN}Cleaning up old build files...${NC}"
rm -rf dist/ build/ *.egg-info

# Step 2: Build the package
echo -e "${GREEN}Building the package...${NC}"
python3 setup.py sdist bdist_wheel || {
    echo -e "${RED}Failed to build the package.${NC}"
    exit 1
}

# Step 3: Upload to PyPI
echo -e "${GREEN}Uploading to PyPI...${NC}"
python3 -m twine upload dist/* || {
    echo -e "${RED}Failed to upload to PyPI.${NC}"
    exit 1
}

echo -e "${GREEN}Successfully deployed to PyPI!${NC}"

