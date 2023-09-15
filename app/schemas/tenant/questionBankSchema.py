from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from fastapi import  UploadFile
from app.schemas.globalSchemas import userStatusEnum


class questionBankSchema(BaseModel):
    workspace_id: Optional[int]
    assessment_id: Optional[int]
    tenant_id: Optional[int]
    tenant_sortname: Optional[str]
    user_id: Optional[int]
    question: str
    questionType: str
    option1: Optional[str]
    option2: Optional[str]
    option3: Optional[str]
    option4: Optional[str]
    option5: Optional[str]
    answer: Optional[List[str]]
    hints: Optional[List[str]]
    chapter: Optional[str]
    topic: Optional[str]
    tags: Optional[List[str]]
    instruction: Optional[str]
    marks: Optional[int]
    negativeMarks: Optional[int]
    duration: Optional[int]
    supportedLanguages: Optional[List[str]]
    defaultCode: Optional[str]
    correctCode: Optional[str]
    testCases: Optional[Any]
    difficultyLevel: str
    status: Optional[userStatusEnum] = userStatusEnum.active
    updated_by: Optional[int]
    deleted_by: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]
    deleted_at: Optional[str]
    
    
    
    
    
#class to update question
class updateQuestionSchema(BaseModel):
    questionId: Optional[int]
    workspaceId: Optional[int]
    assessmentId: Optional[int]
    question: Optional[str]
    questionType: Optional[str]
    option1: Optional[str]
    option2: Optional[str]
    option3: Optional[str]
    option4: Optional[str]
    option5: Optional[str]
    answer: Optional[List[str]]
    hints: Optional[List[str]]
    chapter: Optional[str]
    topic: Optional[str]
    tags: Optional[List[str]]
    instruction: Optional[str]
    marks: Optional[int]
    negativeMarks: Optional[int]
    duration: Optional[int]
    supportedLanguages: Optional[List[str]]
    defaultCode: Optional[str]
    correctCode: Optional[str]
    testCases: Optional[Any]
    difficultyLevel: Optional[str]
    status: Optional[str]
    updated_by: Optional[int]
    deleted_by: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]
    deleted_at: Optional[str]    
    
    
    
        

    
    
class uploadBulkQuestion(BaseModel):
    arry: List[questionBankSchema]
    
    
class fetchQuestionSchema(BaseModel):
    questionId: Optional[str]  
    workspaceId: Optional[int]
    assessmentId: Optional[int]
    
    

class newQuestionSchema(BaseModel):
    id: Optional[str]
    questionBankId: Optional[str]
    assessment_id: Optional[int]
    workspace_id: Optional[str]
    tenant_id: Optional[int]
    tenant_sortname: Optional[str]
    user_id: Optional[int]
    sectionId: Optional[str]
    question: str
    description: Optional[str]
    # difficultyLevel: Optional[difficultyEnum]=difficultyEnum.medium
    type: str
    testCases: Optional[Any]
    examples:Optional[Any]
    numberOfExamples:Optional[int]
    exampleA: Optional[str]
    exampleB: Optional[str]
    exampleC: Optional[str]
    exampleD: Optional[str]
    exampleE: Optional[str]
    programmingLanguage: Optional[str]
    parameters: Optional[str]
    startupCode: Optional[str]
    studentCode: Optional[str]
    noOfTestCasesPassed: Optional[int]
    numberOfOptions: str
    imgUrl: Optional[str]
    optionA: Optional[str]
    optionB: Optional[str]
    optionC: Optional[str]
    optionD: Optional[str]
    optionE: Optional[str]
    selectedOptions: Optional[List]=None   
    
    
    
class newQuestionUpdateSchemaUpdate(BaseModel):
    id: Optional[str]
    question: Optional[str]
    type: Optional[str]
    numberOfOptions: Optional[str]
    testCases: Optional[Any]
    examples:Optional[Any]
    numberOfExamples:Optional[int]
    exampleA: Optional[str]
    exampleB: Optional[str]
    exampleC: Optional[str]
    exampleD: Optional[str]
    exampleE: Optional[str]
    programmingLanguage: Optional[str]
    parameters: Optional[str]
    startupCode: Optional[str]
    studentCode: Optional[str]
    noOfTestCasesPassed: Optional[int]
    imgUrl: Optional[str]
    optionA: Optional[str]
    optionB: Optional[str]
    optionC: Optional[str]
    optionD: Optional[str]
    optionE: Optional[str]
    selectedOptions: Optional[List]=None
    testCases: Optional[Any]
    programmingLanguage: Optional[str]
    parameters: Optional[str]
    startupCode: Optional[str]
    updatedBy: Optional[str]
       
    
    
class UploadBulk(BaseModel):
    array: List[newQuestionSchema]
    
    
    

class idSchema(BaseModel):
    id: Optional[str]
    assessment_id: Optional[str]
    new_assessment_id: Optional[str]
    destination_workspace_id: Optional[str]   
    
    
    
class questionIdSchema(BaseModel):
    id: Optional[str]
    assessment_id: Optional[str]
    workspace_id: Optional[str]
