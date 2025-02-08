from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import date

class Department(BaseModel):
    """A department or program within a division."""
    unit_id: int = Field(description="The ID of the department as used inside Interfolio.")
    unit_name: str = Field(description="The name of the department.")

class Division(BaseModel):
    """A school or division that may contain departments."""
    unit_id: int = Field(description="The ID of the unit used inside Interfolio.")
    unit_name: str = Field(description="The name of the unit.")
    departments: List[Department] = Field(default_factory=list, description="The departments that are part of this unit.")

class DivisionResponse(BaseModel):
    """Response containing all divisions and their departments."""
    divisions: List[Division] = Field(description="List of all divisions and their departments")

class FacultyProfile(BaseModel):
    """Faculty profile information."""
    email: str
    employmentstatus: str
    firstname: str
    lastname: str
    lastlogin: Optional[date] = None
    middlename: str = ""
    pid: int
    position: Optional[str] = None
    primaryunit: Optional[int] = None
    rank: Optional[str] = None
    userid: str
    web_profile: bool

class FacultyResponse(BaseModel):
    """Response containing faculty profiles."""
    faculty: List[FacultyProfile]

class Position(BaseModel):
    """An open faculty position."""
    location: str
    unit_name: str
    name: str
    open_date: str
    deadline: str
    legacy_position_id: str

class PositionsResponse(BaseModel):
    """Response containing open positions."""
    results: List[Position]