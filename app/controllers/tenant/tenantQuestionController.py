from app.routes import tenantDashboardRouter as tdr 
from fastapi import Depends

# from app.models.tenant.tenantModel import TenantUser
from app.libs.authJWT import *
from app.libs.mongoclient import mongoDBClient,question_collection,newQuestion_collection
from app.schemas.tenant.questionBankSchema import questionBankSchema,fetchQuestionSchema,idSchema
from app.schemas.tenant.tenantUserSchema import updateTenantUserSchema
from fastapi import Depends
from app.app import app 
import json
from bson import ObjectId
import pydantic
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str



# adding questions
@app.post('/postQuestionBank',tags=['tenantquestions'])
async def create_question(question: questionBankSchema, Authorize: AuthJWT = Depends()):
    # try:
        # Authoriza.jwt_required()
          currentUser = Authorize.get_jwt_subject()
          question.id=currentUser
          Dict=question.dict()
          workspaces_collection= mongoDBClient["WorkspaceCollection"]
          workspace = workspaces_collection.find_one({"_id": ObjectId(question.Workspaceid)})
          if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            }
          collection=mongoDBClient["adminAssessmentModel"]
          assesment = collection.find_one({"_id": ObjectId(question.assessmentid)})
          if not assesment:
           return{
            "status_code":400,
            "message":"assesment not found"
        }  
    
          sectionCollection=mongoDBClient["SectionCollection"]
          section=sectionCollection.find_one({"_id":ObjectId(question.sectionId)})
          if not section:
           return{
            "status_code":400,
            "message":"section not found"
        }
          existing=newQuestion_collection.find_one({"question": question.question})
          if existing:
            return {"status_code": 400, "message": "question already exists"}

@app.post('/getquestion',tags=['tenantquestions'])
async def get_question(getquestion:fetchQuestionSchema, Authorize: AuthJWT=Depends()):
    currentUser = Authorize.get_jwt_subject()
    Dict=getquestion.dict()
    Dict['userId']=currentUser
    workspaces_collection= mongoDBClient["WorkspaceCollection"]
    workspace = workspaces_collection.find_one({"_id": ObjectId(getquestion.Workspaceid)})
    if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            }
    collection=mongoDBClient["adminAssessmentModel"]
    assesment = collection.find_one({"_id": ObjectId(getquestion.assessmentid)}) 
    if not assesment:
        return{
            "status_code":400,
            "message":"assesment not found"
        } 
    sectionCollection=mongoDBClient["SectionCollection"]
    section=sectionCollection.find_one({"_id":ObjectId(getquestion.sectionId)})
    if not section:
        return{
            "status_code":400,
            "message":"section not found"
        }
    # getquestion.id=getId
    question=newQuestion_collection.find_one({"_id":ObjectId(getquestion.id)})
    print(question)
    if not question:
        return{
            "status_code":400,
            "message":"question not found"
        }
    else:
        question['_id']=str(question['_id'])
        return{
            "message":"found_assesment",
            "status_code":200,
            "res":question
        }   



@app.get('/getallquestions',tags=['tenantquestions'])
async def getallquestions( Authoriza: AuthJWT = Depends()):
        # Authoriza.jwt_required()
        currentuser=Authoriza.get_jwt_subject()
        
        all_questions=question_collection.find()
        data=[]
        for i in all_questions:
            i["_id"]=str(i['_id'])
            data.append(i)
        print(data) 
        return {"status_code":200,
                "data":data}  
@app.post("/updatequestion",tags=['tenantquestions'])
async def update_question(update_data: updateTenantUserSchema,Authorize: AuthJWT = Depends()):
    # try:
        currentUser=Authorize.get_raw_jwt()
        Dict=update_data.dict()
        Dict['userId']=currentUser
        workspaces_collection= mongoDBClient["WorkspaceCollection"]
        workspace = workspaces_collection.find_one({"_id": ObjectId(update_data.Workspaceid)})
        question_id = update_data.questionId
        new_question_text = update_data.newQuestionText
        if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            }
        collection=mongoDBClient["adminAssessmentModel"]
        assesment = collection.find_one({"_id": ObjectId(update_data.assessmentid)}) 
        if not assesment:
          return{
            "status_code":400,
            "message":"assesment not found"
        } 
        sectionCollection=mongoDBClient["SectionCollection"]
        section=sectionCollection.find_one({"_id":ObjectId(update_data.sectionId)})
        if not section:
          return{
            "status_code":400,
            "message":"section not found"
        }
    # if claims['type']=='classified':
    # questionDict=question.dict()
        newQuestion_collection.update_one({"_id":ObjectId(Dict['id'])},{"$set":Dict})
        return {"status_code":200,"message":"question updated successfully"}

@app.post("/deletequestion",tags=['tenantquestions'])
async def delete_question(id:idSchema, Authorize: AuthJWT=Depends()):
    currentUser=Authorize.get_raw_jwt()
    Dict=id.dict()
    Dict['userId']=currentUser
    workspaces_collection= mongoDBClient["WorkspaceCollection"]
    workspace = workspaces_collection.find_one({"_id": ObjectId(id.Workspaceid)})
    if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            }
    collection=mongoDBClient["adminAssessmentModel"]
    assesment = collection.find_one({"_id": ObjectId(id.assessmentid)}) 
    if not assesment:
        return{
            "status_code":400,
            "message":"assesment not found"
        } 
    sectionCollection=mongoDBClient["SectionCollection"]
    section=sectionCollection.find_one({"_id":ObjectId(id.sectionId)})
    if not section:
        return{
            "status_code":400,
            "message":"section not found"
        }
    delete=newQuestion_collection.delete_one({"_id":ObjectId(id.id)})
    return{
        "message":"question deleted",
        "staus_code":200
    }


