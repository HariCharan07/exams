from pydantic import BaseModel,EmailStr
from typing import Optional


class sponserSchema(BaseModel):
    id: Optional[str]
    name: str
    description: Optional[str]
    website: Optional[str]
    logo: Optional[str]
    
    
class sponserUpdateSchema(BaseModel):
    name: str
    description: Optional[str]
    website: Optional[str]
    logo: Optional[str]
    
    
class sponserIdSchema(BaseModel):
    id: str        
