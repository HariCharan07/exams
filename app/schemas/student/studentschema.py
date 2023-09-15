from fastapi import FastAPI
from pydantic import BaseModel
from bson import ObjectId
from typing import Optional
from datetime import datetime
class studentsignup(BaseModel):
    sid:str
    studentname:str
    password :str
    dob:str
    gender:str
    email:str
    mno:int
    age:int
    address: str
    city: str
    country: str
    postal_code: str
    
class studentLoginSchema(BaseModel):
    email: str
    password: str 
class studentForgotPasswordSchema(BaseModel):
    email: str


class Assessment(BaseModel):
    id: int
    WorkspaceId: str
class assesmsentScheema(BaseModel):
    id:int
    name:str
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
    # status:Optional[userStatusEnum]=userStatusEnum.active
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

    

class studentResetPasswordSchema(BaseModel):
    password: str
    otp: str

class studentChangePasswordSchema(BaseModel):
    oldPassword: str 
    newPassword: str

class studentVerifyOtpSchema(BaseModel):
    otp: str

class studentPasswordSchema(BaseModel):
    email:str
    password: str
    otp:Optional[str]

class studentStrSchema(BaseModel):
    str: str

class studentIntSchema(BaseModel):
    id: int

class studentChangePassword(BaseModel):
    
    old_password:str
    new_password:str
class studentMobileLogin(BaseModel):
    mobile:str
    password:str

class studentEmailOtpLogin(BaseModel):
    email:str
class studentemailverifyotplogin(BaseModel):
    otp:str
