#!/usr/bin/env python3
"""
PDF Text Extractor Tool
A universal tool for extracting text from PDF files with support for:
- Page range extraction
- Section/chapter detection
- Multiple output formats (text, markdown, json)
- Preserving formatting and structure
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, List, Tuple

try:
    import pymupdf  # PyMuPDF (fitz)
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False
    print("Warning: PyMuPDF not installed. Install with: pip install pymupdf", file=sys.stderr)

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False
    print("Warning: pdfplumber not installed. Install with: pip install pdfplumber", file=sys.stderr)


class PDFExtractor:
    """Extract text from PDF files with various options."""
    
    def __init__(self, pdf_path: str, backend: str = "auto"):
        """
        Initialize PDF extractor.
        
        Args:
            pdf_path: Path to the PDF file
            backend: Extraction backend ('pymupdf', 'pdfplumber', or 'auto')
        """
        import os
        # Use os.path.exists() for better handling of special characters
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        self.pdf_path = Path(pdf_path)
        
        # Select backend
        if backend == "auto":
            if HAS_PYMUPDF:
                self.backend = "pymupdf"
            elif HAS_PDFPLUMBER:
                self.backend = "pdfplumber"
            else:
                raise RuntimeError("No PDF library available. Install pymupdf or pdfplumber.")
        else:
            self.backend = backend
            
        print(f"Using backend: {self.backend}", file=sys.stderr)
    
    def extract_pages(self, start_page: Optional[int] = None, 
                     end_page: Optional[int] = None) -> List[Dict]:
        """
        Extract text from specified page range.
        
        Args:
            start_page: Starting page number (1-indexed, inclusive)
            end_page: Ending page number (1-indexed, inclusive)
            
        Returns:
            List of dictionaries with page number and text
        """
        if self.backend == "pymupdf":
            return self._extract_with_pymupdf(start_page, end_page)
        elif self.backend == "pdfplumber":
            return self._extract_with_pdfplumber(start_page, end_page)
        else:
            raise ValueError(f"Unknown backend: {self.backend}")
    
    def _extract_with_pymupdf(self, start_page: Optional[int], 
                             end_page: Optional[int]) -> List[Dict]:
        """Extract using PyMuPDF (faster, better for most PDFs)."""
        import pymupdf
        
        doc = pymupdf.open(self.pdf_path)
        total_pages = len(doc)
        
        # Convert to 0-indexed
        start = (start_page - 1) if start_page else 0
        end = end_page if end_page else total_pages
        
        pages = []
        for page_num in range(start, min(end, total_pages)):
            page = doc[page_num]
            text = page.get_text()
            pages.append({
                "page_number": page_num + 1,
                "text": text
            })
        
        doc.close()
        return pages
    
    def _extract_with_pdfplumber(self, start_page: Optional[int], 
                                end_page: Optional[int]) -> List[Dict]:
        """Extract using pdfplumber (better for tables and complex layouts)."""
        import pdfplumber
        
        pages = []
        with pdfplumber.open(self.pdf_path) as pdf:
            total_pages = len(pdf.pages)
            
            # Convert to 0-indexed
            start = (start_page - 1) if start_page else 0
            end = end_page if end_page else total_pages
            
            for page_num in range(start, min(end, total_pages)):
                page = pdf.pages[page_num]
                text = page.extract_text()
                pages.append({
                    "page_number": page_num + 1,
                    "text": text or ""
                })
        
        return pages
    
    def find_section(self, section_pattern: str, 
                    start_page: Optional[int] = None,
                    end_page: Optional[int] = None) -> Optional[Tuple[int, int]]:
        """
        Find the page range of a section by pattern.
        
        Args:
            section_pattern: Pattern to search for (e.g., "14.1", "Chapter 14")
            start_page: Starting page to search from
            end_page: Ending page to search to
            
        Returns:
            Tuple of (start_page, end_page) or None if not found
        """
        pages = self.extract_pages(start_page, end_page)
        
        section_start = None
        section_end = None
        
        for i, page_data in enumerate(pages):
            text = page_data["text"]
            
            # Look for section start
            if section_start is None and section_pattern in text:
                section_start = page_data["page_number"]
            
            # Look for next section (simple heuristic)
            elif section_start is not None:
                # Check if we found the next section
                # This is a simple heuristic - you might need to customize this
                lines = text.split('\n')
                for line in lines:
                    # Look for patterns like "14.2", "14.3", etc.
                    if line.strip().startswith(tuple('0123456789')):
                        parts = line.split()
                        if parts and parts[0] != section_pattern:
                            section_end = page_data["page_number"] - 1
                            return (section_start, section_end)
        
        # If we found the start but not the end, use the last page
        if section_start is not None:
            section_end = pages[-1]["page_number"]
            return (section_start, section_end)
        
        return None
    
    def extract_to_text(self, pages: List[Dict], 
                       include_page_numbers: bool = True) -> str:
        """Convert extracted pages to plain text."""
        lines = []
        for page_data in pages:
            if include_page_numbers:
                lines.append(f"\n{'='*60}")
                lines.append(f"Page {page_data['page_number']}")
                lines.append(f"{'='*60}\n")
            lines.append(page_data["text"])
        
        return "\n".join(lines)
    
    def extract_to_markdown(self, pages: List[Dict]) -> str:
        """Convert extracted pages to markdown format."""
        lines = []
        for page_data in pages:
            lines.append(f"\n## Page {page_data['page_number']}\n")
            lines.append(page_data["text"])
        
        return "\n".join(lines)
    
    def extract_to_json(self, pages: List[Dict]) -> str:
        """Convert extracted pages to JSON format."""
        return json.dumps(pages, indent=2, ensure_ascii=False)


def main():
    """Command-line interface for PDF extraction."""
    parser = argparse.ArgumentParser(
        description="Extract text from PDF files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract pages 297-316
  %(prog)s input.pdf --start 297 --end 316
  
  # Extract and save to file
  %(prog)s input.pdf --start 297 --end 316 --output output.txt
  
  # Extract in markdown format
  %(prog)s input.pdf --start 297 --end 316 --format markdown
  
  # Find and extract a specific section
  %(prog)s input.pdf --section "14.1" --search-start 297 --search-end 316
        """
    )
    
    parser.add_argument("pdf_file", help="Path to PDF file")
    parser.add_argument("--start", type=int, help="Start page (1-indexed, inclusive)")
    parser.add_argument("--end", type=int, help="End page (1-indexed, inclusive)")
    parser.add_argument("--section", help="Section pattern to find (e.g., '14.1')")
    parser.add_argument("--search-start", type=int, help="Start page for section search")
    parser.add_argument("--search-end", type=int, help="End page for section search")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--format", choices=["text", "markdown", "json"], 
                       default="text", help="Output format")
    parser.add_argument("--backend", choices=["pymupdf", "pdfplumber", "auto"],
                       default="auto", help="PDF extraction backend")
    parser.add_argument("--no-page-numbers", action="store_true",
                       help="Don't include page numbers in text output")
    
    args = parser.parse_args()
    
    try:
        extractor = PDFExtractor(args.pdf_file, backend=args.backend)
        
        # Determine page range
        if args.section:
            print(f"Searching for section '{args.section}'...", file=sys.stderr)
            result = extractor.find_section(
                args.section, 
                args.search_start, 
                args.search_end
            )
            if result:
                start_page, end_page = result
                print(f"Found section at pages {start_page}-{end_page}", file=sys.stderr)
            else:
                print(f"Section '{args.section}' not found", file=sys.stderr)
                return 1
        else:
            start_page = args.start
            end_page = args.end
        
        # Extract pages
        print(f"Extracting pages {start_page or 'first'} to {end_page or 'last'}...", 
              file=sys.stderr)
        pages = extractor.extract_pages(start_page, end_page)
        
        # Format output
        if args.format == "text":
            output = extractor.extract_to_text(pages, not args.no_page_numbers)
        elif args.format == "markdown":
            output = extractor.extract_to_markdown(pages)
        elif args.format == "json":
            output = extractor.extract_to_json(pages)
        
        # Write output
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(output, encoding="utf-8")
            print(f"Output written to: {output_path}", file=sys.stderr)
        else:
            print(output)
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
