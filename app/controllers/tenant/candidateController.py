from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from typing import Union


from app.libs.mongoclient import mongoDBClient
from pymongo import MongoClient
from app.libs.mongoclient import question_collection

from app.libs.smsClient import sendsms
import json
import bson.json_util
from app.libs.authJWT import *
from app.schemas.tenant.candidateAssessmentSchema import candidateSchema,candidateUpdateSchema,idSchema,PasswordSchema,ImageFolderSchema,bulkIdSchema,mailedCandidateSchema
from datetime import datetime, timedelta
from app.utils.helper import serializeList
from app.settings import FERNET_KEY
from app.libs.mongoclient import candidateCollection,mailedcandidateCollection,candidateSignupCollection
from bson.objectid import ObjectId
from fastapi.responses import RedirectResponse
import pydantic
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str
import uuid
from datetime import datetime
import hashlib
from app.app import app as tdr



        
# create candidate and store it to mongo db      
@tdr.post("/createCandidate",tags=["candiates"])
async def createCandidate(newCandidate:candidateSchema,Authorize: AuthJWT = Depends()):  
    # Authorize.jwt_required()
    if len(newCandidate.mobile) < 10 or len(newCandidate.mobile) > 12:
        return {"status_code": 400,
                "message": "Invalid mobile number"}
    candidate=newCandidate.dict()
    candidateCollection.insert_one(candidate)
    return {"status_code": 200,
            "message": "candidate added successfully"}
@tdr.post("/getCandidate",tags=["candiates"])
async def getCandidate(id:idSchema,Authorize: AuthJWT = Depends()):  
    # Authorize.jwt_required()
    all_candidate=serializeList(candidateCollection.find())
    if id.id:
        for i in all_candidate:
            if i['_id']==id.id:
                return {"status_code":200,"data":i}
    return {"status_code":200,"data":all_candidate}



@tdr.post("/getAllCandidateWithBatchId",tags=["candiates"])
async def getCandidate(id:idSchema,Authorize: AuthJWT = Depends()):  
    # Authorize.jwt_required()
    all_candidate=serializeList(candidateCollection.find())
    data=[]
    # print(all_candidate)
    for i in all_candidate:
        if i['batchId']==id.id:
            data.append(i)
    return {"status_code":200,"data":data}



#to delete a candidate from mongo db by id
@tdr.post("/deleteCandidate",tags=["candiates"])
def delete_candidate(id:idSchema,Authorize: AuthJWT = Depends()):  
    # Authorize.jwt_required()
    candidateCollection = mongoDBClient['candidateCollection']
    result = candidateCollection.delete_one({"_id": ObjectId(id.id)})
    if result.deleted_count > 0:
        return {
                'message':'candidate deleted',
                'status_code':200}
    else:
        return {'message':'candidate not found',
                'status_code':200} 


# to delete candidate from mongo db by id
@tdr.post("/deleteCandidates",tags=["candiates"])
async def deleteCandidate(id:bulkIdSchema,Authorize: AuthJWT = Depends()):  
    # Authorize.jwt_required()
    for i in id.array:
        candidate=i.dict()
        result=candidateCollection.delete_one({"_id": ObjectId(candidate['id'])})
    if result.deleted_count > 0:
            return {
                'message':'candidate deleted',
                'status_code':200}
    return {"status_code":200,"message":"candidate  not found"}



# to update candidate in mongo db by id
@tdr.post("/updateCandidate",tags=["candiates"])
async def updateCandidate(updateCandidate:candidateUpdateSchema,Authorize: AuthJWT = Depends()):  
    result=candidateCollection.find_one({"_id": ObjectId(updateCandidate.id)})
    print(result)
    if result:
        candidateCollection.update_one({"_id": ObjectId(updateCandidate.id)}, {"$set": updateCandidate.dict()})
        return {"status_code":200,"message":"candidate updated"}
    

    raise HTTPException(status_code=404, detail='User not found')


    
    



# @tdr.post("/uploadCandidateFile")
# async def create_upload_file(batchId:str,file: Union[UploadFile, None] = None,Authorize: AuthJWT = Depends()):
#     # Authorize.jwt_required()
    
#     print("test")
#     if not file:
#         return {"message": "No upload file sent"}
#     else:
#         contents = file.file.read()
#         contents = BytesIO(contents)
#         df = pd.read_excel(contents)
#         df['batchId']=batchId
#         print(df)
#         mobile=df['mobile'].tolist()
#         for i in mobile:
#             if len(str(i)) < 10 or len(str(i)) > 12:
#                 return {"status_code":400,
#                         "message": "mobile number should be 10 digits",
#                         "details": i}        
            
#         uploaded=candidateCollection.insert_many(df.to_dict('records'))
#         if len(uploaded.inserted_ids)==0:
#             return {"status_code":400,
#                     "message": "file upload failed"}
#         print(uploaded.inserted_ids)
#         return {"status_code":200,
#                 "message": "file uploaded successfully"}    
    
    
                
                
# @tdr.post("/sendMailToCandidate")
# async def sendMailToCandidate(id: bulkIdSchema, Authorize: AuthJWT = Depends(),tenant:str=Depends(getTenantInfo),db: Session = Depends(get_db)):
#     # Authorize.jwt_required()
#     # try:
#         db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
#         selectedStudents=len(id.array)
#         credit=db.query(Uses).first().credits
#         print(credit)
        
    
#         if credit < selectedStudents:
#             leftCredits=selectedStudents - credit
#             print("Insufficait credits to send mail")
#             return {"status_code": 400,
#                     "message": "Insufficait credits to send mail"}
            
        
#         creditItem=db.query(Uses).first()
#         print(creditItem)
#         print(selectedStudents)
#         if creditItem:
#             creditItem.credits=credit-selectedStudents
#             db.commit()
#             print("credits updated")
#         already_sent_ids = []
#         for i in id.array:
#             examId = uuid.uuid4()
#             candidate = i.dict()
#             alreadyExist = mailedcandidateCollection.find_one({"studentId": candidate['id']})
#             EXISTS=[]
#             if alreadyExist:
#                 print("already exist")
#                 EXISTS.append(alreadyExist)
#                 continue
            
#             result = candidateCollection.find_one({"_id": ObjectId(candidate['id'])})
#             studentId = str(result['_id'])
#             already_sent = mailedcandidateCollection.find_one({"studentId": candidate['id']})
#             if already_sent:
#                 already_sent_ids.append(candidate['id'])
#                 continue
#             exist=candidateSignupCollection.find_one({"studentId":studentId})
#             if exist:
#                 try:
#                     pswd=exist['password']
#                 except:
#                     pswd="12345"
                
#             id.assessmentDetails = {"assessmentStatus": "Scheduled",
#                                     "workspaceId": id.workspaceId,
#                                     "examId": str(examId),
#                                     "assessmentId": id.assessmentId,
#                                     "email": result['email'],
#                                     "LinkSentDatetime": datetime.now(),
#                                     "name": result['name'],
#                                     'studentId':studentId,
#                                     "sortname":tenant['tenant']}
            
#             # updateCand=candidateCollection.update_one({"_id": ObjectId(candidate['id'])}, {"$set": {"assessmentStatus": "Scheduled"}})
#             # signUpData=candidateSignupCollection.insert_one(candidate)
        
#             linkText= str(id.workspaceId) + ":" + str(id.assessmentId) + ":" + str(examId) + ":" + str(studentId)+":"+str(tenant)
            
#             access_token =Authorize.create_access_token(subject=str(studentId), expires_time=360000,
#                     user_claims= {
#                         "workspaceId": id.workspaceId,
#                         "assessmentId": id.assessmentId,
#                         "examId": str(examId),
#                         "studentId": studentId,
#                         "tenant":tenant['tenant'],
#                         "email":result['email'],
#                         "isPasswordSet":True if exist and pswd else False,
                        
                        
#                     })
        
#             link = 'https://trovenfe.smartinternz.com/examportal?examid=' + access_token
#             db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
#             exam=db.query(assessmentModel).filter(assessmentModel.id == id.assessmentId).filter(assessmentModel.tenantWorkspaceId==id.workspaceId).first()
#             startDate=exam.examStartDate
#             endDate=exam.examEndDate
#             assessmentDetails ={"studentId":studentId,"assessmentStatus": "Scheduled","workspaceId": id.workspaceId,"examId": str(examId),"assessmentId": id.assessmentId,"LinkSentDatetime": datetime.now(),"sortname":tenant['tenant'],"examToken": access_token,"examStartTime": startDate,"examEndTime": endDate}
            
#             assessmentCollection=mongoDBClient['assessmentCollection']
#             assessmentCollection.insert_one(assessmentDetails)
            
            
                
#             mailedcandidateCollection.insert_one({
#                 "assessmentStatus": "Scheduled",
#                                     "workspaceId": id.workspaceId,
#                                     "examId": str(examId),
#                                     "assessmentId": id.assessmentId,
#                                     "email": result['email'],
#                                     "LinkSentDatetime": datetime.now(),
#                                     "name": result['name'],
#                                     'studentId':studentId,
#                                     "sortname":tenant['tenant']
   
#             })
#             if exist and pswd:
#                 print("password already set")
                
#             else:
#                 candidateSignupCollection.insert_one({
#                     "email": result['email'],
#                     "name": result['name'],
#                     'studentId':studentId,
#                     "isPasswordSet":False,
                    
#                 })
#             emailContent="Hi "+result['name']+",\n\n"+"Please click on the below link to start the assessment\n\n"+link+"\n\n" +"Regards,\n"+"Troven Team"

#             print("mail sent")
#             sendEmail(result['email'], emailContent)
            

#         return {
#                 "status_code": 200,
#                 "message": "mails sent successfully",
#                 "AssessmentLink": access_token  ,
#                 "remainingCredits":credit-selectedStudents,
#                 "already_sent_ids": EXISTS,
#             }
#     # except Exception as e:
#     #     return {"status_code": 400,
#     #             "message": "mails sent failed",}
            
           
# @adminApp.post("/initialize")
# async def initialize(passsword:PasswordSchema,Authorize: AuthJWT = Depends()):
#     # try:
#         claims = Authorize.get_raw_jwt()
#         print(claims)
#         workspaceId=claims['workspaceId']
#         assessmentId=claims['assessmentId']
#         passsword.studentId=claims['studentId']
#         examId=claims['examId']
#         email=claims['studentId']
#         # passsword.email=claims['email']
#         sortname=claims["tenant"]
#         isPasswordSet=claims['isPasswordSet']
#         assessmentCollection=mongoDBClient['assessmentCollection']
        
#         examCompleted=assessmentCollection.find_one({"studentId": passsword.studentId,"examId":examId})
#         if examCompleted['assessmentStatus']=="Completed":
#             return {"status_code": 400,
#                     "message": "You have already completed the assessment"}

        
#         if isPasswordSet==False:
#             passsword.password=hashlib.sha256(passsword.password.encode()).hexdigest()
#             existCand=candidateSignupCollection.find_one({"studentId": passsword.studentId})
#             print(existCand)
#             # if existCand['email']:
#             #     try:
#             #         existCand['password']==hashlib.sha256(passsword.password.encode()).hexdigest()
                    
#             #     except:
#             #         return {"status_code": 400,
#             #             "message": "You are not authorized to attend This Assessment Please use the correct password"}
#             #     # if passsword.password !=hashlib.sha256(existCand['password'].encode()).hexdigest():
#             #     #     return {"status_code": 400,
#             #     #         "message": "You are not authorized to attend This Assessment Please use the correct password"}
#             #     # return {"status_code": 400,
#             #     #         "message": "You are not authorized to attend This Assessment Please use the Same Email Id which you have used for Signup"}
             
                
#             access_token =Authorize.create_access_token(subject=str(passsword.studentId), expires_time=360000,
#                         user_claims= {
#                             "studentId" : passsword.studentId,
#                             "examId": examId,
#                             "assessmentId": assessmentId,
#                             "workspaceId": workspaceId,
#                             "sortname":sortname
                            
#                         })
       
#         # examDetails={"examId":examId,"workspaceId":workspaceId,"assessmentId":assessmentId,"sortname":sortname,"examStartedDatetime":datetime.now(),"examToken":access_token}
#         # passsword.assessmentDetails=[examDetails]
#             if existCand:
#                         check=candidateSignupCollection.update_one({"studentId": passsword.studentId}, {"$set": {"password": passsword.password,'isPasswordSet':True}})
#                         print(check.modified_count)
#                         if check.modified_count==1:
#                             print("password updated")
#                             assessmentCollection.update_one({"studentId": passsword.studentId,"examId":examId}, {"$set": {"examStartedAt": datetime.now(),"examToken":access_token,"assessmentStatus":"Started"}})
            

#                         return {"status_code": 200,
#                         "message": "student already added",
#                         "access_token":access_token}
#             else:
#                 return {"status_code": 400,
#                         "message": "No assessment scheduled for this student"}
                
#         access_token =Authorize.create_access_token(subject=str(passsword.studentId), expires_time=360000,
#                         user_claims= {
#                             "studentId" : passsword.studentId,
#                             "examId": examId,
#                             "assessmentId": assessmentId,
#                             "workspaceId": workspaceId,
#                             "sortname":sortname
                            
#                         })
#         return {"status_code": 200,
#                         "message": "student already added",
#                         "access_token":access_token}
#         # candidateSignupCollection.insert_one(passsword.dict())
#         # mailedcandidateCollection.update_one({"studentId": passsword.studentId}, {"$set": {"assessmentStatus": "Started","staredDatetime":datetime.now(),"sortname":sortname,"email":passsword.email,"examToken":access_token}})
#         # access_token =Authorize.create_access_token(subject=str(passsword.studentId), expires_time=360000,
#         #             user_claims= {
#         #                 "studentId" : passsword.studentId,
#         #                 "examId": examId,
#         #                 "assessmentId": assessmentId,
#         #                 "workspaceId": workspaceId,
#         #                 "sortname":sortname
#         #             })
#         # return {"status_code": 200,
#         #         "message": "student added successfully",
#         #         "access_token":access_token}
#     # except Exception as e:
#     #     return {"status_code": 400,
#     #             "message": "student not added",
#     #             "error": str(e)}
        
        
        
        
# # @tdr.post('validateCanduidate')     
# # async def validating(token:str,Authorize: AuthJWT = Depends()):
# #     if token:
# #         if token=='undefined':
# #             return {"status_code":400,
# #                     "message": "token not found"}
        
# #     # Authorize.jwt_required()
# #     if result:
# #         return {"status_code":200,
# #                 "message": "candidate found",
# #                 "data":result}
# #     return {"status_code":400,
# #             "message": "candidate not found"}
        

# @tdr.post("/submit-details") 
# async def submit_details(details: str, db: Session = Depends(get_db)):
#     try:
#         # Decrypt the link to obtain the tenant sort name and student ID
#         decrypted_link = decrypt(FERNET_KEY, details.initializeLink)
#         tenant_sortname, student_id = decrypted_link.split(':')
        
#         # Update the student record with the additional details
#         db.execute(text('SET search_path TO {}'.format(tenant_sortname))) 
#         # student = db.query(students).filter(students.id == student_id).first()
#         # student.additional_details = details.dict()
#         db.commit()
        
#         # Redirect the user to a success page
#         return RedirectResponse(url="/success")
#     except Exception as e:
#         return {"status_code": 400,
#                 "message": "Failed to submit details",
#                 "error": str(e)}
        
        
        
# @tdr.post("/allMailedCandidates")       
# async def candidate(cand:mailedCandidateSchema,  Authorize: AuthJWT = Depends(),tenant:str=Depends(getTenantInfo)):  
#     # Authorize.jwt_required()
#     sortname=tenant['tenant']
#     all_candidate=mailedcandidateCollection.find({"sortname":tenant['tenant']})
#     data=[]
#     for i in all_candidate:
#         if i['assessmentId']==cand.assessmentId and i['workspaceId']==cand.workspaceId:
#             data.append(i)
#     return {"status_code":200,"data":data}

    
