#!/bin/bash
# Complete Voice Cloning Setup - Fully Automated
# This script does everything needed to clone your voice

set -e  # Exit on error

echo "🎙️  Complete Voice Cloning Setup for Zenyai"
echo "============================================="
echo ""

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check for Python 3.11
echo -e "${CYAN}Step 1: Checking for Python 3.11...${NC}"

if command -v python3.11 &> /dev/null; then
    echo -e "${GREEN}✅ Python 3.11 found${NC}"
    PYTHON_CMD="python3.11"
elif command -v /opt/homebrew/bin/python3.11 &> /dev/null; then
    echo -e "${GREEN}✅ Python 3.11 found at /opt/homebrew/bin/python3.11${NC}"
    PYTHON_CMD="/opt/homebrew/bin/python3.11"
elif command -v /usr/local/bin/python3.11 &> /dev/null; then
    echo -e "${GREEN}✅ Python 3.11 found at /usr/local/bin/python3.11${NC}"
    PYTHON_CMD="/usr/local/bin/python3.11"
else
    echo -e "${YELLOW}⏳ Python 3.11 not found. Installing...${NC}"
    brew install python@3.11
    
    # Check again
    if command -v python3.11 &> /dev/null; then
        PYTHON_CMD="python3.11"
    elif command -v /opt/homebrew/bin/python3.11 &> /dev/null; then
        PYTHON_CMD="/opt/homebrew/bin/python3.11"
    else
        echo -e "${YELLOW}⚠️  Python 3.11 installed but not in PATH. Using full path.${NC}"
        PYTHON_CMD="/opt/homebrew/bin/python3.11"
    fi
fi

echo "Using Python: $PYTHON_CMD"
$PYTHON_CMD --version
echo ""

# Step 2: Create virtual environment
echo -e "${CYAN}Step 2: Creating Python 3.11 virtual environment...${NC}"

if [ -d "venv_chatterbox" ]; then
    echo -e "${YELLOW}Virtual environment already exists, removing old one...${NC}"
    rm -rf venv_chatterbox
fi

$PYTHON_CMD -m venv venv_chatterbox
echo -e "${GREEN}✅ Virtual environment created${NC}"
echo ""

# Step 3: Activate and install Chatterbox
echo -e "${CYAN}Step 3: Installing Chatterbox...${NC}"

source venv_chatterbox/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install Chatterbox
cd chatterbox
pip install -e .
cd ..

echo -e "${GREEN}✅ Chatterbox installed${NC}"
echo ""

# Step 4: Install project dependencies
echo -e "${CYAN}Step 4: Installing project dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

# Step 5: Clone voice and generate test
echo -e "${CYAN}Step 5: Cloning your voice and generating test...${NC}"

python test_my_voice.py

echo ""
echo -e "${GREEN}=============================================${NC}"
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo -e "${GREEN}=============================================${NC}"
echo ""
echo -e "${CYAN}Your voice has been cloned as: Tomi_Zenyai${NC}"
echo -e "${CYAN}Test audio saved to: narrations/tomi_zenyai_test.wav${NC}"
echo ""
echo -e "${YELLOW}To use in future sessions:${NC}"
echo "  source venv_chatterbox/bin/activate"
echo "  python3 hybrid_video_generator.py 'Your Video Topic'"
echo ""
echo -e "${YELLOW}To hear the test:${NC}"
echo "  open narrations/tomi_zenyai_test.wav"
echo ""
