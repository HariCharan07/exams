from pydantic import BaseModel, EmailStr, Field

from typing import Optional, List
 
#schema to create a section list

class sectionListSchema(BaseModel):
    sectionDetails: dict
    assessmentId: str
    workspaceId: str
class updateSectionListSchema(BaseModel):
    sectionDetails: dict
    id: str    
class idSchema(BaseModel):
    id: str  
class idSchemas(BaseModel):
    assessmentId: str
    workspaceId: str

   