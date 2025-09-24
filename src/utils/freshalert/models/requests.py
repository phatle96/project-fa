"""
Request models for Fresh Alert API endpoints.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProductFilterParams(BaseModel):
    """Query parameters for filtering products"""
    days: Optional[int] = Field(None, description="Number of days for lookback (used in expired endpoint)")
    
    class Config:
        extra = "forbid"  # Don't allow extra fields