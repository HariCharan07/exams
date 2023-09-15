from app.routes import tenantDashboardRouter as tdr
from  app.app import adminApp
from fastapi import Depends
from app.libs.mongoCLient import mongoDBClient
from app.routes import get_db,getTenantInfo
from app.models.tenant.tenantModel import TenantUser
from app.libs.authJWT import *
from sqlalchemy.orm import Session
from app.schemas.tenant.questionBankSchema import questionBankSchema,newQuestionSchema,questionIdSchema,UploadBulk,idSchema,newQuestionUpdateSchemaUpdate
from app.libs.mongoCLient import question_collection,newQuestion_collection
from app.utills.helper import serializeList,serializeDict
from fastapi import UploadFile, File
import shutil
from app.libs.mongoCLient import newQuestion_collection,question_collection
from app.libs.authJWT import *
from fastapi import Depends
from app.routes import get_db,getTenantInfo
from sqlalchemy import text
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from typing import Union
from app.routes import tenantDashboardRouter as tdr
from io import BytesIO
from app.schemas.tenant.tenantSkillSchema import SkillSchema,SkillIdSchema,SkillUpdateSchema
import pandas as pd
from app.routes import getTenantInfo
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.libs.authJWT import *
from app.libs.psqlDBClient import get_db
from app.models.tenant.tenantModel import TenantWorkspace
from datetime import datetime, timedelta
from app.models.tenant.tenantModel import Skills
from app.models.tenant.tennatAssessmentModel import assessmentModel
import subprocess
from app.schemas.globalSchemas import codeExecutioSchema



# adding questions
# @tdr.post('/postQuestionBank',tags=["Tenant Question Bank"])
# async def create_question(question: questionBankSchema,db: Session = Depends(get_db), tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
#     # Authoriza.jwt_required()
#     getId = Authoriza.get_jwt_subject()
#     question_item=question.dict()
#     print(getId)
#     db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
#     sortname=db.query(TenantUser).filter(TenantUser.id==getId).first().sortname
#     question_item["tenant_id"]=getId
#     question_item["tenant_sortname"]=sortname
#     question_collection.insert_one(question_item)
#     return {"status_code":200,
#             "message":"question added"
#             }



# #get all questions by Worksapce id
# @tdr.post('/questionBankList',tags=["Tenant Question Bank"])
# async def get_question(workspace_id:idSchema,db: Session = Depends(get_db), tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
#     Authoriza.jwt_required()
#     getId = Authoriza.get_jwt_subject()
#     db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
#     sortname=db.query(TenantUser).filter(TenantUser.id==(getId)).first().sortname
#     all_questions=serializeList(question_collection.find())
#     data = []
#     if int(workspace_id.id) == 0:
#         for i in all_questions:
#             if i["tenant_sortname"] == sortname:
#                 data.append(i)
                
#     else:
#         for i in all_questions:
#             if int(workspace_id.assessment_id) == 0:
#                 if i["tenant_sortname"] == sortname and i["workspace_id"] == int(workspace_id.id):
#                     data.append(i)
#             else:
#                     if i["assessment_id"] == int(workspace_id.assessment_id) and (i["tenant_sortname"] == sortname and i["workspace_id"] == int(workspace_id.id)):
#                         data.append(i)            
                        
#     return {"status_code":200,
#             "data":data
#             }                  
    
    


# #questionList By Assessment id
# @tdr.post('/questionBankListByAssessmentId',tags=["Tenant Question Bank"])
# async def Question_bank_list_by_assessmentId(assessment_id:idSchema,db: Session = Depends(get_db), tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
#     Authoriza.jwt_required()
#     getId=Authoriza.get_jwt_subject()
#     all_questions=serializeList(question_collection.find())
#     data=[]
#     for i in all_questions:
#         if i["assessment_id"]== int(assessment_id.id):
#             data.append(i)
#     return {"status_code":200,
#             "data":data}    



# @tdr.get('/questionBankListByTenantId',tags=["Tenant Question Bank"])
# async def Question_bank_list_by_assessmentId(db: Session = Depends(get_db), tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
#     Authoriza.jwt_required()
#     getId=Authoriza.get_jwt_subject()
#     db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))    
#     sortname=db.query(TenantUser).filter(TenantUser.id==getId).first().sortname
#     all_questions=serializeList(question_collection.find())
#     data=[]
#     for i in all_questions:
#         if i["assessment_id"]== getId:
#             data.append(i)
#     return {"status_code":200,
#             "data":data}   



# clone all questions by assessmentid and workspaceid
# @tdr.post('/cloneQuestionBank',tags=["Tenant Question Bank"])
# async def cloneQuestions(workspace_id:idSchema,db: Session = Depends(get_db), tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
#     Authoriza.jwt_required()
#     getId = Authoriza.get_jwt_subject()
#     db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
#     sortname=db.query(TenantUser).filter(TenantUser.id==getId).first().sortname
#     all_questions=serializeList(question_collection.find())
#     data = []
#     for i in all_questions:
#         if i["assessment_id"] == int(workspace_id.assessment_id) and (i["tenant_sortname"] == sortname and i["workspace_id"] == int(workspace_id.id)):
#             data.append(i)
#     for i in data:
#         i.pop('_id')
#         question_collection.insert_one(i)
#     return {"status_code":200,
#             "message":"question added"
#             }






# NEW QUESTION BANK CONTROLLER


@tdr.post('/newQuestionBank')
async def create_question(question: newQuestionSchema,db: Session = Depends(get_db), tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
    # Authoriza.jwt_required()
    getId = Authoriza.get_jwt_subject()
    print(getId)
    question.tenant_id=getId
    db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
    question_item=question.dict()
    sortname=db.query(TenantUser).filter(TenantUser.id==getId).first().sortname
    question_item["tenant_sortname"]=tenant['tenant']
    print(sortname)
    newQuestion_collection.insert_one(question_item)
    return {"status_code":200,"message":"question added"}






#clone all questions by assessmentid and workspaceid
@tdr.post('/cloneQuestionBank',tags=["Tenant Question Bank"])
async def cloneQuestions(id:idSchema,db: Session = Depends(get_db), tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
    # Authoriza.jwt_required()
    # getId = Authoriza.get_jwt_subject()
    db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
    # sortname=db.query(TenantUser).filter(TenantUser.id==getId).first().sortname
    all_questions=serializeList(newQuestion_collection.find())
    print(all_questions)
    for i in all_questions:
        # print(i["assessment_id"],int(id.assessment_id),i["workspace_id"],int(id.id))
        if int(i["assessment_id"]) == int(id.assessment_id) and int(i["workspace_id"]) == int(id.id):
            i.pop('_id')     
            i.pop('assessment_id')  
            i['assessment_id'] = int(id.new_assessment_id)
            newQuestion_collection.insert_one(i)
            
    return {"status_code":200,
                    "message":"question added"}
   
    # return {"status_code":200,
    #         "data":"questions cloned successfully"}


@tdr.post('/newQuestionBankBulk',tags=["Tenant Question Bank"])
async def create_question_in_bulk(question: UploadBulk):
    for i in question.arry:
        question_item=i.dict()
        newQuestion_collection.insert_one(dict(question_item))
    return {"status_code":200,"message":"question added" }


#get all questions
@tdr.post('/newQuestionBankList')
async def get_question(workspace_id:idSchema,db: Session = Depends(get_db), tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
    # Authoriza.jwt_required()
    getId = Authoriza.get_jwt_subject()
    db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
    assessmentDuration=db.query(assessmentModel).filter(assessmentModel.id==workspace_id.assessment_id).filter(assessmentModel.tenantWorkspaceId==workspace_id.id).first().duration
    sortname=db.query(TenantUser).filter(TenantUser.id==(getId)).first().sortname
    query = {"tenant_sortname":sortname,"workspace_id":(workspace_id.id),"assessment_id":int(workspace_id.assessment_id)}
    all_questions=newQuestion_collection.find(query)
    data = []
    for i in all_questions:
        for j in i:
            i['numberOfOptions'] = str(i['numberOfOptions'])
        # for key,value in i:
        #     import math
        #     if isinstance(value, float) and math.isnan(value):
        #         i[value] = None
        data.append(i)
        # print(i)
    
    # for i in all_questions:
    #     i.pop('_id')
    #     data.append(i)
    # print(all_questions,"all_questions")
    # return all_questions
    # data = []
    # if int(workspace_id.id) == 0:
    #     for i in all_questions:
    #         if i["tenant_sortname"] == sortname:
    #             data.append(i)
                
    # else:
    #     for i in all_questions:
    #         if int(workspace_id.assessment_id) == 0:
    #             if str(i["tenant_sortname"]) == str(sortname) and int(i["workspace_id"]) == int(workspace_id.id):
    #                 data.append(i)
    #         else:   
    #                 print("final loop")
    #                 print(i['assessment_id'],workspace_id.assessment_id,i['workspace_id'],workspace_id.id)
    #                 print(type(i['assessment_id']),type(workspace_id.assessment_id),type(i['workspace_id']),type(workspace_id.id))
    #                 if (i["assessment_id"]) == int(workspace_id.assessment_id) and ((i["tenant_sortname"]) == sortname and (i["workspace_id"]) == (workspace_id.id)):
    #                     data.append(i) 
    #                     print("test")
                           
                        
    return {"status_code":200,
            "data":data,
            "duration":assessmentDuration,
            }                  
    



@tdr.get('/newquestionBankListByAssessmentId')
async def get_question_by_assessment_id(assessment_id:idSchema):
    return {"status_code":200,"data":serializeList(newQuestion_collection.find({"assessment_id":assessment_id}))}





# delete question by id
@tdr.post('/deleteQuestionById')
async def delete_question_by_id(id:questionIdSchema):
    deleting=newQuestion_collection.delete_one({"id":id.id})
    if deleting:
        print('deleted')
        return {"status_code":200,"message":"question deleted"}
    return {"status_code":400,"message":"question not found"} 
    
    


 
#update question by id
@tdr.post('/updateQuestionById')
async def update_question_by_id(question: newQuestionSchema):
    try:
        questionData=question.dict()
        print(questionData)
        questionData = {k: v for k, v in questionData.items() if v is not None}
        result = newQuestion_collection.update_one({"id":question.id}, {"$set": questionData })
        if result:
            print('updated')
            return {"status_code":200,
                    "message":"question updated"
                    }
        
        return {"status_code":400,
                "message":"question not found"
                }
    except Exception as e:
        return {"status_code":400,
                "message":"question not found"
                }


#upload a video file
# @tdr.post('/uploadVideo')
# async def upload_video(video:UploadFile = File(...)):
#     with open(f'./{video.filename}', 'wb') as buffer:
#         shutil.copyfileobj(video.file, buffer)
#         uploadvideo.insert_one({"video":video.filename})
#         return {"status_code":200,"message":"video uploaded"}




def codeAsses(cas):
    cmd = ["docker", "run", "-i", "python:3.8", "python", "-c", cas.code]
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = popen.communicate()
    return {
        "output": stdout.decode("utf-8"),
        "error": stderr.decode("utf-8")
        }
    
    
    
    
    



@adminApp.post("/codeAssessment")
async def codeAssessment(cas: codeExecutioSchema):
    result=codeAsses(cas)
    return {"status_code":200,"message":"code executed","result":result['output'],"error":result['error']}
#     cmd = ["docker", "run", "-i", "python:3.8", "python", "-c", cas.code]
#     popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout, stderr = popen.communicate()
#     return {
#         "output": stdout.decode("utf-8"),
#         "error": stderr.decode("utf-8")
#         }
    
    

    
    
    