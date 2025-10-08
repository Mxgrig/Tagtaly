#!/bin/bash

# Tagtaly - Quick Run Script
# Makes it easy to run the pipeline daily

echo "╔════════════════════════════════════════╗"
echo "║         TAGTALY                        ║"
echo "║    UK News, Counted & Charted          ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "🔌 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  No virtual environment found"
    echo "💡 Run: python3 -m venv venv"
    echo ""
fi

# Check if dependencies are installed
if ! python -c "import feedparser" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    python -m textblob.download_corpora
    echo ""
fi

# Run the pipeline
echo "🚀 Running Tagtaly pipeline..."
echo ""
python main_pipeline.py

# Check if successful
if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════╗"
    echo "║           ✅ SUCCESS!                  ║"
    echo "╚════════════════════════════════════════╝"
    echo ""

    # Find today's charts
    TODAY=$(date +%Y%m%d)
    CHART_DIR="viral_charts_$TODAY"

    if [ -d "$CHART_DIR" ]; then
        echo "📊 Today's charts are ready:"
        echo ""
        ls -1 $CHART_DIR/*.png | while read file; do
            echo "   $(basename $file)"
        done
        echo ""
        echo "📁 Location: $CHART_DIR/"
        echo ""
        echo "💡 Next steps:"
        echo "   1. Open the folder: cd $CHART_DIR"
        echo "   2. View charts: open *.png"
        echo "   3. Read captions: cat *_caption.txt"
        echo "   4. Post to social media!"
    fi
else
    echo ""
    echo "╔════════════════════════════════════════╗"
    echo "║           ❌ ERROR                     ║"
    echo "╚════════════════════════════════════════╝"
    echo ""
    echo "Something went wrong. Check the error messages above."
    echo ""
    echo "Common fixes:"
    echo "  - Make sure dependencies are installed: pip install -r requirements.txt"
    echo "  - Check internet connection"
    echo "  - Try running individual scripts to isolate the issue"
fi

echo ""
