from app.routes import tenantDashboardRouter as tdr
from app.models.tenant.tenantModel import  TenantUser
from app.libs.psqlDBClient import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.schemas.tenant.tenantUserSchema import tenantUserSchema,tenantStrSchema,TenantLoginSchema,changePasswordSchema,changeProfileIamgeSchema,updateTenantUserSchema,userIdSchema,tenantUserMeSchema
import hashlib
from app.libs.awsMods import sendEmail
from app.libs.smsClient import sendsms
from app.utills.helper import generate_aplhanum_random
import os
from app.utills.helper import *
from app.routes import getTenantInfo
from app.libs.authJWT import AuthJWT
from sqlalchemy import text
from app.libs.redisClient import redisAdd
from datetime import datetime
from app.settings import FERNET_KEY





@tdr.post("/createUser")
async def createTenantUser(user: tenantUserSchema,  tenant: str = Depends(getTenantInfo), db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    try:
        getId = Authorize.get_jwt_subject()
        exactPassword=user.password
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        userData = db.query(TenantUser).filter(TenantUser.email == user.email).first()
        tenantEmail=db.query(TenantUser).filter(TenantUser.id == 1).first().email
        tenantDomain = tenantEmail.split('@')[1]
        userDmain = user.email.split('@')[1]
        
        if tenantDomain != userDmain:
            return {
                "status_code":400,
                "data": "Invalid email domain"
                    }
        if userData:
            return {
                "status_code":400,
                "data": "Email already exists"
                }
        if len(user.mobile)  < 10 or len(user.mobile) > 12:
            return {
                "status_code":400,
                "data": "Invalid mobile number"
                }
        getMobile=db.query(TenantUser).filter(TenantUser.mobile == user.mobile).first()
        if getMobile:
            return {
                "status_code":400,
                "data": "Mobile number already exists"
                }   
        userModel = user.dict()
        if userModel['password'] == None:
            userModel['password'] = hashlib.sha256(generate_aplhanum_random(8).encode()).hexdigest()
            userModel['sortname'] = tenant['tenant']
            userModel['company'] = tenant['tenant']
            
        else:
            password = userModel['password'] 
            userModel['password'] = hashlib.sha256(userModel['password'].encode()).hexdigest()
            userModel['sortname'] = tenant['tenant']
            userModel['company'] = tenant['tenant']
            

        userInsertData = TenantUser(**userModel)
        sendsms(userInsertData.mobile,"Your account has been created successfully. Your login credentials are: Email: "+userInsertData.email+" Password: "+exactPassword)
        
        sendEmail(userInsertData.email,"Your account has been created successfully. Your login credentials are: Email: "+userInsertData.email+" Password: "+exactPassword)
        

        db.add(userInsertData)
        db.commit()
        print('test')
        return {
            "user_id": userInsertData.id,
                "status_code":200,
                "data": "tenant user created successfully"
                }

    except Exception as e:
        return {"status_code":400, "data": str(e)}   
        
#list tenant users
@tdr.get("/listTenantUsers")
async def listtenantusers(tenant: str = Depends(getTenantInfo), db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    try:
        # Authorize.jwt_required()
        getId=Authorize.get_jwt_subject()
        print('SET search_path TO {}'.format(tenant['tenant']))
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        tenantUsers = db.query(TenantUser).filter(TenantUser.status!="deleted").all()
        return {"status_code":200, "data": tenantUsers}
    except Exception as e:
        return {"status_code":400, "data": str(e)}
    


@tdr.post("/updateUser")
def updateProfile(user: updateTenantUserSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends(),tenant: str = Depends(getTenantInfo)):
    try:
        claims = Authorize.get_raw_jwt()
        userId = Authorize.get_jwt_subject()
        password=user.password
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        tennatuser = db.query(TenantUser).filter(TenantUser.email==user.email).first()
        isMobile=db.query(TenantUser).filter(TenantUser.email!=user.email).first()
        if len(user.mobile)  < 10 or len(user.mobile) > 12:
            return {
                "status_code":400,
                "data": "Invalid mobile number"
                }
         
        if tennatuser:
            if user.mobile and isMobile.mobile == user.mobile:  
                
                return {"status_code":400,
                            "data": "Mobile number already exists"}
            tennatuser.mobile = user.mobile
            tennatuser.name = user.name
            tennatuser.status = user.status
            tennatuser.role = user.role
            tennatuser.sortname = tenant['tenant']
            if password:
                sendEmail(tennatuser.email,"Your account has been created successfully. Your login credentials are: Email: "+tennatuser.email+" Password: "+password)
            sendEmail(tennatuser.email,"Your account has been updated successfully.")

            db.commit()
            

            return {"status_code":200,
                        "Data with Userid": tennatuser.id,
                        "detail": "Tenant updated successfully"}
        else:
            return {"status_code":400,
                    "message": "tenant not found"}
    except Exception as e:
        return {"status_code":400,
                "data": str(e)}        
            


    
#  #update tenant user
# @tdr.post("/updateUser")
# async def updateTenantUser(user: updateTenantUserSchema, tenant: str = Depends(getTenantInfo), db: Session = Depends(get_db), Authoriza: AuthJWT = Depends()): 
#     try:
#         # Authoriza.jwt_required()
#         tenantuser=user.dict()
#         getid = Authoriza.get_jwt_subject()
#         db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
#         tennatuser = db.query(TenantUser).filter(TenantUser.email==user.email).first()
#         isMobile=db.query(TenantUser).filter(TenantUser.email!=user.email).first()
#         if len(user.mobile)  < 10 or len(user.mobile) > 12:
#             return {
#                 "status_code":400,
#                 "data": "Invalid mobile number"
#                 }
         
#         if tennatuser:
#             if user.mobile and isMobile.mobile == user.mobile:  
                
#                 return {"status_code":400,
#                             "data": "Mobile number already exists"}
#             tennatuser.mobile = user.mobile
#             tennatuser.name = user.name
#             tennatuser.status = user.status
#             tennatuser.role = user.role
#             tennatuser.sortname = tenant['tenant']
#             db.commit()
#             return {"status":200,
#                         "Data with Userid": tennatuser.id,
#                         "detail": "Tenant updated successfully"}
#         else:
#             return {"status_code":400,
#                     "message": "tenant not found"}
#     except Exception as e:
#         return {"status_code":400,
#                 "data": str(e)}        
            
    

@tdr.post("/changeProfilePic")
def changeProfilePic(filePath: tenantStrSchema,db: Session = Depends(get_db), Authorize: AuthJWT = Depends(),tenant: str = Depends(getTenantInfo)):
    try:
        # claims = Authorize.get_raw_jwt()
        userId = Authorize.get_jwt_subject()
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        getUser = db.query(TenantUser).filter(TenantUser.id == userId).first()
        if getUser and getUser.status == 'active':
            getUser.profilePic = filePath.str
            db.commit()
            # record_task_creation({"userId":userId,"task":"profile pic changed","taskTime":datetime.now(),"ip":claims['ip']})
            return {
                "status_code" : 200,
                "message" : "profile pic changed successfully",
                "details" : {
                    "id" : getUser.id
                }
            }
        else:
            return {
                "status_code" : 404,
                "message" : "admin user not found",
                "details" : {
                    "id" : None
                }
            }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized") 



# get tennat user by id
@tdr.post("/getUser/") 
async def getTenantUser(id: userIdSchema, tenant: str = Depends(getTenantInfo), db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    try:
        # Authorize.jwt_required()
        getid = Authorize.get_jwt_subject()
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        tenantUser = db.query(TenantUser).filter(TenantUser.id == id.id).first()
        return {"status_code":200, "data": tenantUser}
    except Exception as e:
        return {"status_code":400, "data": str(e)}


# # delete tenant user
@tdr.post("/deleteUser")
async def deleteTenantUser(user: userIdSchema, tenant: str = Depends(getTenantInfo), db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    try:
        # Authorize.jwt_required()
        get_id = Authorize.get_jwt_subject()
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        user=db.query(TenantUser).filter(TenantUser.id == user.id).first()
        if user:
            db.delete(user)
            db.commit()
            return {
                    "status_code":200, 
                    "data": "tenant user deleted successfully"
                    }
        
        if user:
            db.commit()
            return {"status_code":200, "data": "tenant user deleted successfully"}
        return {"status_code":400, "data": "tenant user not found"}
    except Exception as e:
        return {"status_code":400, "data": str(e)}




