# from app.routes import tenantAppRouter as tar
from app.schemas.tenant.tenantUserSchema import tenantTempSchema,TenantLoginSchema,passwordResetSchema,tenantForgotPasswordSchema,tenantUserChangePasswordSchema
from app.app import app
from fastapi import Depends, Response
import random
from app.confy.whitelist import admin_allowed_domain
import hashlib 
from app.libs.msg91Email import sendmail 
from fastapi import Depends, Response,HTTPException
# from app.models.tenant import tenantuser
from bson import ObjectId
from app.libs.authJWT import * 
from app.libs.smsClient import sendsms
from app.tpls.smsTpls import sendOtpTpl
from datetime import datetime, timedelta
from app.libs.mongoclient import tenant_collection
# from  app.models.tenant.tenantModel import TenantUser
# from app.utills.logsHelper import record_user_login,record_user_logout,record_task_creation,record_user_creation
@app.post("/users/")
async def createuser(student:tenantTempSchema):
    user_dict=student.dict()
    tenant_collection.insert_one(user_dict)
    return{

        "status":200,
        "message": "user added successfully"
            }

@app.post("/login/")
async def login(studentlogin:TenantLoginSchema,Authorize:AuthJWT=Depends()):
    user_dict=studentlogin.dict()
    email=tenant_collection.find_one({"$and":[{"email":studentlogin.email}, {"password":studentlogin.password}]})
    if email: 
        access_token = Authorize.create_access_token(subject=str(email['_id']), expires_time=6048000, 
                                    
                user_claims= {
                        "email":studentlogin.email,
                    })        
        return {"status_code": 200,
                    "message": "Login successfully",
                    "access_token": access_token,} 
    else:
        return{
            "status_code":400,
            "message":"invalid details"
        }

@app.post("/forgot-password/")
async def forgot_password(forgot_password: tenantForgotPasswordSchema,Authorize:AuthJWT=Depends()):
    email = forgot_password.email
    user_data = tenant_collection.find_one({"email": email})

    otp = random.randint(100000, 999999)
    res = tenant_collection.update_one({"_id": user_data['_id']}, {
                                   "$set": {"mobileOtp": otp, "mobileOtpCreatedAt": datetime.now()}})
        # sendsms(user['mobile'], sendOtpTpl(otp))
    print(user_data['email'])
    emailsent=sendmail(user_data['email'],"think75","info@think75.com","otp","you OTp for login is "+str(otp))
        # sendmail("vikas50572kushwaha@gmail.com", 'Vikas Kushwaha', 'info@koneqto.com', 'Test Subject', 'This is a test body'+str(otp))
    print(emailsent)
    access_token = Authorize.create_access_token(subject=str(user_data['_id']),
                                                     user_claims={

            "type": "confidential",
            "otpVerified": False,
            "forgotPassword": True
        }
        )

    return HTTPException(status_code=200, detail={
            "status_code": 200,
            "message": "User found",
            "access_token": access_token

        })

# @app.post("/verifyOtp")
# def verify_otp(response: Response, otp: tenantVerifyOtpSchema, Authorize: AuthJWT = Depends()):
#     user_id = Authorize.get_jwt_subject()
#     user_data = tenant_collection.find_one({"_id": ObjectId(user_id)})
#     print(user_data)
#     if user_data:
#         if user_data['mobileOtp'] == otp.otp:
#          return {
#             "status":200,
#             "message": "OTP verified successfully"
#             }
#         else:
#             return{
#                 "message":list(otp),
#                 "message":"OTP verified successfully"
#             }
#     else:
#         return{
#             "status_code":400, "message":"Invalid OTP"
#         }

@app.post("/reset-password/")
async def reset_password(reset_data: passwordResetSchema):
    email = reset_data.email
    new_password = reset_data.password
    
    user_data = tenant_collection.find_one({"email": email})
    if not user_data:
        return {
            "status_code": 404, 
            "detail": "User not found"
        }
    
    # Update the user's password
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()  # Hash the new password securely
    tenant_collection.update_one({"_id": user_data['_id']}, {"$set": {"password": hashed_password}})
    
    return {
        "status_code":202,
        "message": "Password reset successful"}


@app.post("/changepassword")
async def changepassword(cpwd:tenantUserChangePasswordSchema,Authorize:AuthJWT=Depends()):
    old_password = cpwd.old_password
    new_password = cpwd.new_password
    # studentname=cpwd.studentname
    ID=Authorize.get_jwt_subject()
    print(ID)
    query={"_id":ObjectId(ID),"password": (cpwd.old_password)}
    print(query)
    user_data = tenant_collection.find_one(query)
    print(user_data)
    
    # if user_data is None:
    #     raise HTTPException(status_code=404, detail={ 
    #             "status_code": 404,
    #             "message": "Invalid Credentials"
    #         })
    res = tenant_collection.update_one({"_id":ObjectId(ID)},

                                   {"$set": {"password": cpwd.new_password}})
    if res.modified_count == 1:
        return HTTPException(
            status_code=200, detail={
                "status_code": 200,
                "message": "Password Changed Successfully"
            })
    else:
      raise HTTPException(status_code=500, detail={

                "status_code": 500,
                "message": "Something Went Wrong"
    })
     


