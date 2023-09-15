from pydantic import BaseModel,EmailStr
from typing import Optional,List
from datetime import datetime

class codeExecutioSchema(BaseModel):
    code: str
    questionId: str
    programmingLanguage: str
    
    
class genUser(BaseModel):
    name:str
    email:EmailStr
    # phonenumber:str
    password:str  
    role:str


class examProgressSchema(BaseModel):
    examId: int
    studentId: int
    studentName: Optional[str]
    studentImage: Optional[str]
    assessmentName: Optional[str]
    assessmentTime:Optional[datetime]
    noOfTotalQuestions: Optional[int]
    noOfSkippedQuestions: Optional[int]
    noOfCorrectQuestions: Optional[int]=0
    noOfInCorrectQuestions: Optional[int]=0
    totalMarksObtained: Optional[int]=0
    allQuestionslist: Optional[list]
    timeStamp: Optional[datetime]  = datetime.now()
    timeExpired:Optional[bool]=False
    
    
class examSubmitSchema(BaseModel):
    questionData: Optional[list]
    examId: Optional[str]
    question: Optional[str]
    studentId: Optional[str]
    assessmentId: Optional[int]
    workspaceId: Optional[int]
    tenantSortname: Optional[str]
    examProgressId: Optional[str]
    questionId: Optional[str]
    isCorrect: Optional[bool]
    isIncorrect: Optional[bool]
    isSkipped: Optional[bool]=False
    selectedOptions: Optional[list]
    studentCode: Optional[str]
    noOfTestCasesPassed: Optional[int]
    programmingLanguage: Optional[str]
    correctAnswer: Optional[int]=0
    marksObtained: Optional[int]=0
    timestamp: Optional[str]  = datetime.now().isoformat() 
    timeTaken: Optional[datetime] = 20



class reportSchema(BaseModel):
    examId: str
    studentId: str
    assessmentId:Optional[str]
    workspaceId: Optional[str]
    sortname: Optional[str]
    sudentName: Optional[str]
    profileImage: Optional[str]
    assessmentName: Optional[str]
    assessmentTime:Optional[datetime]
    # examProgressId: int
    # questionId: str
    noOfQuestions: Optional[int] =0
    noOfCorrectQuestions: Optional[int] =0
    noOfInCorrectQuestions: Optional[int] =0
    noOfSkippedQuestions: Optional[int] =0
    totalMarksObtained: Optional[int] =0
    allQuestionslist: Optional[list] =[]
    timestamp: Optional[datetime]  = datetime.now().isoformat()    
    
    
class filenameSchema(BaseModel):
    filename: str   
    
class ImageFolderSchema(BaseModel):
    folder_path: str

class VideoFileSchema(BaseModel):
    file_path: str    
    

class candidateSchema(BaseModel):
    batchId: Optional[str]
    name: Optional[str]
    email: EmailStr
    mobile: Optional[str]
    assessmentStatus: Optional[str] = 'pending'
    
    
class startExamSchema(BaseModel):
    examID: str
        
   

class candidateUpdateSchema(BaseModel):
    id: Optional[str]
    batchId: Optional[str]
    name: Optional[str]
    mobile: Optional[str]
    email: Optional[EmailStr]
    assessmentStatus: Optional[str] = 'pending'
    
    
class batchSchema(BaseModel):
    id : Optional[str]
    name : str
    description : str
    color : Optional[str]
    image : Optional[str]   
    status : Optional[str] = 'active' 
    
    
class idSchema(BaseModel):
    id : Optional[str]
    
    
    
class getQuestionSchema(BaseModel):
    id: Optional[str]
    assessment_id: Optional[str]
    new_assessment_id: Optional[str]
    destination_workspace_id: Optional[str]     
    
class bulkIdSchema(BaseModel):
    array: List[idSchema]
    workspaceId: Optional[str]
    assessmentId: Optional[str]
    assessmentDetails: Optional[List[dict]]
   
   
   
class mailedCandidateSchema(BaseModel):
    assessmentId: Optional[str]
    workspaceId: Optional[str]   
    
    
class PasswordSchema(BaseModel):
    password: str
    email:Optional[EmailStr]
    date:Optional[datetime] = datetime.now()
    email: Optional[EmailStr]
    studentId: Optional[str]
    examId: Optional[str]
    assessmentId: Optional[str]
    workspaceId: Optional[str]
    assessmentDetails: Optional[List[dict]]