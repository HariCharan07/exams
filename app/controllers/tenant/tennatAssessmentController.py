from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status

from typing import Union
from io import BytesIO
from app.libs.authJWT import *
from app.app import app 
from app.libs.mongoclient import mongoDBClient,collection
# from app.models.tenant.tenantModel import TenantWorkspace,TenantUser

from datetime import datetime, timedelta
from app.schemas.tenant.tenantAssessmentSchema import assessmentSchema,updateAssessmentSchema,idSchema,assessmentIdSchema
# from app.models.tenant.tennatAssessmentModel import assessmentModel
# from app.models.admin.adminWorkspaceAssessmentModel import adminAssessmentModel,adminWorkspace

import bson
from bson import ObjectId



# Close the MongoDB connection



@app.post("/createAssessment",tags=['tennantAssessment'])
def createAssessment(assessment:assessmentSchema, Authoriza: AuthJWT = Depends()):
    try:
        collection = mongoDBClient["collection"]
        currentUser = Authoriza.get_jwt_subject()
        Dict=assessment.dict()
        Dict['userId']=currentUser
        workspace = collection.find_one({"_id": ObjectId(assessment.WorkspaceId)})
        if workspace:
            return {"status_code": 400,
                "message": "assessment already exist"} 
        workspaces_collection= mongoDBClient["WorkspaceCollection"]
        workspace = workspaces_collection.find_one({"_id": ObjectId(assessment.WorkspaceId)})
        if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            } 
        assessment_data = assessment.dict()
        assessment_data["created_by"] = "user_id_here" 
        if assessment_data["sponserId"] == "":
            assessment_data["sponserId"] = None
        collection.insert_one(assessment_data)
          
        return {
            "status_code": 200,
            "message": "Assessment created successfully"
        }
    except Exception as e:
        return {
            "status_code": 400,
            "message": str(e)
        }
    
    
# to list all assessments
@app.post("/listAssessment",tags=['tennantAssessment'])
async def listAssessment( Authorize: AuthJWT = Depends()):
        currentUser=Authorize.get_raw_jwt
        collection = mongoDBClient["adminAssessmentModel"]
        # Authoriza.jwt_required()
        assessments = collection.find().sort("_id",-1)
        print(assessments)
        assessment_list=[]
        for list in assessments:
            list["_id"]=str(list["_id"])
            assessment_list.append(list)
        print(assessment_list)
        return {"status_code": 200,
                "data": assessment_list}
    
        
        

# get assessment by id
@app.post("/getAssessment",tags=['tennantAssessment'])
async def getAssessment(id: assessmentIdSchema, Authorize: AuthJWT = Depends()):
    # try:
        # Authoriza.jwt_required()
        currentUser=Authorize.get_jwt_subject
        Dict=id.dict()
        Dict['userId']=currentUser
        # db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        assessmentList = collection.find_one(
                                                    {'id':ObjectId(id.WorkspaceId)})
        print(assessmentList)
        if not assessmentList:
            return{
                "status_code":400,
                "message":"workspace not found"
            }
        collection = mongoDBClient["adminAssessmentModel"]
        assessment=collection.find_one({"_id":ObjectId(id.id)})
        if not assessment:
            return {
                "status_code": 400,
                "message": "Assessment not found"
            }
        else:
            assessment['_id']=str(assessmentList['_id'])
            return{
                "status_code":200,
                "message":"found data",
                "res":"assessment"
            }
            
            
            
        

        
# update assessment
@app.post("/updateAssessment",tags=['tennantAssessment'])
async def updateAssessment(assessment: updateAssessmentSchema, Authoriza: AuthJWT = Depends()):
    try:
    # Authoriza.jwt_required()
        currentUser  = Authoriza.get_jwt_subject()
        Dict=assessment.dict()
        Dict['userId']=currentUser
        workspaces_collection= mongoDBClient["WorkspaceCollection"]
        workspace = workspaces_collection.find_one({"_id": ObjectId(assessment.WorkspaceId)})
        # db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        if not workspace:
            return {"status_code": 400,
                "message": "workspace not found"
                }
        assessment_id = ObjectId(assessment.id)
        existing_assessment = collection.find_one({"_id": assessment_id})
        if not existing_assessment:
                return {"status_code": 400,
                        "message": "Assessment not found"}
        else:
            collection.update_one({"_id":ObjectId(assessment.id)}, {"$set":assessment.dict()})
        return {"status_code":200,
            "message": "Assessment updated successfully"}
    except Exception as e:
        return {"status_code": 400,
                "message": str(e)} 
    
    
#delete assessment
@app.post("/deleteAssessment",tags=['tennantAssessment'])
async def deleteAssessment(id: idSchema, Authoriza: AuthJWT = Depends()):
    try:
    # Authoriza.jwt_required()
        currentUser = Authoriza.get_jwt_subject()
        Dict=id.dict()
        Dict['userId']=currentUser
        # db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        workspaces_collection= mongoDBClient["WorkspaceCollection"]
        workspace = workspaces_collection.find_one({"_id": ObjectId(id.WorkspaceId)})
        if not workspace:
                return {
                    "status_code": 400,
                    "message": "Workspace not found"
                } 
        assessment_id = ObjectId(id.id)
        collection.delete_one({"_id": assessment_id})
        return {
            "status_code": 200,
                            "message": "Assessment  deleted"}
    except Exception as e:
        return {
            "status_code": 400,
            "message": "Assessment not found",
            "error": str(e)
       
        }
   
   
