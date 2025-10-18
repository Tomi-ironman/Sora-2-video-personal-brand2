#!/bin/bash
# Setup SadTalker - Download Models and Prepare

set -e

echo "🎬 Setting up SadTalker for Talking Head Videos"
echo "=============================================="
echo ""

GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

cd SadTalker

# Create checkpoints directory
echo -e "${CYAN}Creating checkpoints directory...${NC}"
mkdir -p checkpoints

# Download models
echo -e "${CYAN}Downloading SadTalker models (~3-4 GB)...${NC}"
echo "This may take 5-10 minutes depending on your internet speed"
echo ""

# Download main model checkpoints
echo "Downloading main checkpoints..."
cd checkpoints

# SadTalker model
if [ ! -f "SadTalker_V0.0.2_256.safetensors" ]; then
    curl -L -o SadTalker_V0.0.2_256.safetensors https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors
fi

if [ ! -f "SadTalker_V0.0.2_512.safetensors" ]; then
    curl -L -o SadTalker_V0.0.2_512.safetensors https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_512.safetensors
fi

# Face detection models
echo "Downloading face detection models..."
mkdir -p ../gfpgan/weights
cd ../gfpgan/weights

if [ ! -f "alignment_WFLW_4HG.pth" ]; then
    curl -L -o alignment_WFLW_4HG.pth https://github.com/xinntao/facexlib/releases/download/v0.1.0/alignment_WFLW_4HG.pth
fi

if [ ! -f "detection_Resnet50_Final.pth" ]; then
    curl -L -o detection_Resnet50_Final.pth https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth
fi

if [ ! -f "parsing_parsenet.pth" ]; then
    curl -L -o parsing_parsenet.pth https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth
fi

# GFPGAN for face enhancement
if [ ! -f "GFPGANv1.4.pth" ]; then
    curl -L -o GFPGANv1.4.pth https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth
fi

cd ../../..

echo ""
echo -e "${GREEN}✅ SadTalker setup complete!${NC}"
echo ""
echo -e "${CYAN}You can now create talking head videos!${NC}"
echo ""
echo "Usage:"
echo "  python create_talking_video.py <your_photo> <your_audio>"
echo ""
echo "Or run interactively:"
echo "  python create_talking_video.py"
echo ""
