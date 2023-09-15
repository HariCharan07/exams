from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List,Any
from datetime import datetime,timedelta
# from app.utills.pyObjId import PyObjectId


class groupPermissionsEnum(str, Enum):
    "Group Permissions Enum"
    public = "public"
    private = "private"
    protected = "protected"


class userStatusEnum(str, Enum):
    "User Status Enum"
    active = "active"
    inactive = "inactive"
    blocked = "blocked"
    deleted = "deleted"


class userActionsEnum(str, Enum):
    "User Actions Enum"
    login = "login"
    logout = "logout"
    register = "register"
    forgotPassword = "forgotPassword"
    resetPassword = "resetPassword"
    changePassword = "changePassword"
    verifyEmail = "verifyEmail"
    verifyMobile = "verifyMobile"
    mfaActivate = "mfaActivate"
    mfaDeactivate = "mfaDeactivate"
    

class strSchema(BaseModel):
    value: str
    

class listStrSchema(BaseModel):
    id:Optional[str]
    value: list[str]
    class Config:
        schema_extra = {
            "value": ["John Doe", "Jane Doe"]
        }

class locationSchema(BaseModel):
    coordinates: List[float]
    type: str = "Point"  
    label: Optional[str]  
    
    
class filtersSchema(BaseModel):
    id: Optional[str]
    value: Optional[str]
    start: Optional[int]
    page: Optional[int]
    limit: Optional[int]
    salaryMax: Optional[str]
    salaryMin: Optional[str]
    experienceMaxYears: Optional[int]
    experienceMinYears: Optional[int]
    location: Optional[list[str]]
    coords: Optional[locationSchema]
    distance: Optional[int]
    industry: Optional[str]
    jobType: Optional[list[str]]
    typeOfWorkplace: Optional[list[str]]
    
    class config:
        schema_extra = {
            "example": {
                "key":"name",
                "value":"John Doe",
            }
        
        }
    

class jobType(str, Enum):
    "Job Type Enum"
    fullTime = "fullTime"
    partTime = "partTime/internship"
    fullyRemote = "fullyRemote"
    empty=''



class workPlaceType(str, Enum):
    "Work Place Type Enum"
    office = "office"
    remote = "remote"
    hybrid = "hybrid"
    offSite = "offsite"
    onSite = "onSite"
    
    
    
class investorSchema(BaseModel):
    title:Optional[str]
    amount:Optional[str]
    category:Optional[str]
    image : Optional[str]
    descr:Optional[str]
    loc:Optional[str]

class idSchema(BaseModel):
    id: str
    recruiterId:Optional[str]
    
    

class postTypeEnum(str, Enum):
    "Post Type Enum"
    investorPost = "investorPost"
    expertAdvise = "expertAdvise"
    seekerJobPost = "seekerJobPost"
    generalPost = "generalPost"
    freelancerPost = "freelancerPost"
    eventPost = "eventPost"
    webinarPost = "webinarPost"
    

class durationSchema(BaseModel):
    years:Optional[int]
    months:Optional[int]
    days:Optional[int]
    hours:Optional[int]
    
    
    
class allPostSchema(BaseModel):
    #investorPostSchema
    postType:Optional[postTypeEnum]=postTypeEnum.generalPost
    title:Optional[str]
    amount:Optional[str]
    category:Optional[str]
    image : Optional[str]
    descr:Optional[str]
    loc:Optional[str]
    #jobPostSchema and seekerJobPostSchema
    jobTitle: Optional[str] 
    typeOfWorkPlace: Optional[workPlaceType] 
    jobLocation: Optional[locationSchema] 
    jobPlaces: Optional[List[str]] 
    job_type: Optional[jobType] 
    jobdescription: Optional[str] 
    experienceMaxYears: Optional[int] 
    experienceMaxMonths: Optional[int] 
    experienceMinYears: Optional[int] 
    experienceMinMonths: Optional[int] 
    requiredSkills: Optional[List[str]] 
    applicationDeadline: Optional[datetime] 
    salaryMax:Optional[str] 
    slaryMin:Optional[str] 
    qualifications:Optional[str] 
    jobIndustry:Optional[str]
    #expertAdviceSchema
    postData:Optional[str]
    userTypes:Optional[str]
    postedBy:Optional[str]
    postedAt:Optional[datetime] = datetime.now()
    enablePost:Optional[bool]=True
    currency:Optional[str]
    price:Optional[float]
    years:Optional[Any]
    months:Optional[Any]
    days:Optional[Any]
    startDate:Optional[datetime]=datetime.now() 
    endDate:Optional[datetime]=datetime.now() 
    webinarLink:Optional[str]
    webinarType:Optional[str]
    pricing:Optional[str]='unpaid'
    
    
class allPostUpdateSchema(BaseModel):
        # id : PyObjectId = Field(default_factory=PyObjectId, alias="_id")
        postType:Optional[str]
        title:Optional[str]
        amount:Optional[str]
        category:Optional[str]
        image : Optional[str]
        descr:Optional[str]
        loc:Optional[str]
        #jobPostSchema and seekerJobPostSchema
        jobTitle: Optional[str] 
        typeOfWorkPlace: Optional[workPlaceType] 
        jobLocation: Optional[locationSchema] 
        jobPlaces: Optional[List[str]] 
        job_type: Optional[jobType] 
        jobdescription: Optional[str] 
        experienceMaxYears: Optional[int] 
        experienceMaxMonths: Optional[int] 
        experienceMinYears: Optional[int] 
        experienceMinMonths: Optional[int] 
        requiredSkills: Optional[List[str]] 
        applicationDeadline: Optional[datetime] 
        salaryMax:Optional[str] 
        slaryMin:Optional[str] 
        qualifications:Optional[str] 
        jobIndustry:Optional[str]
        #expertAdviceSchema
        postData:Optional[str]
        userTypes:Optional[str]
        postedAt:Optional[datetime]
        enablePost:Optional[bool]=True
        currency:Optional[str]
        price:Optional[float]
        years:Optional[Any]
        months:Optional[Any]
        days:Optional[Any]
        startDate:Optional[datetime]=datetime.now() 
        endDate:Optional[datetime]=datetime.now() 
        webinarLink:Optional[str]
        webinarType:Optional[str]
        pricing:Optional[str]='unpaid'
        updatedBy:Optional[str]
        
        
        
        
class allPostMeSchema(BaseModel):
        id : str
        postType:Optional[str]
        title:Optional[str]
        amount:Optional[str]
        category:Optional[str]
        image : Optional[str]
        descr:Optional[str]
        loc:Optional[str]
        #jobPostSchema and seekerJobPostSchema
        jobTitle: Optional[str] 
        typeOfWorkPlace: workPlaceType 
        jobLocation: Optional[locationSchema] 
        jobPlaces: Optional[List[str]] 
        job_type: Optional[jobType] 
        jobdescription: Optional[str] 
        experienceMaxYears: Optional[int] 
        experienceMaxMonths: Optional[int] 
        experienceMinYears: Optional[int] 
        experienceMinMonths: Optional[int] 
        requiredSkills: Optional[List[str]] 
        applicationDeadline: Optional[datetime] 
        salaryMax:Optional[str] 
        slaryMin:Optional[str] 
        qualifications:Optional[str] 
        jobIndustry:Optional[str]
        #expertAdviceSchema
        postData:Optional[str]
        userTypes:Optional[str]
        postedBy:Optional[str]
        postedAt:Optional[datetime]
        enablePost:Optional[bool]=True
        


class friendStatusENum(str, Enum):
    "Friend Status Enum"
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    blocked = "blocked"
    ignored = "ignored"
    requested = "requested"



class addFriendSchema(BaseModel):
    userId: Optional[str]
    friendsList: Optional[str] 
    sentFriendRequest: Optional[str]
    getFriendRequest: Optional[str]
    

class friendSchema(BaseModel):
    reqPersonId: Optional[str]
    reqUserType: Optional[str]
    receiverId: Optional[str]
    status: Optional[friendStatusENum]=friendStatusENum.pending
    requestedAt: Optional[datetime]= datetime.now()
    

class friendShipStatusSchema(BaseModel):
    id: str
    reqPersonId: Optional[str]
    reqUserType: Optional[str]
    receiverId: Optional[str]
    status: Optional[friendStatusENum]=friendStatusENum.pending
    updatedAt: Optional[datetime]= datetime.now()    


#create schema for chatting
class chatSchema(BaseModel):
    # id: Optional[PyObjectId] = Field(alias="_id")
    message: str
    senderId: Optional[str]
    receiverId: str
    timeStamps: datetime = datetime.now()
    status: str = "sent"
    
    class config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        # json_encoders = {
        #     PyObjectId: str
        # }
    
class chatIdSchema(BaseModel):
    id: Optional[str]
    chatId:Optional[list[str]]
    friendId:Optional[str]
    
class showFriendSchema(BaseModel):
    id: Optional[str]



class filterSchema(BaseModel):
    value: Optional[str]
    start: Optional[int]
    page: Optional[int]
    limit: Optional[int]
    salaryMax: Optional[str]
    salaryMin: Optional[str]
    experienceMaxYears: Optional[int]
    location: Optional[list[str]]
    userType: Optional[str]

class contactUsSchema(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    subject: Optional[str]
    message: Optional[str]
    filePath: Optional[str]
    location: Optional[str]
    contactUsAt: Optional[datetime]= datetime.now()
    
    
class timeschema(BaseModel):
    id: Optional[str]
    startTime: Optional[datetime]= datetime.now()
    utcformat: Optional[str]= datetime.utcnow()
    timeDiff: Optional[str]= datetime.now() - datetime.utcnow()
    endTime: Optional[str]= datetime.now() + timedelta(hours=1)
    date: Optional[str]= datetime.now().strftime("%Y-%m-%d")
    day: Optional[str]= datetime.now().strftime("%A")
    
    
class esSearchSchema(BaseModel):
    value: Optional[str]
    title: Optional[str]
    jobType: Optional[str]
    
    
    
    
class recRequestSchema(BaseModel):
    reqPersonId: Optional[str]
    reqUserType: Optional[str]
    receiverId: Optional[str]
    status: Optional[friendStatusENum]=friendStatusENum.pending
    requestedAt: Optional[datetime]= datetime.now()
    value: Optional[str]
    
    
class addRecruiterSchema(BaseModel):
    userId: Optional[str]
    acceptId: Optional[str]
    recruiterList: Optional[str] 
    sentRecRequest: Optional[str]
    getRecRequest: Optional[str]
    
    


class kycSchema(BaseModel):
    adharCard: Optional[str]
    otp: Optional[str]
    ref_id: Optional[str]
    
    
    
    