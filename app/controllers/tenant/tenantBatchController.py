from app.routes import tenantDashboardRouter as tdr
from app.schemas.tenant.batchSchema import batchSchema,batchIdSchema,batchUpdateSchema
from fastapi import Depends, FastAPI, HTTPException, status
from app.libs.mongoclient import batch_collection,mongoDBClient
from bson.objectid import ObjectId
from app.routes import getTenantInfo
from app.app import app 

@app.post("/createBatch",tags=['tenantBatch'])
def create_batch(batch:batchSchema, tenant: str = Depends(getTenantInfo)):
    batch.sortname=tenant['tenant']
    batch_item=batch.dict()
    batch_collection = mongoDBClient['batch']
    if batch_collection.find_one({"name": batch.name}) is not None:
        
        return {"status_code":400,
                "message": "batch already exists"}
    batch = batch_collection.insert_one(batch_item)   
    insertedId = batch.inserted_id     
    return {"status_code":200,
            "data":insertedId,
        "message": "batch created successfully"}


@app.get("/listBatch",tags=['tenantBatch'])
async def list_batches(tenant: str = Depends(getTenantInfo)): 
    batch_data = list(batch_collection.find({"sortname": tenant['tenant']}))
    return {"status_code":200,
            "data":batch_data}   



@app.post("/updateBatch/",tags=['tenantBatch'])
async def update_batch(batch:batchUpdateSchema,tenant: str = Depends(getTenantInfo)):
    try:
            existing_batch = batch_collection.find_one({"id": batch.id})
            if existing_batch is None:
                return {"status_code":400,
                        "message": "batch not found"}
            if existing_batch['sortname'] == tenant['tenant']:
                print(existing_batch)
                if existing_batch is None:
                    return {"message": "batch not found"}
                updated_batch = batch.dict()
                batch_collection.update_one({"id": batch.id}, {"$set": updated_batch})
                return {"status_code":200,
                        "message": "batch updated"}
                
            return {"status_code":400,
                    "message": "Please Relogin to perform this action"}
        
    except Exception as e:
        return {"status_code":400,
                "message": "batch not updated",
                "error": str(e)}    


@app.post("/getBatch/",tags=['tenantBatch'])
async def update_batch(batch:batchIdSchema,tenant: str = Depends(getTenantInfo)):
    existing_batch = batch_collection.find_one({"_id": ObjectId(batch.id)})
    if existing_batch.sortname == tenant['tenant']:
        print(existing_batch)
        if existing_batch is None:
            return {"message": "batch not found"}
        return {
            "status_code":200,
            "message": existing_batch
        }
    return {"status_code":400,
            "message": "Please Relogin to perform this action"}



@app .post("/deleteBatch",tags=['tenantBatch'])
def delete_batch(id:batchIdSchema):  
    batch_collection = mongoDBClient['batch_collection']
    result = batch_collection.delete_one({"_id": ObjectId(id.id)})
    if result.deleted_count > 0:
        return {
                'message':'batch deleted',
                'status_code':200}
    else:
        return {'message':'batch not found',
                'status_code':200}   