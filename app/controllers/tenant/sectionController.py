from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
# from app.routes import tenantDashboardRouter as tdr,getTenantInfo
from fastapi import FastAPI
from app.libs.mongoclient import mongoDBClient,sectionCollection
import json
import bson.json_util
from app.libs.authJWT import *
from app.app import app 
from bson.objectid import ObjectId
import pydantic
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str
from app.schemas.tenant.sectionschema import sectionListSchema,updateSectionListSchema,idSchemas,idSchema
from datetime import datetime
# from app.models.tenant.tenantModel import Uses


# create candidate and store it to mongo db      
@app.post("/createSection",tags=['tenantSection'])
async def createsection(section:sectionListSchema,Authorize: AuthJWT = Depends()):  
    currentUser=Authorize.get_raw_jwt() 
    section.id=currentUser
    workspaces_collection= mongoDBClient["WorkspaceCollection"]
    workspace = workspaces_collection.find_one({"_id": ObjectId(section.WorkspaceId)})
    if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            }
    collection=mongoDBClient["adminAssessmentModel"]
    assesment = collection.find_one({"_id": ObjectId(section.assessmentId)}) 
    if not assesment:
        return{
            "status_code":400,
            "message":"assesment not found"
        } 
    # if claims['type']=='classified':
    existing_section = sectionCollection.find_one({"sectionDetails": section.sectionDetails})
    if existing_section:
            return {
                "status_code": 400,
                "message": "section already exists"
            }
    sectionDict=section.dict()
    sectionCollection.insert_one(sectionDict)
    return {"status_code": 200,
                "message": "section added successfully"}
    

    
@app.post("/getSection",tags=['tenantSection'])
async def getSection(id:idSchema,Authorize: AuthJWT = Depends()):  
    # Authorize.jwt_required()
   workspaces_collection= mongoDBClient["WorkspaceCollection"]
   workspace = workspaces_collection.find_one({"_id": ObjectId(id.WorkspaceId)})
   if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            }
   collection=mongoDBClient["adminAssessmentModel"]
   assesment = collection.find_one({"_id": ObjectId(id.assesmentId)}) 
   if not assesment:
        return{
            "status_code":400,
            "message":"assesment not found"
        } 
   Sections=sectionCollection.find_one({"_id":ObjectId(id.id)})
   print(Sections)
   if not Sections:
        return{
            "status_code":400,
            "message":"section not found"
        }
   else:
        Sections['_id']=str(Sections['_id'])
        return{
            "message":"found_assesment",
            "status_code":200,
            "res":Sections
        }
   
    


@app.post("/updateSection",tags=['tenantSection'])
async def updateSections(section:updateSectionListSchema,Authorize: AuthJWT = Depends()):  
    currentUser=Authorize.get_jwt_subject()
    Dict=section.dict()
    Dict['userId']=currentUser
    workspaces_collection= mongoDBClient["WorkspaceCollection"]
    workspace = workspaces_collection.find_one({"_id": ObjectId(section.WorkspaceId)})
    if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            }
    collection=mongoDBClient["adminAssessmentModel"]
    assesment = collection.find_one({"_id": ObjectId(section.assesmentId)}) 
    if not assesment:
        return{
            "status_code":400,
            "message":"assesment not found"
        } 
    # if claims['type']=='classified':
    sectionDict=section.dict()
    sectionCollection.update_one({"_id":ObjectId(section.id)},{"$set":sectionDict})
    return {"status_code":200,"message":"section updated successfully"}




@app.post("/getSections",tags=['tenantSection'])
async def getSections(Authorize: AuthJWT = Depends()):  
    # Authorize.jwt_required()
    allSections=sectionCollection.find().sort('_id, -1')
    print(allSections)
    data=[]
    for i in allSections:
        i["_id"]=str(i['_id'])
        data.append(i)
    print(data)
    return {
        "status_code":200,
        "data":data
        }






#to delete a candidate from mongo db by id
@app.post("/deleteSection",tags=['tenantSection'])
def deleteSection(id:idSchemas,Authorize: AuthJWT = Depends()):  
    # Authorize.jwt_required()


    # Authorize.jwt_required()
    currentUser=Authorize.get_jwt_subject()
    Dict=id.dict()
    Dict['userId']=currentUser
    # id.id=currentUser
    # if claims['type']=='classified':
    workspaces_collection= mongoDBClient["WorkspaceCollection"]
    workspace = workspaces_collection.find_one({"_id": ObjectId(id.WorkspaceId)})
    if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            }
    collection=mongoDBClient["adminAssessmentModel"]
    assesment = collection.find_one({"_id": ObjectId(id.assesmentId)}) 
    if not assesment:
        return{
            "status_code":400,
            "message":"assesment not found"
        } 
    result = sectionCollection.delete_one({"_id": ObjectId(id.id)})
    return {
            'message':'section  deleted',
            'status_code':200
            }
   