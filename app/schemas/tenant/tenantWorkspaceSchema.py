from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from app.schemas.globalSchemas import userStatusEnum


class tenantWorkspaceSchema(BaseModel):
    id: str
    name: str
    description: Optional[str]
    color:Optional [str]
    image: Optional[str]
    status:Optional [userStatusEnum]=userStatusEnum.active
    created_at: Optional[datetime] = datetime.now()
    created_by: Optional[str]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    
class tennatWorkspaceUpdateSchema(BaseModel):
    id: str
    name: Optional[str]
    description: Optional[str]
    color: Optional[str]
    image: Optional[str]
    status: Optional[userStatusEnum]=userStatusEnum.active
    created_by: Optional[str]
    updated_at: Optional[datetime] = datetime.now()


class tenantWorkspaceIdSchema(BaseModel):
    id: int