"""
Local logger implementation for development/testing.
Logs to console with formatted output.
"""
import logging
import json
from typing import Optional, Dict, Any
from uuid import uuid4
from .base_logger import BaseLogger


class LocalLogger(BaseLogger):
    """
    Logger implementation for local development.
    Outputs logs to console with color formatting and trace IDs.
    """
    
    def __init__(self, name: str):
        """
        Initialize local logger.
        
        Args:
            name: Name of the logger (usually the class/module name)
        """
        self.name = name
        self.trace_id = None
        
        # Configure logging format
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.logger = logging.getLogger(name)
    
    def set_trace(self, trace_id: str) -> None:
        """Set the trace ID for this logger instance"""
        self.trace_id = trace_id
    
    def get_trace(self) -> str:
        """Get the current trace ID"""
        return self.trace_id

    def generate_trace(self) -> str:
        """Generate a new unique trace ID using UUID"""
        self.trace_id = f"{uuid4().hex}"
        return self.trace_id

    def log_text(
        self, 
        text: str, 
        trace_id: Optional[str] = None,
        severity: str = "INFO"
    ) -> None:
        """
        Log a text message to console.
        
        Args:
            text: Message to log
            trace_id: Optional trace ID (uses instance trace_id if not provided)
            severity: Log level (INFO, WARNING, ERROR, DEBUG)
        """
        trace = trace_id or self.trace_id
        log_fn = getattr(logging, severity.lower(), logging.info)
        
        message = f"{text}"
        if trace:
            message += f" [trace_id={trace}]"
        
        log_fn(message)

    def log_struct(
        self, 
        payload: Dict[str, Any], 
        trace_id: Optional[str] = None,
        severity: str = "INFO"
    ) -> None:
        """
        Log structured data (dict) to console as formatted JSON.
        
        Args:
            payload: Dictionary to log
            trace_id: Optional trace ID (uses instance trace_id if not provided)
            severity: Log level (INFO, WARNING, ERROR, DEBUG)
        """
        trace = trace_id or self.trace_id
        
        # Format the payload as pretty JSON
        try:
            formatted_payload = json.dumps(payload, indent=2, ensure_ascii=False)
        except (TypeError, ValueError):
            formatted_payload = str(payload)
        
        message = f"Structured Log:\n{formatted_payload}"
        if trace:
            message += f"\n[trace_id={trace}]"
        
        self.log_text(message, trace_id=trace, severity=severity)
