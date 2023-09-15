from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Any
from datetime import datetime
# from app.schemas.globalSchemas import userStatusEnum
from enum import Enum
class RoleEnum(str, Enum):
    "Admin Role Enum"
    admin = "admin"
    superAdmin = "superAdmin"
    moderator = "moderator"
    creator = "creator"

class tenantTempSchema(BaseModel):
    name:  str
    company: str
    sortname: str
    email: EmailStr
    mobile: str
    password: str
    # role: Optional[RoleEnum] = RoleEnum.superAdmin
    profilePic: Optional[str]
    isMobileVerified: Optional[bool] = False
    isEmailVerified: Optional[bool] = False
    mfa: Optional[bool] = False
    mfaSecretCode: Optional[str]
    emailOtp: Optional[str]
    emailOtpCreatedAt: Optional[datetime]
    mobileOtp: Optional[str]
    mobileOtpCreatedAt: Optional[datetime]
    # status: Optional[userStatusEnum] = userStatusEnum.active
    Tfa: Optional[bool] = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
class userEmailSchema(BaseModel):
    email: EmailStr
    otp: Optional[str]
    
class TenantSchema(BaseModel):
    name: str
    sortname: str
    description: str
    companyLogo: Optional[str]
    status: str
    subscriptionId: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
class TenantLoginSchema(BaseModel):
    email: EmailStr
    password: str
    
    

class passwordResetSchema(BaseModel):
    email: Optional[EmailStr]
    otp: Optional[str]
    password: Optional[str]   
    
    

class changeProfileIamgeSchema(BaseModel):
    id:Optional[str]
    email: Optional[EmailStr]
    profileImage: Optional[str]    
    
class changePasswordSchema(BaseModel):
    id:Optional[str]
    email: Optional[EmailStr]
    oldPassword: Optional[str]
    newPassword: Optional[str]        
    
class tenantUserSchema(BaseModel):
    name:  str
    company: Optional[str]
    sortname: Optional[str]
    email: EmailStr
    mobile: str
    password: str
    role: Optional[RoleEnum] = RoleEnum.moderator
    profilePic: Optional[str]
    isMobileVerified: Optional[bool] = False
    isEmailVerified: Optional[bool] = False
    mfa: Optional[bool] = False
    mfaSecretCode: Optional[str]
    emailOtp: Optional[str]
    emailOtpCreatedAt: Optional[datetime]
    mobileOtp: Optional[str]
    mobileOtpCreatedAt: Optional[datetime]
    # status: Optional[userStatusEnum] = userStatusEnum.active
    Tfa: Optional[bool] = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]  
    
    
    
class tenantUserMeSchema(BaseModel):
    id: str
    name: str
    email: EmailStr
    mobile: str
    role: Optional[RoleEnum] = RoleEnum.moderator
    profilePic: Optional[str]
    isMobileVerified: Optional[bool] = False
    isEmailVerified: Optional[bool] = False
    mfa: Optional[bool] = False
    mfaSecretCode: Optional[str]
    emailOtp: Optional[str]
    emailOtpCreatedAt: Optional[datetime]
    mobileOtp: Optional[str]
    mobileOtpCreatedAt: Optional[datetime]
    # status: Optional[userStatusEnum] = userStatusEnum.active
    Tfa: Optional[bool] = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]    
    
    
class updateTenantUserSchema(BaseModel):
    name:  Optional[str]
    id:Optional[str]
    mobile: Optional[str]
    role: Optional[str] 
    password: Optional[str]
    status: Optional[str]
    email: Optional[EmailStr]
    
    
class tenantStrSchema(BaseModel):
    str: str   
    
    
class emailTempSchema(BaseModel):
    id: Optional[int]
    templateType: str
    templateContent: str
    templateName: Optional[str]
    created_by: Optional[int]
    created_at: Optional[datetime]=datetime.now()
    status: Optional[str]  = 'active'
    visibility: Optional[bool]=True
    
    
class userIdSchema(BaseModel):
    id: str    
    
class tenantSortnameSchema(BaseModel):
    sortname: str    
    
class profileImageSchema(BaseModel):
    profileImage: str    
    
    
class tenantMeUpdateSchema(BaseModel):
    name: Optional[str]
    mobile: Optional[str]
    profilePic: Optional[str]  
    
    
class tenantUserChangePasswordSchema(BaseModel):
    oldPassword: str 
    newPassword: str      
class tenantForgotPasswordSchema(BaseModel):
    email:str
class tenantVerifyOtpSchema(BaseModel):
    otp: str
