"""
Request models for API Core communication.
"""
from typing import List, Optional
from pydantic import BaseModel


class ApiCoreRequest(BaseModel):
    """
    Request model for invoking an agent in API Core.
    """
    agent_id: int
    message: Optional[str] = "Analiza los contratos y poliza"
    files: Optional[List[str]] = []
    use_raw_system_inst: Optional[bool] = True
