from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from typing import Union
from app.routes import tenantDashboardRouter as tdr
from io import BytesIO
from app.schemas.tenant.tenantSponserSchema import sponserSchema,sponserIdSchema,sponserUpdateSchema
import pandas as pd
from app.routes import getTenantInfo
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.libs.authJWT import *
from app.libs.psqlDBClient import get_db
from app.models.tenant.tenantModel import TenantWorkspace
from datetime import datetime, timedelta
from app.models.tenant.tenantModel import Sponser


#to create sponsers 
@tdr.post("/createSponser")
async def add_sponser(sponser: sponserSchema,db: Session = Depends(get_db), tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
    try:
        # Authoriza.jwt_required()
        getId = Authoriza.get_jwt_subject()
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))    
        sponserList = db.query(Sponser).filter(Sponser.name == sponser.name).first()  
        print(sponserList)  
        if sponserList:
              return {"status_code": 400,
                 "message": "Sponser already exists"} 
        sponserInsertData = Sponser(**sponser.dict())
        db.add(sponserInsertData)
        print(sponser)
        db.commit()
        return {"status_code":200,
             "message": "Sponser created successfully"}

    except Exception as e:
        return{"status_code":400,
               "error": str(e),
               "message": "Something went wrong"}  
    
    
# get all sponsers
@tdr.get("/listSponsers")
async def post_sponser(db: Session = Depends(get_db), tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
    try:
        # Authoriza.jwt_required()
        getId = Authoriza.get_jwt_subject()
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        sponserList = db.query(Sponser).order_by(Sponser.id).all()
        return {"status_code":200,
            "message": sponserList}
    except Exception as e:
        return{"status_code":400,
               "message": "Something went wrong"}
        
# update sponser
@tdr.post("/updateSponser")
async def update_sponser(sponser: sponserSchema, db: Session = Depends(get_db), tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
    try:
        # Authoriza.jwt_required()
        getId = Authoriza.get_jwt_subject()
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        sponserList = db.query(Sponser).filter(Sponser.id==sponser.id).first()
        if sponserList == None:
            return {"status_code": 404,
                "message": "Sponser not found"}
        elif sponserList.name == sponser.name:
            sponserList = db.query(Sponser).filter(Sponser.name==sponser.name).filter(Sponser.id!=sponser.id).first()
            if sponserList:
                return {"status_code": 400,
                    "message": "Sponser already exists"}
            else:
                db.query(Sponser).filter(Sponser.id==sponser.id).update(sponser.dict())
                db.commit()
        else:
            db.query(Sponser).filter(Sponser.id==sponser.id).update(sponser.dict())
            db.commit()
        return {"status_code":200,
            "message": "Sponser updated successfully"}
    except Exception as e:
        return{"status_code":500,
               "message": "Something went wrong"}
        
        
# delete sponser
@tdr.post("/deleteSponser")
async def delete_sponser(id:sponserIdSchema, db: Session = Depends(get_db),tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
    try:
        # Authoriza.jwt_required()
        getId = Authoriza.get_jwt_subject()
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        sponserList = db.query(Sponser).filter(Sponser.id==id.id).first()
        if sponserList == None:
            return {"status_code": 400,
                "message": "Sponser not found"}
        else:
            db.query(Sponser).filter(Sponser.id==id.id).delete()
            db.commit()
        return {"status_code":200,
            "message": "Sponser deleted successfully"} 
    except Exception as e:
        return{"status_code":400,
               "message": "Something went wrong"}
        
# get sponser by id
@tdr.post("/getSponserById")
async def getSponserByid(id:sponserIdSchema, db: Session = Depends(get_db), tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
    try:
        # Authoriza.jwt_required()
        getId = Authoriza.get_jwt_subject()
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        sponserList = db.query(Sponser).filter(Sponser.id==id.id).first()
        if sponserList == None:
            return {"status_code": 400,
                "message": "Sponser not found"}
        else:
            return {"status_code":200,
                "message": sponserList}
    except Exception as e:
        return{"status_code":400,
               "message": "Something went wrong"}
        
        
        
        
        
                        