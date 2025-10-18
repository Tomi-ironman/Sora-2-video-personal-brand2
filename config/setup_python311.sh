#!/bin/bash
# Quick setup script for Python 3.11 environment with Chatterbox

echo "🎙️  Setting up Chatterbox with Python 3.11..."

# Check if conda is installed
if command -v conda &> /dev/null; then
    echo "✅ Conda found"
    
    # Create environment
    echo "Creating Python 3.11 environment..."
    conda create -n chatterbox python=3.11 -y
    
    echo ""
    echo "✅ Environment created!"
    echo ""
    echo "Next steps:"
    echo "1. Activate environment: conda activate chatterbox"
    echo "2. Install Chatterbox: cd chatterbox && pip install -e ."
    echo "3. Install project: cd .. && pip install -r requirements.txt"
    echo "4. Test: python3 test_chatterbox.py"
    echo ""
    echo "See CHATTERBOX_SETUP.md for detailed instructions"
    
elif command -v pyenv &> /dev/null; then
    echo "✅ pyenv found"
    
    # Install Python 3.11
    echo "Installing Python 3.11.7..."
    pyenv install 3.11.7 -s
    
    # Create virtual environment
    echo "Creating virtual environment..."
    pyenv virtualenv 3.11.7 chatterbox-env
    
    echo ""
    echo "✅ Environment created!"
    echo ""
    echo "Next steps:"
    echo "1. Activate environment: pyenv activate chatterbox-env"
    echo "2. Install Chatterbox: cd chatterbox && pip install -e ."
    echo "3. Install project: cd .. && pip install -r requirements.txt"
    echo "4. Test: python3 test_chatterbox.py"
    echo ""
    echo "See CHATTERBOX_SETUP.md for detailed instructions"
    
else
    echo "❌ Neither conda nor pyenv found"
    echo ""
    echo "Please install one of the following:"
    echo ""
    echo "Option 1 - Conda (Recommended):"
    echo "  Download from: https://docs.conda.io/en/latest/miniconda.html"
    echo ""
    echo "Option 2 - pyenv:"
    echo "  Install: brew install pyenv"
    echo ""
    echo "Then run this script again"
fi
