#!/bin/bash
# Generate PDF report from markdown

echo "Generating PDF report..."

# Check if pandoc is installed
if command -v pandoc &> /dev/null; then
    echo "Using pandoc..."
    pandoc POLYMARKET_INSIDER_TRADING_REPORT.md \
        -o POLYMARKET_INSIDER_TRADING_REPORT.pdf \
        --pdf-engine=xelatex \
        -V geometry:margin=1in \
        -V fontsize=11pt \
        -V colorlinks=true \
        --toc \
        --toc-depth=2
    echo "✅ PDF generated: POLYMARKET_INSIDER_TRADING_REPORT.pdf"
else
    echo "❌ pandoc not found. Installing..."
    echo ""
    echo "Install pandoc:"
    echo "  macOS: brew install pandoc basictex"
    echo "  Linux: sudo apt-get install pandoc texlive-xetex"
    echo ""
    echo "Then run: ./generate_pdf.sh"
fi
