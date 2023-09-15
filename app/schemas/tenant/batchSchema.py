from pydantic import BaseModel
from typing import Optional, List, Any
from app.schemas.globalSchemas import userStatusEnum

class batchSchema(BaseModel):
    id: Optional[str]
    sortname : Optional[str]
    name : str
    description : str
    color : Optional[str]
    image : Optional[str]   
    status : Optional[userStatusEnum] = userStatusEnum.active
    
    
    
class batchUpdateSchema(BaseModel):
    id: Optional[str]
    name : Optional[str]
    description : Optional[str]
    color : Optional[str]
    image : Optional[str]   
    status : Optional[userStatusEnum] = userStatusEnum.active    
    
         
    
    
class batchIdSchema(BaseModel):
    id : Optional[str]