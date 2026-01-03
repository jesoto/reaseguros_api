"""
HTML to PDF Conversion Service

Compiles HTML documents to PDF format using xhtml2pdf.
"""
import io
import logging
from typing import Optional
from xhtml2pdf import pisa
from documents.domain.logger import get_logger
from documents.domain.constants.env_constants import LOGGING_TYPE

class HtmlToPdfService:
    """Service for converting HTML documents to PDF format."""
    
    def __init__(self, trace_id: Optional[str] = None):
        """
        Initialize the HTML to PDF converter.
        
        Args:
            trace_id: Optional trace ID for logging
        """
        self.logger = get_logger(HtmlToPdfService.__name__, LOGGING_TYPE)
        if trace_id:
            self.logger.set_trace(trace_id)
        self.trace_id = trace_id
    
    def compile_html_to_pdf(self, html_content: str, filename: str = "document") -> Optional[bytes]:
        """
        Compile HTML content to PDF.
        
        Args:
            html_content: HTML document content as string
            filename: Base filename for the document (without extension)
        
        Returns:
            PDF content as bytes, or None if failed
        """
        self.logger.log_text(f"[HTML-PDF] Starting conversion for: {filename}")
        
        try:
            # Create a bytes buffer for the PDF
            pdf_buffer = io.BytesIO()
            
            # Convert HTML to PDF
            pisa_status = pisa.CreatePDF(
                src=html_content,
                dest=pdf_buffer,
                encoding='utf-8'
            )
            
            if pisa_status.err:
                error_msg = f"PDF generation failed: {pisa_status.err}"
                self.logger.log_text(f"[HTML-PDF] ERROR: {error_msg}", severity="ERROR")
                return None
            
            pdf_bytes = pdf_buffer.getvalue()
            pdf_size = len(pdf_bytes)
            
            self.logger.log_struct({
                "evento": "html_to_pdf_success",
                "filename": filename,
                "pdf_size_bytes": pdf_size,
                "pdf_size_kb": round(pdf_size / 1024, 2)
            })
            self.logger.log_text(f"[HTML-PDF] Conversion successful. PDF size: {pdf_size} bytes")
            
            return pdf_bytes
            
        except Exception as e:
            self.logger.log_text(f"[HTML-PDF] specific error: {str(e)}", severity="ERROR")
            import traceback
            traceback.print_exc()
            return None
