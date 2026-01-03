"""
Base logger interface that all logger implementations must follow.
"""
import logging
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod


class BaseLogger(ABC):
    """
    Abstract base class for logger implementations.
    Provides interface for logging text and structured data with trace support.
    """
    
    @abstractmethod
    def generate_trace(self) -> str:
        """Generate a new unique trace ID"""
        pass
    
    @abstractmethod
    def set_trace(self, trace_id: str) -> None:
        """Set the trace ID for this logger instance"""
        pass
    
    @abstractmethod
    def get_trace(self) -> str:
        """Get the current trace ID"""
        pass
    
    @abstractmethod
    def log_text(
        self, 
        text: str,
        trace_id: Optional[str] = None, 
        severity: Optional[str] = logging.INFO
    ) -> None:
        """Log a text message"""
        pass
    
    @abstractmethod
    def log_struct(
        self, 
        payload: Dict[str, Any], 
        trace_id: Optional[str] = None, 
        severity: Optional[str] = logging.INFO
    ) -> None:
        """Log structured data (dict/JSON)"""
        pass
