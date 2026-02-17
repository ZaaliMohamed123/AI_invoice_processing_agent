"""
PDF Service - Extract text from PDF invoices.
"""
import pdfplumber
from pathlib import Path


class PDFExtractionError(Exception):
    """Raised when PDF text extraction fails."""
    pass


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all text content from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as a single string
        
    Raises:
        PDFExtractionError: If the PDF cannot be read or has no text
    """
    path = Path(pdf_path)
    
    # Validate file exists
    if not path.exists():
        raise PDFExtractionError(f"PDF file not found: {pdf_path}")
    
    # Validate file extension
    if path.suffix.lower() != ".pdf":
        raise PDFExtractionError(f"File is not a PDF: {pdf_path}")
    
    try:
        text_parts = []
        
        with pdfplumber.open(pdf_path) as pdf:
            # Check if PDF has pages
            if len(pdf.pages) == 0:
                raise PDFExtractionError("PDF has no pages")
            
            # Extract text from each page
            for page_num, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()
                
                if page_text:
                    text_parts.append(page_text)
        
        # Combine all pages
        full_text = "\n\n".join(text_parts)
        
        # Check if we extracted any text
        if not full_text.strip():
            raise PDFExtractionError(
                "No text could be extracted from PDF. "
                "The PDF might be scanned/image-based and require OCR."
            )
        
        return clean_text(full_text)
        
    except Exception as e:
        if isinstance(e, PDFExtractionError):
            raise
        if "PDFSyntaxError" in type(e).__name__:
            raise PDFExtractionError(f"Invalid or corrupt PDF file: {e}")
        raise PDFExtractionError(f"Failed to extract text from PDF: {e}")


def clean_text(text: str) -> str:
    """
    Clean and normalize extracted PDF text.
    
    Args:
        text: Raw extracted text
        
    Returns:
        Cleaned text with normalized whitespace
    """
    # Replace multiple spaces with single space
    import re
    text = re.sub(r' +', ' ', text)
    
    # Replace multiple newlines with double newline (paragraph break)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def get_pdf_info(pdf_path: str) -> dict:
    """
    Get metadata information about a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary with PDF metadata
    """
    path = Path(pdf_path)
    
    if not path.exists():
        raise PDFExtractionError(f"PDF file not found: {pdf_path}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return {
                "page_count": len(pdf.pages),
                "file_size_kb": round(path.stat().st_size / 1024, 2),
            }
    except Exception as e:
        raise PDFExtractionError(f"Failed to read PDF info: {e}")
