from sqlalchemy import String, Integer, Float, Column, types
from pydantic import BaseModel
from typing import Optional


class IdQuery(BaseModel):
    """
    Query class to fetch by id
    """
    id: str


class SearchQuery(BaseModel):
    """
    Query for searching a specific object or range of objects
    """
    name: Optional[str] = None
    abs_mag_min: Optional[float] = None
    abs_mag_max: Optional[float] = None
    diameter_min: Optional[float] = None
    diameter_max: Optional[float] = None
    inclination_min: Optional[float] = None
    inclination_max: Optional[float] = None


class LargestQuery(BaseModel):
    """
    Query for fetching the top N largest objects
    """
    top_n: Optional[int] = 10
