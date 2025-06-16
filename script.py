#!/usr/bin/env python3
"""
PDF Tool - A comprehensive tool for PDF operations
Supports: merge, split, extract text, rotate pages, add watermarks, and more

Required dependencies:
pip install PyPDF2 reportlab Pillow

Usage:
    python pdf_tool.py merge file1.pdf file2.pdf -o merged.pdf
    python pdf_tool.py split input.pdf -o output_folder
    python pdf_tool.py extract-text input.pdf
    python pdf_tool.py rotate input.pdf -a 90 -o rotated.pdf
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional
import logging

try:
    import PyPDF2
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from PIL import Image
except ImportError as e:
    print(f"Error: Missing required dependency - {e}")
    print("Please install with: pip install PyPDF2 reportlab Pillow")
    sys.exit(1)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFTool:
    """A comprehensive PDF manipulation tool"""
    
    def __init__(self):
        self.supported_operations = [
            'merge', 'split', 'extract-text', 'rotate', 
            'watermark', 'compress', 'info', 'create'
        ]
    
    def merge_pdfs(self, input_files: List[str], output_file: str) -> bool:
        """Merge multiple PDF files into one"""
        try:
            merger = PyPDF2.PdfMerger()
            
            for file_path in input_files:
                if not os.path.exists(file_path):
                    logger.error(f"File not found: {file_path}")
                    return False
                
                logger.info(f"Adding {file_path} to merge")
                merger.append(file_path)
            
            with open(output_file, 'wb') as output:
                merger.write(output)
                
            merger.close()
            logger.info(f"Successfully merged {len(input_files)} files into {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error merging PDFs: {e}")
            return False
    
    def split_pdf(self, input_file: str, output_dir: str, pages_per_file: int = 1) -> bool:
        """Split PDF into separate files"""
        try:
            if not os.path.exists(input_file):
                logger.error(f"Input file not found: {input_file}")
                return False
            
            # Create output directory if it doesn't exist
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            with open(input_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                total_pages = len(reader.pages)
                
                logger.info(f"Splitting {input_file} ({total_pages} pages)")
                
                for i in range(0, total_pages, pages_per_file):
                    writer = PyPDF2.PdfWriter()
                    
                    # Add pages to writer
                    end_page = min(i + pages_per_file, total_pages)
                    for page_num in range(i, end_page):
                        writer.add_page(reader.pages[page_num])
                    
                    # Create output filename
                    base_name = Path(input_file).stem
                    if pages_per_file == 1:
                        output_filename = f"{base_name}_page_{i+1}.pdf"
                    else:
                        output_filename = f"{base_name}_pages_{i+1}-{end_page}.pdf"
                    
                    output_path = os.path.join(output_dir, output_filename)
                    
                    with open(output_path, 'wb') as output_file:
                        writer.write(output_file)
                    
                    logger.info(f"Created: {output_filename}")
                
                logger.info(f"Successfully split into {output_dir}")
                return True
                
        except Exception as e:
            logger.error(f"Error splitting PDF: {e}")
            return False
    
    def extract_text(self, input_file: str, output_file: Optional[str] = None) -> bool:
        """Extract text from PDF"""
        try:
            if not os.path.exists(input_file):
                logger.error(f"Input file not found: {input_file}")
                return False
            
            text_content = []
            
            with open(input_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                logger.info(f"Extracting text from {len(reader.pages)} pages")
                
                for page_num, page in enumerate(reader.pages, 1):
                    text = page.extract_text()
                    text_content.append(f"=== Page {page_num} ===\n{text}\n")
            
            full_text = "\n".join(text_content)
            
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(full_text)
                logger.info(f"Text saved to: {output_file}")
            else:
                print(full_text)
            
            return True
            
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return False
    
    def rotate_pdf(self, input_file: str, angle: int, output_file: str) -> bool:
        """Rotate all pages in PDF by specified angle"""
        try:
            if not os.path.exists(input_file):
                logger.error(f"Input file not found: {input_file}")
                return False
            
            if angle % 90 != 0:
                logger.error("Angle must be a multiple of 90 degrees")
                return False
            
            with open(input_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                writer = PyPDF2.PdfWriter()
                
                logger.info(f"Rotating {len(reader.pages)} pages by {angle} degrees")
                
                for page in reader.pages:
                    rotated_page = page.rotate(angle)
                    writer.add_page(rotated_page)
                
                with open(output_file, 'wb') as output:
                    writer.write(output)
                
                logger.info(f"Rotated PDF saved as: {output_file}")
                return True
                
        except Exception as e:
            logger.error(f"Error rotating PDF: {e}")
            return False
    
    def add_watermark(self, input_file: str, watermark_text: str, output_file: str) -> bool:
        """Add text watermark to PDF"""
        try:
            if not os.path.exists(input_file):
                logger.error(f"Input file not found: {input_file}")
                return False
            
            # Create watermark PDF
            watermark_file = "temp_watermark.pdf"
            c = canvas.Canvas(watermark_file, pagesize=letter)
            c.setFont("Helvetica", 50)
            c.setFillAlpha(0.3)  # Make watermark transparent
            c.rotate(45)  # Rotate watermark text
            c.drawString(200, 200, watermark_text)
            c.save()
            
            # Apply watermark to each page
            with open(input_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                writer = PyPDF2.PdfWriter()
                
                with open(watermark_file, 'rb') as wm_file:
                    watermark = PyPDF2.PdfReader(wm_file)
                    watermark_page = watermark.pages[0]
                    
                    for page in reader.pages:
                        page.merge_page(watermark_page)
                        writer.add_page(page)
                
                with open(output_file, 'wb') as output:
                    writer.write(output)
            
            # Clean up temporary watermark file
            os.remove(watermark_file)
            
            logger.info(f"Watermarked PDF saved as: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding watermark: {e}")
            return False
    
    def get_pdf_info(self, input_file: str) -> bool:
        """Get information about PDF file"""
        try:
            if not os.path.exists(input_file):
                logger.error(f"Input file not found: {input_file}")
                return False
            
            with open(input_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                print(f"\n=== PDF Information: {input_file} ===")
                print(f"Number of pages: {len(reader.pages)}")
                print(f"File size: {os.path.getsize(input_file)} bytes")
                
                # Get metadata if available
                if reader.metadata:
                    print("\nMetadata:")
                    for key, value in reader.metadata.items():
                        print(f"  {key}: {value}")
                
                # Get page dimensions for first page
                if reader.pages:
                    first_page = reader.pages[0]
                    mediabox = first_page.mediabox
                    print(f"\nFirst page dimensions:")
                    print(f"  Width: {float(mediabox.width)} points")
                    print(f"  Height: {float(mediabox.height)} points")
                
                return True
                
        except Exception as e:
            logger.error(f"Error getting PDF info: {e}")
            return False
    
    def create_sample_pdf(self, output_file: str, content: str = "Sample PDF Content") -> bool:
        """Create a sample PDF file"""
        try:
            c = canvas.Canvas(output_file, pagesize=letter)
            width, height = letter
            
            # Add title
            c.setFont("Helvetica-Bold", 24)
            c.drawString(100, height - 100, "Sample PDF Document")
            
            # Add content
            c.setFont("Helvetica", 12)
            lines = content.split('\n')
            y_position = height - 150
            
            for line in lines:
                if y_position < 50:  # Start new page if needed
                    c.showPage()
                    y_position = height - 50
                
                c.drawString(100, y_position, line)
                y_position -= 20
            
            # Add page numbers
            c.setFont("Helvetica", 10)
            c.drawString(width - 100, 30, f"Page {c.getPageNumber()}")
            
            c.save()
            logger.info(f"Sample PDF created: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating PDF: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='PDF Tool - Comprehensive PDF operations')
    parser.add_argument('operation', choices=[
        'merge', 'split', 'extract-text', 'rotate', 
        'watermark', 'info', 'create'
    ], help='Operation to perform')
    
    parser.add_argument('input', nargs='*', help='Input PDF file(s)')
    parser.add_argument('-o', '--output', help='Output file or directory')
    parser.add_argument('-a', '--angle', type=int, default=90, help='Rotation angle (default: 90)')
    parser.add_argument('-w', '--watermark', help='Watermark text')
    parser.add_argument('-p', '--pages', type=int, default=1, help='Pages per file when splitting')
    parser.add_argument('-c', '--content', default='Sample PDF Content', help='Content for sample PDF')
    
    args = parser.parse_args()
    
    tool = PDFTool()
    success = False
    
    try:
        if args.operation == 'merge':
            if len(args.input) < 2:
                print("Error: Merge operation requires at least 2 input files")
                return 1
            output = args.output or 'merged.pdf'
            success = tool.merge_pdfs(args.input, output)
            
        elif args.operation == 'split':
            if not args.input:
                print("Error: Split operation requires input file")
                return 1
            output = args.output or 'split_output'
            success = tool.split_pdf(args.input[0], output, args.pages)
            
        elif args.operation == 'extract-text':
            if not args.input:
                print("Error: Extract-text operation requires input file")
                return 1
            success = tool.extract_text(args.input[0], args.output)
            
        elif args.operation == 'rotate':
            if not args.input:
                print("Error: Rotate operation requires input file")
                return 1
            output = args.output or f'rotated_{args.input[0]}'
            success = tool.rotate_pdf(args.input[0], args.angle, output)
            
        elif args.operation == 'watermark':
            if not args.input or not args.watermark:
                print("Error: Watermark operation requires input file and watermark text")
                return 1
            output = args.output or f'watermarked_{args.input[0]}'
            success = tool.add_watermark(args.input[0], args.watermark, output)
            
        elif args.operation == 'info':
            if not args.input:
                print("Error: Info operation requires input file")
                return 1
            success = tool.get_pdf_info(args.input[0])
            
        elif args.operation == 'create':
            output = args.output or 'sample.pdf'
            success = tool.create_sample_pdf(output, args.content)
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
