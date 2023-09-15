from app.routes import tenantDashboardRouter as tdr
from app.models.tenant.tenantModel import  TenantUser
from app.libs.psqlDBClient import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.libs.authJWT import AuthJWT
from app.libs.redisClient import redisAdd
from app.schemas.tenant.tenantUserSchema import tenantUserMeSchema,tenantMeUpdateSchema,changePasswordSchema,tenantUserChangePasswordSchema,changeProfileIamgeSchema
from app.models.tenant.tenantModel import  TenantUser
from app.routes import getTenantInfo
from sqlalchemy import text
from app.libs.awsMods import generate_upload_url
from app.schemas.admin.adminUserSchema import filenameSchema
import hashlib
from app.libs.awsMods import sendEmail
import datetime
from pyotp import random_base32, TOTP
from app.confy.labels import TOTP_ISSUER_NAME
from app.schemas.globalSchemas import userStatusEnum
from app.models.admin.paymentAdminModel import paymentPlans
from app.schemas.admin.adminPaymentsPlanSchema import paymentPlansSchema
import json
from app.models.tenant.tenantModel import Uses


@tdr.post("/logout")
def logout(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    try:
        access_token = {}
        access_token['token'] = Authorize.get_raw_jwt()['jti']
        print(access_token, "access_token")
        redisAdd(access_token)
        return {
            "status_code" : 200,
            "message" : "logged out successfully"
        }
    except Exception as e:
        return {
            "status_code" : 500,
            "message" : "Internal Server Error",
            "details" : {
                "error" : str(e)
            }
        }

@tdr.post("/me")
async def getTenantUser( tenant: str = Depends(getTenantInfo), db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    # try: 
        try:
            getId = Authorize.get_jwt_subject()
            db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
            getUser = db.query(TenantUser).filter(TenantUser.id == getId).first()
            # db.execute(text('SET search_path TO public'))
            # plan = db.query(paymentPlans).filter(paymentPlans.id == getUser.subscriptionId).first()
            plan = db.query(Uses).filter(Uses.id == getUser.subscriptionId).first()
            moduleName=plan.name
            credits=plan.credits
            duration=plan.duration
            planDetails = {"moduleName":moduleName,"credits":credits,"duartion":duration}
            print(planDetails)

            if getUser and plan:  
                print(plan)
                getUser = tenantUserMeSchema(**getUser.__dict__)
                userDetails = getUser.dict()
                userDetails['planModules']=[planDetails]
                
                
                return {
                    "status_code" : 200,
                    "message" : "admin user details",
                    "details" : {
                        "user" : userDetails,

                    }
                }
                
            if plan == None:
                return {"status_code" : 404,
                        "message" : "No plans Found",}
        except Exception as e:
            getId = Authorize.get_jwt_subject()
            db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
            getUser = db.query(TenantUser).filter(TenantUser.id == getId).first()
            # db.execute(text('SET search_path TO public'))
            # plan = db.query(paymentPlans).filter(paymentPlans.id == getUser.subscriptionId).first()
            plan = db.query(Uses).filter(Uses.id == getUser.subscriptionId).first()
            moduleName=plan.name
            credits=plan.credits
            duration=plan.duration
            planDetails = {"moduleName":moduleName,"credits":credits,"duartion":duration}
            print(planDetails)

            if getUser and plan:  
                print(plan)
                getUser = tenantUserMeSchema(**getUser.__dict__)
                userDetails = getUser.dict()
                userDetails['planModules']=[planDetails]
                
                
                return {
                    "status_code" : 200,
                    "message" : "admin user details",
                    "details" : {
                        "user" : userDetails,

                    }
                }
                
            if plan == None:
                return {"status_code" : 404,
                        "message" : "No plans Found",}

    # except Exception as e:
    #     raise HTTPException(status_code=401, detail="Unauthorized")
    
    


@tdr.post("/enableMfa")
def enableMfa(db: Session = Depends(get_db), Authorize: AuthJWT = Depends(),tenant: str = Depends(getTenantInfo)):
    try:
        claims = Authorize.get_raw_jwt()
        userId = Authorize.get_jwt_subject()
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        getUser = db.query(TenantUser).filter(TenantUser.id == userId).first()
        if getUser and getUser.status == 'active':
            getUser.mfa = True
            getUser.mfaSecretCode = random_base32()
            db.commit()
            uri = TOTP(getUser.mfaSecretCode).provisioning_uri(name=getUser.email, issuer_name=TOTP_ISSUER_NAME)
            # qrcode.make(uri).save("/mfa.png")
            # record_user_creation({"userId":userId,"task":"mfa enabled","taskTime":datetime.now(),"userType":"classified"})
            return {
                "status_code" : 200,
                "message" : "mfa enabled successfully",
                "details" : {
                    "mfaUri" : uri
                }
            }
        else:
            return {
                "status_code" : 404,
                "message" : "admin user not found",
                "details" : {
                    "mfaSecret" : None
                }
            }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@tdr.post("/disableMfa")
def disableMfa(db: Session = Depends(get_db), Authorize: AuthJWT = Depends(),tenant: str = Depends(getTenantInfo)):
    try:
        claims = Authorize.get_raw_jwt()
        userId = Authorize.get_jwt_subject()
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        getUser = db.query(TenantUser).filter(TenantUser.id == userId).first()
        if getUser and getUser.status == 'active':
            getUser.mfa = False
            getUser.mfaSecretCode = None
            db.commit()
            # record_user_creation({"userId":userId,"task":"mfa disabled","taskTime":datetime.now(),"userType":"classified"})
            return {
                "status_code" : 200,
                "message" : "mfa disabled successfully",
                "details" : {
                    "mfaSecret" : None
                }
            }
        else:
            return {
                "status_code" : 404,
                "message" : "admin user not found",
                "details" : {
                    "mfaSecret" : None
                }
            }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")
    


    

@tdr.post("/changeProfilePic")
def changeProfilePic(filePath: filenameSchema,db: Session = Depends(get_db), Authorize: AuthJWT = Depends(),tenant: str = Depends(getTenantInfo)):
    try:
        claims = Authorize.get_raw_jwt()
        userId = Authorize.get_jwt_subject()
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        getUser = db.query(TenantUser).filter(TenantUser.id == userId).filter(TenantUser.status!="deleted").first()
        if getUser:
            getUser.profilePic = filePath.filename
            db.commit()
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
    
    
    
@tdr.post("/updateProfile")
def updateProfile(updateProfileSchema: tenantMeUpdateSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends(),tenant: str = Depends(getTenantInfo)):
    try:
        try:
            claims = Authorize.get_raw_jwt()
            userId = Authorize.get_jwt_subject()
            print(updateProfileSchema)
            db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))     
            getUser = db.query(TenantUser).filter(TenantUser.id == userId).first()
            print(getUser.id)
            print(getUser.status)
            if getUser and getUser.status== userStatusEnum.active:
                if updateProfileSchema.name != None or updateProfileSchema.name != "":
                    getUser.name = updateProfileSchema.name
                if updateProfileSchema.mobile != None or updateProfileSchema.mobile != "":
                    if len(updateProfileSchema.mobile)<10 or len(updateProfileSchema.mobile)>12:
                        return {
                            "status_code" : 400,
                            "message" : "mobile number should be of 10 digits",
                            "details" : {
                            }
                        }
                    getUser.mobile = updateProfileSchema.mobile
                    # getUser.isMobileVerified = False 
                db.commit()
                # record_task_creation({"userId":userId,"task":"profile updated","taskTime":datetime.now(),"userType":"classified"})
                return {
                    "status_code" : 200,
                    "message" : "profile updated successfully"
                }
            else:
                return {
                    "status_code" : 404,
                    "message" : "admin user not found",
                    "details" : {
                    }
                }
        except Exception as e:
            claims = Authorize.get_raw_jwt()
            userId = Authorize.get_jwt_subject()
            print(updateProfileSchema)
            db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))     
            getUser = db.query(TenantUser).filter(TenantUser.id == userId).first()
            print(getUser.id)
            print(getUser.status)
            if getUser and getUser.status== userStatusEnum.active:
                if updateProfileSchema.name != None or updateProfileSchema.name != "":
                    getUser.name = updateProfileSchema.name
                if updateProfileSchema.mobile != None or updateProfileSchema.mobile != "":
                    if len(updateProfileSchema.mobile)<10 or len(updateProfileSchema.mobile)>12:
                        return {
                            "status_code" : 400,
                            "message" : "mobile number should be of 10 digits",
                            "details" : {
                            }
                        }
                    getUser.mobile = updateProfileSchema.mobile
                    # getUser.isMobileVerified = False 
                db.commit()
                # record_task_creation({"userId":userId,"task":"profile updated","taskTime":datetime.now(),"userType":"classified"})
                return {
                    "status_code" : 200,
                    "message" : "profile updated successfully"
                }
            else:
                return {
                    "status_code" : 404,
                    "message" : "admin user not found",
                    "details" : {
                    }
                }
            
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")       
    
@tdr.post("/changePassword")
async def changePassword(user: changePasswordSchema, tenant: str = Depends(getTenantInfo), db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    try:
        
        try:# Authorize.jwt_required()
            get_id = Authorize.get_jwt_subject()
            print(get_id)
            db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
            tenantUpdatePassword=db.query(TenantUser).filter(TenantUser.id==get_id).first()
            if tenantUpdatePassword.password != hashlib.sha256(user.oldPassword.encode()).hexdigest():
                return {"status_code":400, "data": "Old password is incorrect"}
            if len(user.newPassword) < 8:
                return {"status_code":400, "data": "Password must be 8 characters long"}
            if user.newPassword ==user.oldPassword:
                return {"status_code":400, "data": "old and new password should not be same"}
                
            sendEmail(tenantUpdatePassword.email,user.newPassword)
            print(user.newPassword)
            tenantUpdatePassword.password = hashlib.sha256(user.newPassword.encode()).hexdigest()
            password=tenantUpdatePassword.password
            print(password,"password")
            result = db.add(tenantUpdatePassword)
            db.commit()
            return {
                    "status_code":200,
                    "detail": "Password changed successfully"}
        except Exception as e:
            get_id = Authorize.get_jwt_subject()
            print(get_id)
            db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
            tenantUpdatePassword=db.query(TenantUser).filter(TenantUser.id==get_id).first()
            if tenantUpdatePassword.password != hashlib.sha256(user.oldPassword.encode()).hexdigest():
                return {"status_code":400, "data": "Old password is incorrect"}
            if len(user.newPassword) < 8:
                return {"status_code":400, "data": "Password must be 8 characters long"}
            if user.newPassword ==user.oldPassword:
                return {"status_code":400, "data": "old and new password should not be same"}
                
            sendEmail(tenantUpdatePassword.email,user.newPassword)
            print(user.newPassword)
            tenantUpdatePassword.password = hashlib.sha256(user.newPassword.encode()).hexdigest()
            password=tenantUpdatePassword.password
            print(password,"password")
            result = db.add(tenantUpdatePassword)
            db.commit()
            return {
                    "status_code":200,
                    "detail": "Password changed successfully"}
            
    except Exception as e:
        return {"status_code":400, "data": str(e)}      
    
    
    
@tdr.post('/imageUrlAws')
async def test(filename: filenameSchema,db: Session = Depends(get_db),Authorize: AuthJWT = Depends()):  
    getId = Authorize.get_jwt_subject()
    return generate_upload_url(filename.filename)    
