#models.py
from pydantic import BaseModel
from typing import List, Optional

class AttendanceLogItem(BaseModel):
    EmployeeId: str
    Timestamp: str
    EmployeeName: str
    MatchDistance: float

class EmployeeDetailsItem(BaseModel):
    EmployeeId: str
    EmployeeName: str
    PhoneNumber: str
    Address: Optional[str] = None  # Made optional
    Department: Optional[str] = None  # Made optional
    Email: Optional[str] = None  # Made optional

class EmployeeEmbeddingItem(BaseModel):
    EmployeeId: str
    EmbeddingVector: List[float]

class EmployeeFaceItem(BaseModel):
    EmployeeId: str
    FaceImage: Optional[str] = None  # Base64 string
