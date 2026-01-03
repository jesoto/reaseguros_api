"""
Logger factory module.
Provides a centralized way to get logger instances based on environment configuration.
"""
from typing import Optional
from documents.domain.repository.local_logging import LocalLogger
from documents.domain.repository.gcp_logging_client import GcpLoggerClient
from documents.domain.constants.domain_constants import TypeLogger
from documents.domain.repository.base_logger import BaseLogger

# Cache for logger instances (singleton pattern)
DICT_LOGGER = {}


def get_logger(name: str, logger_type: Optional[str] = TypeLogger.LOCAL) -> BaseLogger:
    """
    Get or create a logger instance.
    
    This function implements a singleton pattern - it caches logger instances
    by name to avoid creating multiple loggers for the same component.
    
    Args:
        name: Name of the logger (typically the class or module name)
        logger_type: Type of logger to create (TypeLogger.LOCAL or TypeLogger.GCP)
    
    Returns:
        BaseLogger: A logger instance (LocalLogger or GcpLoggerClient)
    
    Example:
        >>> from documents.domain.logger import get_logger
        >>> from documents.domain.constants.env_constants import LOGGING_TYPE
        >>> 
        >>> logger = get_logger("MyService", LOGGING_TYPE)
        >>> logger.set_trace("abc123")
        >>> logger.log_text("Processing started")
        >>> logger.log_struct({"status": "success", "count": 5})
    """
    
    # Return cached logger if it exists
    if name in DICT_LOGGER:
        return DICT_LOGGER[name]
    
    # Create new logger based on type
    if logger_type == TypeLogger.GCP:
        try:
            DICT_LOGGER[name] = GcpLoggerClient(name)
        except Exception as e:
            # Fallback to local logger if GCP fails (e.g. missing credentials)
            print(f"WARNING: Failed to initialize GCP logger: {e}. Falling back to LocalLogger.")
            DICT_LOGGER[name] = LocalLogger(name)
    else:
        # Default to LocalLogger for development
        DICT_LOGGER[name] = LocalLogger(name)
    
    return DICT_LOGGER[name]
