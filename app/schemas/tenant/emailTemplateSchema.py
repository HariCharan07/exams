from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class emailTempSchema(BaseModel):
    id: Optional[int]
    templateType: str
    templateContent: str
    templateName: Optional[str]
    created_by: Optional[int]
    created_at: Optional[datetime]=datetime.now()
    status: Optional[str]  = 'active'
    visibility: Optional[bool]=True
    
    
    
class updateEmailTempSchema(BaseModel):
    id:Optional[int]
    templateType: str
    templateContent: str
    templateName: Optional[str]
    created_by: Optional[int]
    created_at: Optional[datetime]=datetime.now()
    status: Optional[str]  = 'active'
    visibility: Optional[bool]=True    
    
    
class temptype(BaseModel):
    templateType: str 
    
    
class idSchema(BaseModel):
    id:str        