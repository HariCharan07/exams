
from fastapi import Depends
from app.libs.authJWT import *
from bson import ObjectId
from app.schemas.tenant.tenantWorkspaceSchema import tenantWorkspaceSchema,tenantWorkspaceIdSchema,tennatWorkspaceUpdateSchema
# from app.models.tenant.tenantModel import TenantWorkspace
# from app.models.tenant.tennatAssessmentModel import assessmentModel
from datetime import datetime, timedelta

from app.libs.mongoclient import mongoDBClient,workspaces_collection
from app.app import app 
@app.get("/listWorkspace",tags=['workspace'])
def get_created_workspaces(Authorize:AuthJWT=Depends()):
        
    # try:
        currentUser=Authorize.get_jwt_subject()
        # tenant_ws.id=currentUser
        workspaces_collection = mongoDBClient["WorkspaceCollection"]
        list_w = workspaces_collection.find().sort('_id', -1)
        print(list_w)
        workspace_list = []
        for list in list_w:
            list["_id"]=str(list['_id'])
            workspace_list.append(list)
        print(workspace_list)
        return {
            "status_code": 200,
            "data": workspace_list
        }
@app.post("/createWorkspace",tags=["workspace"])
def createWorkspace(tenantWs: tenantWorkspaceSchema, Authoriza: AuthJWT = Depends()):
    try:        
        currentUser = Authoriza.get_jwt_subject()
        tenantWs.id=currentUser
        # db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        # print(text('SET search_path TO {}'.format(tenant['tenant'])))
        workspaces_collection = mongoDBClient["WorkspaceCollection"]
        workspaceList = workspaces_collection.find_one({"name":tenantWs.name})
        if workspaceList:
            return {"status_code": 400,
                "message": "Workspace already exists"} 
        wsInsertData = tenantWs.dict()
        getId = "your_user_id"
        wsInsertData["created_by"] = getId
        workspaces_collection.insert_one(wsInsertData)
        return {"status_code":200,
            "message": "Workspace created successfully"}
    except Exception as e:
        return{"status_code":400,
               "message": "Something went wrong"}    

@app.post("/updateWorkspace",tags=['workspace'])
def updateWorspace(tenantupdate:tennatWorkspaceUpdateSchema, Authoriza: AuthJWT = Depends()):
    try:
        # Authoriza.jwt_required()
        currentUser = Authoriza.get_jwt_subject()
        workspaceDict=tenantupdate.dict()
        workspaceDict['Id']=currentUser
        # db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        query = {"id": tenantupdate.id}
        workspaces_collection=mongoDBClient["WorkspaceCollection"]
        workspacesList = workspaces_collection.find_one(query)
        if workspacesList is  None:
            return {"status_code": 404,
                "message": "Workspace not found"
                }
        else:
            updated_data = {k: v for k, v in tenantupdate.dict().items() if k != 'id'} 
            workspaces_collection.update_one(query,{"$set": updated_data})
        return {"status_code":200,
            "message": "Workspace updated successfully"}
    except Exception as e:
        return {"status_code":400,
            "message": str(e)
            }    


@app.post("/deleteWorkspace",tags=['workspace'])
def deleteWorkspace(tenantdelete:tenantWorkspaceIdSchema, Authoriza: AuthJWT = Depends()):
    try:
        # Authoriza.jwt_required()
        currentUser = Authoriza.get_jwt_subject()
        Dict=tenantdelete.dict()
        Dict['userId']=currentUser
        # db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        query = {"_id": tenantdelete.id}
        workspaces_collection=mongoDBClient["WorkspaceCollection"]
        workspace = workspaces_collection.find_one(query)
        
        if workspace is None:
            return {"status_code": 404,
                "message": "Workspace not found"}
        
        workspaces_collection.delete_one(query)
        return {
                "status_code": 200,
                "message": "Workspace deleted successfully"
            }
    except Exception as e:
        return {"status_code": 400,
            "message": str(e)
            }        
    

