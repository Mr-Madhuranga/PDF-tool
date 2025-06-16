
# PDF Tool 🔧

A comprehensive command-line tool for PDF manipulation built with Python. Perform various PDF operations like merging, splitting, text extraction, rotation, watermarking, and more.

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## ✨ Features

- **📄 Merge PDFs** - Combine multiple PDF files into one document
- **✂️ Split PDFs** - Break PDFs into separate files (by page or page ranges)
- **📝 Extract Text** - Extract text content from PDF documents
- **🔄 Rotate Pages** - Rotate all pages by specified angles (90°, 180°, 270°)
- **🏷️ Add Watermarks** - Add transparent text watermarks to documents
- **ℹ️ PDF Information** - Display metadata, page count, and file details
- **🆕 Create Sample PDFs** - Generate test PDF files with custom content
- **🛡️ Error Handling** - Comprehensive error handling with detailed logging
- **⚡ Batch Processing** - Process multiple files 
## 📚 Usage Examples

### Merge PDFs
```bash
# Merge multiple PDFs into one
python pdf_tool.py merge file1.pdf file2.pdf file3.pdf -o merged_document.pdf

# Merge all PDFs in current directory
python pdf_tool.py merge *.pdf -o combined.pdf
```

### Split PDFs
```bash
# Split PDF into individual pages
python pdf_tool.py split document.pdf -o split_pages/

# Split PDF into files with 3 pages each
python pdf_tool.py split document.pdf -o split_sections/ -p 3

# Split large PDF into 10-page chunks
python pdf_tool.py split large_document.pdf -o chunks/ -p 10
```

### Extract Text
```bash
# Extract text and display in terminal
python pdf_tool.py extract-text document.pdf

# Extract text and save to file
python pdf_tool.py extract-text document.pdf -o extracted_text.txt
```

### Rotate Pages
```bash
# Rotate all pages by 90 degrees clockwise
python pdf_tool.py rotate document.pdf -a 90 -o rotated.pdf

# Rotate by 180 degrees (upside down)
python pdf_tool.py rotate document.pdf -a 180 -o flipped.pdf
```

### Add Watermarks
```bash
# Add "CONFIDENTIAL" watermark
python pdf_tool.py watermark document.pdf -w "CONFIDENTIAL" -o watermarked.pdf

# Add "DRAFT" watermark
python pdf_tool.py watermark report.pdf -w "DRAFT" -o draft_report.pdf
```

### Get PDF Information
```bash
# Display PDF metadata and details
python pdf_tool.py info document.pdf
```

### Create Sample PDFs
```bash
# Create a basic sample PDF
python pdf_tool.py create -o sample.pdf

# Create PDF with custom content
python pdf_tool.py create -o custom.pdf -c "This is my custom PDF content with multiple lines"
```

## 🔧 Command Reference

### Operations

| Operation | Description | Required Args | Optional Args |
|-----------|-------------|---------------|---------------|
| `merge` | Combine multiple PDFs | `input files` | `-o output_file` |
| `split` | Split PDF into separate files | `input_file` | `-o output_dir`, `-p pages_per_file` |
| `extract-text` | Extract text from PDF | `input_file` | `-o output_file` |
| `rotate` | Rotate all pages | `input_file` | `-a angle`, `-o output_file` |
| `watermark` | Add text watermark | `input_file`, `-w text` | `-o output_file` |
| `info` | Display PDF information | `input_file` | None |
| `create` | Create sample PDF | None | `-o output_file`, `-c content` |

### Arguments

- `input`: Input PDF file(s) - supports wildcards for merge operations
- `-o, --output`: Output file or directory path
- `-a, --angle`: Rotation angle in degrees (must be multiple of 90)
- `-w, --watermark`: Watermark text to add
- `-p, --pages`: Number of pages per file when splitting (default: 1)
- `-c, --content`: Custom content for sample PDF creation

## 📋 Requirements

- Python 3.7 or higher
- PyPDF2
- reportlab
- Pillow (PIL)

## 📦 Dependencies

Create a `requirements.txt` file:
```
PyPDF2==3.0.1
reportlab==4.0.4
Pillow==10.0.0
```

## 🐛 Error Handling

The tool includes comprehensive error handling for common issues:

- **File not found**: Clear error messages when input files don't exist
- **Invalid angles**: Validation for rotation angles (must be multiples of 90°)
- **Permission errors**: Helpful messages for file access issues
- **Corrupted PDFs**: Graceful handling of malformed PDF files
- **Memory issues**: Efficient processing for large files

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/pdf-tool.git
cd pdf-tool

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt
```

