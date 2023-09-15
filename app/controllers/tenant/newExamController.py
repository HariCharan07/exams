from app.app import adminApp
from app.routes import tenantDashboardRouter as tdr
from fastapi import Depends ,UploadFile, File
from app.models.tenant.tenantModel import TenantUser
from app.libs.authJWT import *
import shutil
from app.schemas.user.candidateAssessmentSchema import examProgressSchema,examSubmitSchema
from sqlalchemy.orm import Session
from app.libs.mongoCLient import examProgressCollection,examSubmissionCollection,newQuestion_collection,examReportCollection,mailedcandidateCollection
from app.routes import getTenantInfo
from app.libs.mongoCLient import mongoDBClient
from fastapi import Response

from app.models.tenant.tennatAssessmentModel import assessmentModel
from app.schemas.user.candidateAssessmentSchema import filenameSchema,reportSchema,ImageFolderSchema,VideoFileSchema,getQuestionSchema
import bson
from bson import ObjectId
import pydantic
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str
from datetime import datetime
from app.utills.helper import serializeList,video_maker
from app.libs.mongoCLient import candidateCollection,mailedcandidateCollection,candidateSignupCollection
from app.controllers.tenant.newQuestionController import codeAsses



# GET QUESTIONS FOR CANDIDATES

# @adminApp.post('/newQuestionListSample')
# async def get_question(db: Session = Depends(get_db), Authoriza: AuthJWT = Depends()):
#     try:
#         claims=Authoriza.get_raw_jwt()
#         workspaceId=claims['workspaceId']
#         assessmentId=claims['assessmentId']
#         examId=claims['examId']
#         sortname=claims['sortname']
#         all_questions=serializeList(newQuestion_collection.find())
#         data = []
#         if int(workspaceId) == 0:
#             for i in all_questions:
#                 if i["tenant_sortname"] == sortname:
#                     data.append(i) 
                    
#         else:
#             for i in all_questions:
#                 if int(assessmentId) == 0:
#                     if str(i["tenant_sortname"]) == str(sortname) and int(i["workspace_id"]) == workspaceId:
#                         data.append(i)
#                 else:
#                         if int(i["assessment_id"]) == int(assessmentId) and (str(i["tenant_sortname"]) == sortname and int(i["workspace_id"]) == int(workspaceId)):
#                             data.append(i)    
                            
                                    
#         return {"status_code":200,
#                 "data":data
#                 }  
        
#     except Exception as e:
#         return {"status_code":500,
#                 "message":str(e)
#                 }    




# submit a answer of a question by candidate

@adminApp.post('/submitAnswer',tags=["Exam"])
async def answer_a_question(ans:examSubmitSchema,Authrize:AuthJWT=Depends()):
    try:
        ansData=ans.dict()
        answerCollection = mongoDBClient["answerCollection"]
        exist=answerCollection.find_one({"studentId":ans['studentId'],"examId":ans['examId'],"questionId":ans['questionId']})
        if exist:
            answerCollection.update_one({"studentId":ans['studentId'],"examId":ans['examId'],"questionId":ans['questionId']},{"$set":{"answer":ansData}})
            return {"status_code":200,
                    "message":"answer updated successfully"}
        
        answerCollection.insert_one(ans)
        return {"status_code":200,
                "message":"answer submitted successfully"}
        
    except Exception as e:
        return {"status_code":500,
                "message":str(e)}
        
        
        
# compare answer of a candidate with the correct answer
@adminApp.post('/compareAnswer',tags=["Exam"])
async def compareAnswer(ans:examSubmitSchema,Authrize:AuthJWT=Depends()):
    questionsdata=newQuestion_collection.find_one({"id":ans['questionId']})
    answerCollection = mongoDBClient["answerCollection"]
    answerCollection.find({"studentId":ans['studentId'],"examId":ans['examId'],"questionId":ans['questionId']})
    return {"status_code":200,
            "message":"answer compared successfully"}
    
    
        
    
  
@adminApp.post('/examSubmit',tags=["Exam"])
async def examSubmit(examSubmit: examSubmitSchema,Authorize: AuthJWT = Depends()):
    examSub=examSubmit.dict()   
    print(examSub)             
    getAnswer=newQuestion_collection.find({"id":examSub["questionId"]})
    if getAnswer[0]['type']!='coding':
            
        claims=Authorize.get_raw_jwt()
        examSub['tenant_sortname']=claims['tenant']
        examSub['assessmentId']=claims['assessmentId']
        examSub['studentId']=claims['studentId']
        examSub['workspaceId']=claims['workspaceId']
        examSub['examId']=claims['examId']
        examSub['questionData']=getAnswer[0]
        print("answer",getAnswer)
        
        if examSubmissionCollection.find_one({"studentId":examSub["studentId"],"examId":examSub["examId"],"questionId":examSub["questionId"]}):
            check=examSubmissionCollection.update_one({"studentId":examSub["studentId"],"examId":examSub["examId"],"questionId":examSub["questionId"]},{"$set":examSub})
            if check.modified_count==0:
                return {"status_code":500,
                        "message":"Answer not updated"}
            print(check)
            return {"status_code":200,
                    "message":"Answer  updated",
                    }
        print("answer")

        if getAnswer==[]:
            return {"status_code":200,
                    "data":"please enter answer in correct format"}
        answer=getAnswer[0]["selectedOptions"]
        examSub["correctAnswer"]=answer
        print(examSub["selectedOptions"],answer)
        answer.sort()
        print(answer.sort())
        examSub['selectedOptions'].sort()
        if answer==examSub["selectedOptions"]:
            examSub["isCorrect"]=True
            examSub["isSkipped"]=False
            examSub["isIncorrect"]=False
            examSub["marksObtained"]=+1
            examSubmissionCollection.insert_one(examSub)
            return {"status_code":200,
                    "message":"Answer  submitted",
                    }
        elif examSub["selectedOptions"]==[]:
            examSub["isSkipped"]=True
            examSub["isIncorrect"]=False
            examSub["isCorrect"]=False
            examSubmissionCollection.insert_one(examSub)
            return {"status_code":200,
                    "message":"Answer  submitted",
                    }
            
        examSub["isIncorrect"]=True  
        examSub["isCorrect"]=False  
        examSub["isSkipped"]=False
        examSubmissionCollection.insert_one(examSub)
        return {"status_code":200,
                "message":"Answer  submitted",
                }
    print("reached coding question")
    getCode=newQuestion_collection.find({"id":examSub["questionId"],"type":"coding"})
    examSub["marksObtained"]=+ int(examSub["noOfTestCasesPassed"])

    examSub['noOfTestCasesPassed']
    
    examSubmissionCollection.insert_one(examSub)
    return {"status_code":200,
            "message":"Answer  submitted",
            }
 


 




    
 


 
       