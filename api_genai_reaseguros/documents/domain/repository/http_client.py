"""
HTTP client base class.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class HttpClient(ABC):
    """
    Abstract base class for HTTP clients.
    """
    
    @abstractmethod
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None):
        """HTTP GET request"""
        pass
    
    @abstractmethod
    def post(self, endpoint: str, data: Optional[Any] = None, 
             json: Optional[Dict[str, Any]] = None, files: Optional[Any] = None):
        """HTTP POST request"""
        pass
    
    @abstractmethod
    def put(self, endpoint: str, data: Optional[Any] = None,
            json: Optional[Dict[str, Any]] = None, files: Optional[Any] = None):
        """HTTP PUT request"""
        pass
