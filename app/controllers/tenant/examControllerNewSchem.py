from app.app import adminApp
from app.routes import tenantDashboardRouter as tdr
from fastapi import Depends ,UploadFile, File
from app.models.tenant.tenantModel import TenantUser
from app.libs.authJWT import *
import shutil
from app.schemas.user.candidateAssessmentSchema import examProgressSchema,examSubmitSchema
from app.libs.psqlDBClient import get_db
from app.libs.mongoCLient import mongoDBClient
from app.libs.mongoCLient import examProgressCollection,examSubmissionCollection,newQuestion_collection,examReportCollection,mailedcandidateCollection
from app.routes import getTenantInfo
from fastapi import Response

from app.models.tenant.tennatAssessmentModel import assessmentModel
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

@adminApp.post('/newQuestionList')
async def get_question(db: Session = Depends(get_db), Authoriza: AuthJWT = Depends()):
    # try:
        claims=Authoriza.get_raw_jwt()
        workspaceId=claims['workspaceId']
        assessmentId=claims['assessmentId']
        examId=claims['examId']
        sortname=claims['sortname']
        all_questions=serializeList(newQuestion_collection.find())
        data = []
        try:
            assessmentDuration= assessmentModel.find_one
            {"$and": [ {"_id": int(assessmentId)},{"tenantWorkspaceId": int(workspaceId)}]}
            print(assessmentDuration)
        except:
            assessmentDuration=assessmentModel.find_one
            {"$and": [ {"_id": int(assessmentId)},{"tenantWorkspaceId": int(workspaceId)}]}
            print(assessmentDuration)
            data.append({"duration":assessmentDuration})
        if int(workspaceId) == 0:
            for i in all_questions:
                if i["tenant_sortname"] == sortname:
                    data.append(i) 
                    
        else:
            for i in all_questions:
                if int(assessmentId) == 0:
                    if str(i["tenant_sortname"]) == str(sortname) and int(i["workspace_id"]) == workspaceId:
                        data.append(i)
                else:
                        if int(i["assessment_id"]) == int(assessmentId) and (str(i["tenant_sortname"]) == sortname and int(i["workspace_id"]) == int(workspaceId)):
                            data.append(i)    
                            
        
                                    
        return {"status_code":200,
                "data":data,
                "duration":assessmentDuration
                }  
        
    # except Exception as e:
    #     return {"status_code":500,
    #             "message":str(e)
    #             }    





#to exam progress
@adminApp.post('/examProgress',tags=["Exam"])
async def examProgress(response: Response,examProgress: examProgressSchema, Authorize: AuthJWT = Depends()):
    try:
        claims = Authorize.get_raw_jwt()
        if claims['studentId'] == examProgress.studentId and claims['examId'] == examProgress.examId:
        # if True:
            examProgressData=examProgress.dict()
            examProgressData["timeStamp"]=datetime.now()
            result = examProgressCollection.insert_one(examProgressData)
            id = str(result.inserted_id)
            access_token =Authorize.create_access_token(subject=str(id), expires_time=3600,
                            user_claims= {
                                "progressId" : id,
                                "examId" : examProgress.examId,
                                "studentId" : examProgress.studentId,
                                "startTime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            })
            response.set_cookie(
                key="access_token",
                value=f"Bearer {access_token}",
                httponly=True,
                expires=3600,
            )
            return {"status_code": 200,
                    "message": "examProgress created successfully"}
        questions=newQuestion_collection.find({"assessment_id":examProgress.examId})
        noOfTotalQuestions=len(questions)
        progress=examProgress.dict()
        previous_marks=examSubmissionCollection.find().sort("_id", -1)
        previously_marks=previous_marks[0]["marksObtained"] 
        checkAllQuestions = examSubmissionCollection.find()
        allQuestions=newQuestion_collection.find()
        for i in checkAllQuestions: 
            if i["isCorrect"]==True:
                progress["noOfCorrectQuestions"]+=1
                progress["totalMarksObtained"]=1
            elif i["isIncorrect"]==True:
                progress["noOfInCorrectQuestions"]+=1
                # if db.execute("select isNegativeMarking from exam where id=:id",{"id":i["examId"]}).scalar():
                #     progress["totalmarksObtained"]=previously_marks - 1  
            else:
                # progress["noOfSkippedQuestions"]+=1  
                progress["noOfTotalQuestions"]=len(questions)
        print(noOfTotalQuestions)    
        result = examProgressCollection.insert_one(progress)
        results=examProgressCollection.find({"_id":result.inserted_id})
        id = str(result.inserted_id)
        startTime=results[0]["timeStamp"].strftime("%Y-%m-%d %H:%M:%S")
        access_token =Authorize.create_access_token(subject=str(id), expires_time=3600,
                        user_claims= {
                            "progressId" : id,
                            "examId" : examProgress.examId,
                            "studentId" : examProgress.studentId,
                            "startTime" : startTime,
                        })
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, samesite="none", secure=True)
        return {
                        "status_code": 200,
                        "message":"progress added",
                        "access_token": access_token,
                        "questions":questions,
                        "result":results,
                    }
    except Exception as e:
        return {"status_code":400,
                "message":str(e),
                "data":"Please Contact Admin"
                }    


    



@adminApp.post('/examSubmit',tags=["Exam"])
async def examSubmit(examSubmit: examSubmitSchema,Authorize: AuthJWT = Depends()):
    examSub=examSubmit.dict()      
    claims=Authorize.get_raw_jwt()
    examSub['tenant_sortname']=claims['sortname']
    examSub['assessmentId']=claims['assessmentId']
    examSub['studentId']=claims['studentId']
    examSub['workspaceId']=claims['workspaceId']
    examSub['examId']=claims['examId']   
    getAnswer=newQuestion_collection.find({"id":examSub["questionId"]})
    if getAnswer[0]['type'] != 'coding':
        
        examSub['questionData']=getAnswer[0]
        print("answer",getAnswer)
        
        if examSubmissionCollection.find_one({"questionId":examSub['questionId'],'studentId':examSub['studentId']}):
            print(examSub['questionId'])
            if getAnswer==[]:
                return {"status_code":200,
                    "message":"Answer  submitted",
                    "data":"please enter answer in correct format"}
            answer=getAnswer[0]["selectedOptions"]
            examSub["correctAnswer"]=answer
            print(examSub["selectedOptions"],answer)
            answer.sort()
            examSub['selectedOptions'].sort()
            if answer==examSub["selectedOptions"]:
                examSub["isCorrect"]=True
                examSub["isSkipped"]=False
                examSub["isIncorrect"]=False
                examSub["marksObtained"]=+1
                examSubmissionCollection.update_one({"questionId":examSub["questionId"]},{"$set":examSub})
                print('updating answer')
                return {"status_code":200,
                        "message":"Answer  submitted",
                        }
            elif examSub["selectedOptions"]==[]:
                examSub["isSkipped"]=True
                examSub["isIncorrect"]=False
                examSub["isCorrect"]=False
                examSubmissionCollection.update_one({"questionId":examSub["questionId"]},{"$set":examSub})
                print('updating answer')
                return {"status_code":200,
                        "message":"Answer  submitted",
                        }
                
            examSub["isIncorrect"]=True  
            examSub["isCorrect"]=False  
            examSub["isSkipped"]=False
            examSubmissionCollection.update_one({"questionId":examSub["questionId"]},{"$set":examSub})
            print('updating answer')
            return {"status_code":200,
                    "message":"Answer  submitted",
                    }
        
            
        
        if getAnswer==[]:
            return {"status_code":200,
                    "message":"Answer  submitted",
                    "data":"please enter answer in correct format"}
        answer=getAnswer[0]["selectedOptions"]
        examSub["correctAnswer"]=answer
        print(examSub["selectedOptions"],answer)
        answer.sort()
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
    else:
            if examSubmissionCollection.find_one({"questionId":examSub['questionId'],'studentId':examSub['studentId']}):
                examSub['questionData']=getAnswer[0]
                getCode=newQuestion_collection.find({"id":examSub["questionId"],"type":"coding"})
                examSub["marksObtained"]=+ int(examSub["noOfTestCasesPassed"])

                examSub['noOfTestCasesPassed']
                examSubmissionCollection.update_one({"questionId":examSub["questionId"]},{"$set":examSub})
                return {"status_code":200,"message":"Answer  updated",}
            

            print("reached coding question")
            
            examSub['questionData']=getAnswer[0]
            getCode=newQuestion_collection.find({"id":examSub["questionId"],"type":"coding"})
            examSub["marksObtained"]=+ int(examSub["noOfTestCasesPassed"])

            examSub['noOfTestCasesPassed']
            examSub["isCorrect"]=True
            
            examSubmissionCollection.insert_one(examSub)
            return {"status_code":200,
                    "message":"Answer  submitted",
                    }
    
    
 


 
        
@adminApp.post('/exam', tags=["Exam"])
async def exam(examProgress: examProgressSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):

    # Get all the questions from the database
    all_questions = newQuestion_collection.find()
    questions_data = []
    for question in all_questions:
        questions_data.append(question)
        
    # Insert the exam progress into the database
    progress = examProgress.dict()
    result = examProgressCollection.insert_one(progress)
    progress_id = str(result.inserted_id)

    # Create an access token containing the progress ID and other information
    access_token = Authorize.create_access_token(
        subject=progress_id,
        expires_time=3600,
        user_claims={
            "progressId": progress_id,
            "examId": examProgress.assessmentId,
            "studentid": examProgress.studentId,
        }
    )

    # Return the questions and progress information in the response
    return {
        "status_code": 200,
        "data": questions_data,
        "access_token": access_token
    }
        


# # to send report to the candidate of the exam
# @tdr.post('/examReport',tags=["Exam"])
# async def examReport(examReport: reportSchema,Authorize: AuthJWT = Depends(),tenant_sortname: str = Depends(getTenantInfo)):
#     try:
#         previously_marks=0
#         checkAllQuestions = examSubmissionCollection.find()
#         allAnswers=examSubmissionCollection.find()
#         assessment=[]
#         for i in allAnswers:
#             if i['studentId']==examReport.studentId and i['examId']==examReport.examId:
#                 assessment.append(i)
#         examreport=examReport.dict()
       
#         j=0
#         for i in checkAllQuestions:
#             if i['studentId']==examreport['studentId'] and i['examId']==examreport['examId']:
#                 j+=1
#                 if i["isCorrect"]==True:
#                     examreport["noOfCorrectQuestions"]+=1
#                     # print(examreport["noOfCorrectQuestions"])
#                     examreport["totalMarksObtained"]=examreport["totalMarksObtained"] + 1
#                 elif i["isIncorrect"]==True:
#                     examreport["noOfInCorrectQuestions"]+=1
#                     # if db.execute("select isNegativeMarking from exam where id=:id",{"id":i["examId"]}).scalar():
#                     #     examreport["totalmarksObtained"]=previously_marks - 1  
#                 else:
#                     examreport["noOfSkippedQuestions"]+=1
                    
                    
#             examreport["totalQuestions"]=j        
                    
#             result=examReportCollection.insert_one(examreport)      
#             Report_id = str(result.inserted_id)


#             return {"status_code":200,
#                     "message":"report generated  successfully",
#                     "report_id":Report_id,
#                     "data":examReportCollection.find_one({"_id":ObjectId(Report_id)}),
#                     "questionsList":assessment,
#                     }            
#     except Exception as e:
#         print(e)
#         return {"status_code":400,
#                 "message":"report not generated successfully",
#                 "data":str(e)
#                 }    
        
        
        
        
        
        
        
        
        
        
  
        
# api to submit whole exam
@adminApp.post('/examComplete',tags=["Exam"])    
async def completedExam(Authorize: AuthJWT = Depends()):
    try:
        claims = Authorize.get_raw_jwt()
        assessment=claims['assessmentId']
        tenant=claims['sortname']
        user=claims['studentId']
        claims = Authorize.get_raw_jwt()
        examId=claims['examId']
        studentId=claims['studentId']
        assessmentStatus="completed"
        # video_maker(r"D:\defTroven\troven-api\upload\tenant1\assessment2\userf") 
        # video_maker(r"/home/ubuntu/bucket/tenant1/assessment2/userScreen1")    

        candidateCollection.update_one({"_id":ObjectId(studentId)},{"$set":{"assessmentStatus":assessmentStatus,"examId":examId,"examCompletedAt":datetime.now()}})
        cand=mailedcandidateCollection.update_one({"studentId":studentId},{"$set":{"assessmentStatus":assessmentStatus,"examId":examId,"examCompletedAt":datetime.now(),"tenant_sortname":"tenant"}})
        if cand.modified_count==1:
            print("updated in mailed candidate collection")
        # candidateSignupCollection.update_one({"studentId":studentId},{"$set":{"assessmentStatus":assessmentStatus,"examId":examId,"examCompletedAt":datetime.now()}})
        assessmentCollection=mongoDBClient['assessmentCollection']
        assessmentCollection.update_one({"studentId":studentId,"examId":examId}, {"$set": {"examCompletedAt": datetime.now(),"assessmentStatus":"Completed"}})
        

        return {"status_code":200,
                "message":"exam completed successfully",
                "data":"exam completed successfully"
                }
        
    except Exception as e:
        return {"status_code":400,
                "message":"exam not completed successfully",
                "data":str(e)
                }    
        
        
 
     
# to send report to the candidate of the exam
@tdr.post('/examReport',tags=["Exam"])
async def examReport(examReport: reportSchema,Authorize: AuthJWT = Depends(),db:Session=Depends(get_db)):
    # try:
            previously_marks=0
            examreport=examReport.dict()

            claims=Authorize.get_raw_jwt()
            sortname=claims['sortname']
            
            
            
            #************************sectionwise percentage****************
        #     for i in assessmentList:
                        
        #     pipeline = [
        #     {"$group": {
        #         "_id": {"workspace_id": "$workspace_id", "assessment_id": "$assessment_id"},
        #         "category": {"$push": "$$ROOT"}
        #     }}
        # ]
        #     output = examSubmissionCollection.aggregate(pipeline)
            
            #************************End sectionwise percentage****************
  
            
            studentDetails=mailedcandidateCollection.find_one({"studentId":examreport['studentId']})
            
            reprtExist=examReportCollection.find_one({"studentId":examreport["studentId"],"examId":examreport["examId"]})
            
            
            WA=examSubmissionCollection.find_one({"examId":examreport["examId"]})
            # print(WA)
            

            print(WA['assessmentId'],WA['workspaceId'])
            db.execute(text('SET search_path TO {}'.format(sortname)))
            try:
                passingmark=db.query(assessmentModel).filter(assessmentModel.id==WA["assessmentId"],assessmentModel.tenantWorkspaceId==WA['workspaceId']).first().passMarks
                    # return {passingmark,"try block"}
                print(passingmark,"try block")
            except:
                sort=db.execute(text('SET search_path TO {}'.format(sortname)))

                # passingmark=db.query(assessmentModel).filter(assessmentModel.id==WA["assessmentId"],assessmentModel.tenantWorkspaceId==WA['workspaceId']).first().passMarks
                    # return {passingmark,"except block"}
                     
            else:
                passingmark=db.query(assessmentModel).filter(assessmentModel.id==WA["assessmentId"],assessmentModel.tenantWorkspaceId==WA['workspaceId']).first().passMarks
                    # return {passingmark,"except block"}
                     
                print(passingmark,"except block")
            
            marksTotal=db.query(assessmentModel).filter(assessmentModel.id==WA["assessmentId"],assessmentModel.tenantWorkspaceId==WA['workspaceId']).first().totalMarks
            passingmark=db.query(assessmentModel).filter(assessmentModel.id==WA["assessmentId"],assessmentModel.tenantWorkspaceId==WA['workspaceId']).first().passMarks
            query = {"tenant_sortname":sortname,"workspace_id":WA["workspaceId"],"assessment_id":int(WA["assessmentId"])}
            print(query)
                
            all_questions=newQuestion_collection.find(query)
            # print(list(all_questions) ,"all_questions")
            # return {"status_code":200,}
            question=[]
            for i in list(all_questions):
                question.append(i)
                print(len(question))
                print(passingmark,marksTotal)
            checkAllQuestions = serializeList(examSubmissionCollection.find())
            
            questionsList=[]
            
            for i in checkAllQuestions:
                if i["studentId"]==examreport['studentId'] and i["examId"]==examreport['examId']:
                
                    questionsList.append(i)
                    if i["isCorrect"]==True:
                        # print(examreport["noOfCorrectQuestions"])
                        examreport["noOfCorrectQuestions"]+=1
                        # print(examreport["noOfCorrectQuestions"])
                        examreport["totalMarksObtained"]=examreport["totalMarksObtained"] + 1
                    elif i["isIncorrect"]==True:
                        examreport["noOfInCorrectQuestions"]+=1
                        # print(previously_marks)
                        # if db.execute("select isNegativeMarking from exam where id=:id",{"id":i["examId"]}).scalar():
                        #     examreport["totalmarksObtained"]=previously_marks - 1  
                    else:
                        examreport["noOfSkippedQuestions"]+=1 
                        
                    # video_maker(r"D:\defTroven\troven-api\upload\tenant1\assessment2\userf")     
            if reprtExist:
                return {"status_code":200,
                        "message":"report already generated",
                        "data":reprtExist,
                        "questionList":questionsList,
                        "studentDetails":studentDetails,
                        }
                
            
                
            examreport['noOfQuestions']=len(question)
            examreport["noOfSkippedQuestions"]=examreport["noOfQuestions"]-examreport["noOfCorrectQuestions"]-examreport["noOfInCorrectQuestions"] 

            percentage=(examreport["totalMarksObtained"]/marksTotal)*100
            passingPercentage=(passingmark/marksTotal)*100
            if percentage>=passingPercentage:
                examreport["status"]="Pass"
            else:
                examreport["status"]="Fail"
            examreport["percentage"]=percentage
            examreport['assessmentId']=WA['assessmentId']
            examreport['workspaceId']=WA['workspaceId']
            examreport['sortname']=sortname
            result=examReportCollection.insert_one(examreport)      
            Report_id = str(result.inserted_id)
            
            
        
                
            


            return {"status_code":200,
                    "data":"report generated successfully successfully",
                    "report_id":Report_id,
                    "questionList":questionsList,
                    "data":examReportCollection.find_one({"_id":ObjectId(Report_id)},),
                    "studentDetails":studentDetails,

                    }            
    # except Exception as e:
    #     print(e)
    #     return {"status_code":400,
    #             "message":"report not generated successfully",
    #             "data":str(e)
    #             }    



