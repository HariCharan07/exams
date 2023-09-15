from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime
from app.schemas.globalSchemas import userStatusEnum

class assessmentSchema(BaseModel):
    id :Optional[str] 
    name : str
    color : Optional[str]
    description : Optional[str]
    instructions : Optional[str]
    tenantWorkspaceId : Optional[int]
    duration :Optional[int]
    # difficultyLevel:Optional[difficultyEnum]=difficultyEnum.medium
    totalMarks : Optional[int] 
    negativeMarks : Optional[float]
    passMarks : Optional[int]
    showResult : Optional[bool]
    status:Optional[userStatusEnum]=userStatusEnum.active
    bannerImage : Optional[str]
    sponserId : Optional[str]
    registered: Optional[int]
    qualified:Optional[int]
    completed:Optional[int]
    disableRightClick:Optional[bool]
    disableCopyPaste:Optional[bool]
    startWithFullScreen:Optional[bool]
    submitOnTabSwitch:Optional[bool]
    enableWebCam:Optional[bool]
    enableMicrophone:Optional[bool]
    allowMobile:Optional[bool]
    mfaVerification:Optional[bool]
    isEmailOtpVerified : Optional[bool]
    created_by : Optional[int]
    created_at :Optional[datetime] = datetime.now()
    updated_at :Optional[datetime] = datetime.now()
    deleted_at :Optional[datetime]

    
    
class idSchema(BaseModel):
    id: Optional[str]  
    email: Optional[str]
    
    
class cloneAssessmentSchema(BaseModel):
    workspaceId: Optional[int]
    destinationWorkspaceId: Optional[int]
    assessmentId: Optional[int]    
    
    
    
class id(BaseModel):
    id: Optional[str]  
    
class idSchemas(BaseModel):
    array: List[id]   
    workspaceId: Optional[int]
    assessmentId: Optional[int] 
    
       


class updateAssessmentSchema(BaseModel):
    id: Optional[int]
    tenantWorkspaceId: int
    name: str
    description: Optional[str]
    duration: Optional[int]
    totalMarks: Optional[int]
    passMarks: Optional[int]
    negativeMarks: Optional[int]
    # difficultyLevel: Optional[difficultyEnum]=difficultyEnum.medium
    status: str="active"
    sponserId: Optional[int]
    examStartDate: Optional[datetime] = datetime.now()
    created_at: Optional[str]  = datetime.now()
    updated_at: Optional[str] = datetime.now()
    deleted_at: Optional[str] = datetime.now()
    examEndDate:Optional[datetime] = datetime.now()    
    
    

class assessmentIdSchema(BaseModel):
    id: str
    tenantWorkspaceId: Optional[int]
    status: Optional[userStatusEnum]=userStatusEnum.active
    
    
    

       
    
    
      
    