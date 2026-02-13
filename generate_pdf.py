#!/usr/bin/env python3
"""
Generate PDF report from markdown
Uses markdown2 and weasyprint (or falls back to basic HTML conversion)
"""

import sys
import subprocess

def try_weasyprint():
    """Try to generate PDF using weasyprint"""
    try:
        import markdown2
        from weasyprint import HTML, CSS

        print("Converting markdown to HTML...")
        with open('POLYMARKET_INSIDER_TRADING_REPORT.md', 'r') as f:
            md_content = f.read()

        # Convert markdown to HTML
        html_content = markdown2.markdown(md_content, extras=['tables', 'fenced-code-blocks'])

        # Add CSS styling
        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    max-width: 800px;
                    margin: 40px auto;
                    padding: 0 20px;
                    color: #333;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    border-bottom: 2px solid #95a5a6;
                    padding-bottom: 8px;
                    margin-top: 30px;
                }}
                h3 {{
                    color: #555;
                    margin-top: 20px;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 20px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                code {{
                    background-color: #f4f4f4;
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                }}
                pre {{
                    background-color: #f4f4f4;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                blockquote {{
                    border-left: 4px solid #3498db;
                    padding-left: 20px;
                    margin: 20px 0;
                    color: #555;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        print("Generating PDF...")
        HTML(string=styled_html).write_pdf('POLYMARKET_INSIDER_TRADING_REPORT.pdf')

        print("✅ PDF generated successfully: POLYMARKET_INSIDER_TRADING_REPORT.pdf")
        return True

    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        return False
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return False

def try_pandoc():
    """Try to generate PDF using pandoc"""
    try:
        print("Trying pandoc...")
        result = subprocess.run([
            'pandoc',
            'POLYMARKET_INSIDER_TRADING_REPORT.md',
            '-o', 'POLYMARKET_INSIDER_TRADING_REPORT.pdf',
            '--pdf-engine=xelatex',
            '-V', 'geometry:margin=1in',
            '-V', 'fontsize=11pt',
            '--toc',
            '--toc-depth=2'
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ PDF generated successfully: POLYMARKET_INSIDER_TRADING_REPORT.pdf")
            return True
        else:
            print(f"❌ Pandoc failed: {result.stderr}")
            return False

    except FileNotFoundError:
        print("❌ pandoc not found")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def generate_html_fallback():
    """Generate HTML version as fallback"""
    try:
        import markdown2

        print("Generating HTML version...")
        with open('POLYMARKET_INSIDER_TRADING_REPORT.md', 'r') as f:
            md_content = f.read()

        html_content = markdown2.markdown(md_content, extras=['tables', 'fenced-code-blocks'])

        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Polymarket Insider Trading Analysis Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    max-width: 900px;
                    margin: 40px auto;
                    padding: 0 20px;
                    color: #333;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    border-bottom: 2px solid #95a5a6;
                    padding-bottom: 8px;
                    margin-top: 30px;
                }}
                h3 {{
                    color: #555;
                    margin-top: 20px;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 20px 0;
                    font-size: 14px;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 10px;
                    text-align: left;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                    font-weight: bold;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                code {{
                    background-color: #f4f4f4;
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                    font-size: 0.9em;
                }}
                pre {{
                    background-color: #f4f4f4;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                blockquote {{
                    border-left: 4px solid #3498db;
                    padding-left: 20px;
                    margin: 20px 0;
                    color: #555;
                    font-style: italic;
                }}
                @media print {{
                    body {{
                        max-width: 100%;
                    }}
                }}
            </style>
        </head>
        <body>
            {html_content}
            <script>
                // Print to PDF instruction
                console.log('To save as PDF: File > Print > Save as PDF');
            </script>
        </body>
        </html>
        """

        with open('POLYMARKET_INSIDER_TRADING_REPORT.html', 'w') as f:
            f.write(styled_html)

        print("✅ HTML generated: POLYMARKET_INSIDER_TRADING_REPORT.html")
        print("")
        print("To create PDF:")
        print("  1. Open POLYMARKET_INSIDER_TRADING_REPORT.html in browser")
        print("  2. File > Print > Save as PDF")
        print("  OR: Install weasyprint: pip3 install weasyprint markdown2")
        return True

    except Exception as e:
        print(f"❌ Error generating HTML: {e}")
        return False

def main():
    print("="*60)
    print("POLYMARKET REPORT - PDF GENERATOR")
    print("="*60)
    print()

    # Try methods in order of preference
    methods = [
        ("weasyprint", try_weasyprint),
        ("pandoc", try_pandoc),
        ("HTML fallback", generate_html_fallback)
    ]

    for method_name, method_func in methods:
        print(f"Trying {method_name}...")
        if method_func():
            break
        print()
    else:
        print("❌ All methods failed")
        print("")
        print("Install dependencies:")
        print("  pip3 install weasyprint markdown2")
        print("  OR: brew install pandoc basictex")
        sys.exit(1)

if __name__ == '__main__':
    main()
