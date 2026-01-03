"""
GCP API Client for communicating with API Core service.
Handles authentication and HTTP requests with bearer tokens.
"""
import requests
import time
from typing import Dict, Any, TypeVar, Type, Optional, Union
from pydantic import BaseModel

from documents.domain.logger import get_logger
from documents.domain.constants.env_constants import LOGGING_TYPE
from .http_client import HttpClient

try:
    import google.oauth2.id_token
    import google.auth.transport.requests
    GCP_AUTH_AVAILABLE = True
except ImportError:
    GCP_AUTH_AVAILABLE = False


T = TypeVar("T", bound=BaseModel)
GenericJsonResponse = Dict[str, Any]
UnionModelJsonResponse = Union[GenericJsonResponse, T]

# Default token expiration time (in seconds)
DEFAULT_EXPIRATION_TIME = 3600  # 1 hour


class GcpApiClient(HttpClient):
    """
    HTTP client for GCP services with automatic bearer token authentication.
    """
    
    def __init__(
        self, 
        base_url: str,
        trace_id: str, 
        expiration_token_time: int = DEFAULT_EXPIRATION_TIME,
        use_auth: bool = True
    ):
        """
        Initialize GCP API client.
        
        Args:
            base_url: Base URL of the API Core service
            trace_id: Trace ID for logging
            expiration_token_time: Token expiration time in seconds
            use_auth: Whether to use GCP authentication (set False for local testing)
        """
        super().__init__()
        self.base_url = base_url
        self.token = None
        self.token_expiry = 0
        self.expiration_token_time = expiration_token_time
        self.use_auth = use_auth and GCP_AUTH_AVAILABLE
        
        # Initialize logger
        self.logger = get_logger(GcpApiClient.__name__, LOGGING_TYPE)
        self.trace_id = trace_id
        self.logger.set_trace(trace_id)
        
        if self.use_auth and not GCP_AUTH_AVAILABLE:
            self.logger.log_text(
                "GCP authentication libraries not available. Install with: "
                "pip install google-auth google-auth-oauthlib",
                severity="WARNING"
            )
    
    def _get_bearer_token(self) -> str:
        """
        Get a bearer token for GCP service authentication.
        
        Returns:
            Bearer token string
        """
        if not self.use_auth:
            return "mock-token-for-local-testing"
        
        request = google.auth.transport.requests.Request()
        target_audience = self.base_url
        id_token = google.oauth2.id_token.fetch_id_token(request, target_audience)
        return id_token
    
    def get_access_token(self) -> str:
        """
        Get access token, refreshing if expired.
        
        Returns:
            Valid access token
        """
        if self.token is None or time.time() > self.token_expiry:
            self.token = self._get_bearer_token()
            self.token_expiry = time.time() + self.expiration_token_time
            self.logger.log_text("Access token refreshed")
        
        return self.token
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Get HTTP headers with authentication.
        
        Returns:
            Headers dictionary
        """
        headers = {
            'Content-Type': 'application/json'
        }
        
        if self.use_auth:
            headers['Authorization'] = f'Bearer {self.get_access_token()}'
        
        return headers

    def valid_http_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Validate HTTP response and return JSON.
        
        Args:
            response: HTTP response object
        
        Returns:
            JSON response as dictionary
        
        Raises:
            HTTPError: If response status is >= 400
        """
        if response.status_code < 400:
            return response.json()
        
        # Log error
        self.logger.log_text(
            f"HTTP Error {response.status_code}: {response.text}",
            severity="ERROR"
        )
        response.raise_for_status()

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        HTTP GET request.
        
        Args:
            endpoint: API endpoint (relative to base_url)
            params: Query parameters
        
        Returns:
            JSON response
        """
        url = f"{self.base_url}/{endpoint}"
        
        self.logger.log_text(f"GET {url}")
        
        response = requests.get(
            url, 
            headers=self._get_headers(),
            params=params
        )

        return self.valid_http_response(response)

    def post(
        self, 
        endpoint: str, 
        data: Optional[Any] = None, 
        json: Optional[Dict[str, Any]] = None, 
        files: Optional[Any] = None, 
        model_response: Optional[Type[T]] = None
    ) -> UnionModelJsonResponse:
        """
        HTTP POST request.
        
        Args:
            endpoint: API endpoint (relative to base_url)
            data: Form data
            json: JSON payload
            files: Files to upload
            model_response: Optional Pydantic model to parse response
        
        Returns:
            JSON response or Pydantic model instance
        """
        url = f"{self.base_url}/{endpoint}"
        
        self.logger.log_text(f"POST {url}")
        if json:
            self.logger.log_struct({"request_payload": json})
        
        response = requests.post(
            url, 
            headers=self._get_headers(), 
            data=data, 
            json=json, 
            files=files
        )

        valid_json_response = self.valid_http_response(response)
        
        self.logger.log_struct({"response": valid_json_response})
        
        # Parse to Pydantic model if requested
        if model_response is not None:
            return model_response(**valid_json_response)
        
        return valid_json_response
    
    def put(
        self, 
        endpoint: str, 
        data: Optional[Any] = None, 
        json: Optional[Dict[str, Any]] = None, 
        files: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        HTTP PUT request.
        
        Args:
            endpoint: API endpoint (relative to base_url)
            data: Form data
            json: JSON payload
            files: Files to upload
        
        Returns:
            JSON response
        """
        url = f"{self.base_url}/{endpoint}"
        
        self.logger.log_text(f"PUT {url}")
        
        response = requests.put(
            url, 
            headers=self._get_headers(), 
            data=data, 
            json=json, 
            files=files
        )

        return self.valid_http_response(response)
