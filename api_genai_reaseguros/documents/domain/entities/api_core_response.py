"""
Response models for API Core communication.
"""
from pydantic import BaseModel
from typing import Generic, TypeVar, Any, Dict


T = TypeVar('T')


class DataResponse(BaseModel, Generic[T]):
    """Generic data response wrapper"""
    raw: str
    structured: T


class CoreResponse(BaseModel, Generic[T]):
    """Core response wrapper"""
    response: T


class ApiCoreResponse(BaseModel, Generic[T]):
    """
    Standard API Core response format.
    """
    success: bool
    data: CoreResponse[T]
