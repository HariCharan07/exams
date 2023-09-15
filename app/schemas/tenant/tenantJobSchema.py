from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class jobSchema(BaseModel):
    id: Optional[int]
    name: str
    description: str
    minExperienceYr: int
    minExperienceMn: int
    maxExperienceYr: int
    maxExperienceMn: int
    minSalary: int
    maxSalary: int
    currency: str
    jobType: str
    jobLocation: str
    jobSkills: List[str]
    jobRoles: List[str]
    status: str
    createdAt: Optional[datetime] = datetime.now()
    updatedAt: Optional[datetime]
    updatedBy: Optional[int]