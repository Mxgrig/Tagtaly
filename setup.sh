#!/bin/bash

# UK News in Charts - Quick Setup Script
# This script sets up everything you need to get started

echo "=========================================="
echo "  UK News in Charts - Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8 or higher from python.org"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed"
    echo "Please install pip"
    exit 1
fi

echo "✅ pip found"
echo ""

# Create virtual environment (optional but recommended)
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

echo "✅ Virtual environment activated"
echo ""

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Download TextBlob corpora
echo "📚 Downloading TextBlob language data..."
python3 -m textblob.download_corpora

echo ""
echo "=========================================="
echo "  ✅ Setup Complete!"
echo "=========================================="
echo ""
echo "🚀 Quick Start:"
echo ""
echo "1. Run the full pipeline:"
echo "   python main_pipeline.py"
echo ""
echo "2. Or run step by step:"
echo "   python news_collector.py  # Fetch news"
echo "   python news_analyzer.py   # Analyze topics"
echo "   python viral_engine.py    # Create charts"
echo ""
echo "3. Find your charts in:"
echo "   viral_charts_YYYYMMDD/"
echo ""
echo "=========================================="
echo "  📖 Next Steps"
echo "=========================================="
echo ""
echo "For GitHub automation:"
echo "   1. Create GitHub repository"
echo "   2. Push these files"
echo "   3. Enable GitHub Actions"
echo "   4. Charts generate daily at 7 AM"
echo ""
echo "See README.md for full documentation"
echo ""
