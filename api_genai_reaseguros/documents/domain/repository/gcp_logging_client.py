"""
GCP Cloud Logging client for production environments.
Sends logs to Google Cloud Logging service.
"""
import logging
from typing import Optional, Dict, Any
from uuid import uuid4
from .base_logger import BaseLogger

try:
    import google.cloud.logging
    from google.cloud.logging_v2 import Resource
    GCP_AVAILABLE = True
except ImportError:
    GCP_AVAILABLE = False


class GcpLoggerClient(BaseLogger):
    """
    Logger implementation for Google Cloud Platform.
    Sends logs to GCP Cloud Logging with trace support.
    """
    
    def __init__(
        self, 
        name: str,
        level: Optional[str] = logging.INFO
    ) -> None:
        """
        Initialize GCP logger client.
        
        Args:
            name: Name of the logger (usually the class/module name)
            level: Logging level (default: INFO)
        
        Raises:
            ImportError: If google-cloud-logging is not installed
        """
        if not GCP_AVAILABLE:
            raise ImportError(
                "google-cloud-logging is not installed. "
                "Install it with: pip install google-cloud-logging"
            )
        
        self.client = None
        self._setup_client(level)
        self.logger = self.client.logger(name)
        self.resource = self._get_resource()
        self.trace_id = None
    
    def _setup_client(self, level: str) -> None:
        """Setup GCP logging client"""
        self.client = google.cloud.logging.Client()
        self.client.setup_logging(log_level=level)
    
    def _get_resource(self) -> Resource:
        """Get GCP resource configuration"""
        return Resource(
            type="global",
            labels={
                "project_id": self.client.project
            }
        )
    
    def get_trace(self) -> str:
        """Get the current trace ID"""
        return self.trace_id

    def generate_trace(self) -> str:
        """Generate a new trace ID in GCP format"""
        self.trace_id = f"projects/{self.client.project}/traces/{uuid4().hex}"
        return self.trace_id

    def set_trace(self, trace_id: str) -> None:
        """
        Set the trace ID for this logger instance.
        
        Args:
            trace_id: Trace ID (can be simple string or GCP format)
        """
        # If it's not in GCP format, convert it
        if not trace_id.startswith("projects/"):
            self.trace_id = f"projects/{self.client.project}/traces/{trace_id}"
        else:
            self.trace_id = trace_id

    def log_text(
        self, 
        text: str,
        trace_id: Optional[str] = None, 
        severity: Optional[str] = logging.INFO
    ) -> None:
        """
        Log a text message to GCP Cloud Logging.
        
        Args:
            text: Message to log
            trace_id: Optional trace ID (uses instance trace_id if not provided)
            severity: Log level (INFO, WARNING, ERROR, DEBUG)
        """
        trace = trace_id or self.trace_id
        
        self.logger.log_text(
            text,
            severity=severity,
            resource=self.resource,
            trace=trace,
        )
    
    def log_struct(
        self, 
        payload: Dict[str, Any], 
        trace_id: Optional[str] = None, 
        severity: Optional[str] = logging.INFO
    ) -> None:
        """
        Log structured data to GCP Cloud Logging.
        
        Args:
            payload: Dictionary to log
            trace_id: Optional trace ID (uses instance trace_id if not provided)
            severity: Log level (INFO, WARNING, ERROR, DEBUG)
        """
        trace = trace_id or self.trace_id
        
        self.logger.log_struct(
            payload,
            severity=severity,
            resource=self.resource,
            trace=trace
        )
