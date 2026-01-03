"""
Environment constants loaded from environment variables.
"""
import os
from documents.domain.constants.domain_constants import TypeLogger

# API Core URL for agent communication
API_CORE_URL = os.getenv("API_CORE_URL", "http://localhost:8000")

# Logging type: LOCAL for development, GCP for production
LOGGING_TYPE = os.getenv("LOGGING_TYPE", TypeLogger.LOCAL)
