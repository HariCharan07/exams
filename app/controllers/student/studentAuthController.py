import random
from app.app import app
from fastapi import Depends, Response,HTTPException
from fastapi import FastAPI
import hashlib
from app.libs.authJWT import * 

from app.libs.msg91Email import sendmail   

from app.schemas.student.studentschema import studentLoginSchema,studentForgotPasswordSchema,studentsignup,studentChangePassword,studentMobileLogin,studentemailverifyotplogin,studentEmailOtpLogin,studentVerifyOtpSchema,studentPasswordSchema
from datetime import datetime, timedelta

from app.libs.smsClient import sendsms
from app.libs.mongoclient import user_collection
from app.tpls.smsTpls import sendOtpTpl
from bson import ObjectId
@app.post("/users",tags=["student"])
async def createuser(student:studentsignup):
    user_dict=student.dict()
    user_collection.insert_one(user_dict)
    return{

        "status":200,
        "message": "user added successfully"
            }

@app.post("/login",tags=["student"])
async def login(studentlogin:studentLoginSchema,Authorize:AuthJWT=Depends()):
    user_dict=studentlogin.dict()
    email=user_collection.find_one({"$and":[{"email":studentlogin.email}, {"password":studentlogin.password}]})
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

@app.post("/forgot-password/",tags=["student"])
async def forgot_password(forgot_password: studentForgotPasswordSchema,Authorize:AuthJWT=Depends()):
    email = forgot_password.email
    user_data = user_collection.find_one({"email": email})

    otp = random.randint(100000, 999999)
    res = user_collection.update_one({"_id": user_data['_id']}, {
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

@app.post("/verifyOtp",tags=["student"])
def verify_otp(response: Response, otp: studentVerifyOtpSchema, Authorize: AuthJWT = Depends()):
    user_id = Authorize.get_jwt_subject()
    user_data = user_collection.find_one({"_id": ObjectId(user_id)})
    print(user_data)
    if user_data:
        if user_data['mobileOtp'] == otp.otp:
         return {
            "status":200,
            "message": "OTP verified successfully"
            }
        else:
            return{
                "message":list(otp),
                "message":"OTP verified successfully"
            }
    else:
        return{
            "status_code":400, "message":"Invalid OTP"
        }

@app.post("/reset-password/",tags=["student"])
async def reset_password(reset_data: studentPasswordSchema):
    email = reset_data.email
    new_password = reset_data.password
    
    user_data = user_collection.find_one({"email": email})
    if not user_data:
        return {
            "status_code": 404, 
            "detail": "User not found"
        }
    
    # Update the user's password
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()  # Hash the new password securely
    user_collection.update_one({"_id": user_data['_id']}, {"$set": {"password": hashed_password}})
    
    return {
        "status_code":202,
        "message": "Password reset successful"}


@app.post("/changepassword",tags=["student"])
async def changepassword(cpwd:studentChangePassword,Authorize:AuthJWT=Depends()):
    old_password = cpwd.old_password
    new_password = cpwd.new_password
    # studentname=cpwd.studentname
    ID=Authorize.get_jwt_subject()
    print(ID)
    query={"_id":ObjectId(ID),"password": (cpwd.old_password)}
    print(query)
    user_data = user_collection.find_one(query)
    print(user_data)
    
    # if user_data is None:
    #     raise HTTPException(status_code=404, detail={ 
    #             "status_code": 404,
    #             "message": "Invalid Credentials"
    #         })
    res = user_collection.update_one({"_id":ObjectId(ID)},

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
     
@app.post("/mobilelogin",tags=["student"])
def mobilelogin(data:studentMobileLogin,Authorize:AuthJWT=Depends()):
    user_dict=data.dict()
    #username=myItemColl.find_one({"username":(user.username)})
    query={"mobile":data.mobile}
    mobile=user_collection.find_one(query)
    print(mobile)
    if mobile:
            if data.mobile==mobile['mobile']:
                # print(hashlib.sha256(data.password.encode()).hexdigest())
                # if hashlib.sha256(data.password.encode()).hexdigest()==mobile['password']:
                #     token = Authorize.create_access_token(subject=str(mobile['_id']),
                #                                         user_claims={
                #                                         "type": "confidential",
                #                                         "mobile":True,
                #                                         "pwd":True
                #                                         })
                #     return HTTPException(status_code=200, detail={
                return{
                "status_code": 200,
                "message": "Login Successful",
                #"access_token": token
                 }
            else:
                    return {
                        "message":"password incorrect"
                        
                    }
    else:
        return{
            "status_code":404,
            "message":"invalid user"
        }
@app.post("/emailotplogin",tags=["student"])
def emailotplogin(login:studentEmailOtpLogin,Authorize:AuthJWT=Depends()):
            query={"email":login.email}
            email=user_collection.find_one(query)
            print(email)
            otp = random.randint(100000, 999999)
            print(otp)
            res = user_collection.update_one({"_id": email['_id']}, {
                                       "$set": {"emailOtp": otp, "emailOtpCreatedAt": datetime.now()}})
            if res.modified_count == 1:
                sendsms(email['email'], sendOtpTpl(otp))

                token = Authorize.create_access_token(subject=str(email['_id']),
                                                        user_claims={
                                                        "type": "confidential",
                                                        "email":True,
                                                        })
                return {
                    "status_code": 200,
                    "message": "otp sent successfully",
                    "access_token": token
                        }
            else:
                return {
                    "status_code":400,
                    "message":"something"
                }
@app.post("/verifyemailotplogin",tags=["student"])
def verifyemailotplogin(verifyotp:studentemailverifyotplogin,Authorize:AuthJWT=Depends()):
    user_id = Authorize.get_jwt_subject()
    user_data = user_collection.find_one({"_id": ObjectId(user_id)})
    
    print(user_data)
    if user_data:
        if user_data['emailOtp'] == verify_otp.otp:
         return {
            "status":200,
            "message": "OTP verified successfully"
            }
    else:
        return{
            "status_code":400, "message":"Invalid OTP"
        }
            
    
@app.post("/mobileotplogin",tags=["student"])
def emailotplogin(login:studentEmailOtpLogin,Authorize:AuthJWT=Depends()):
            query={"mobile":login.email}
            mobile=user_collection.find_one(query)
            print(mobile)
            otp = random.randint(100000, 999999)
            print(otp)
            res = user_collection.update_one({"_id": mobile['_id']}, {
                                       "$set": {"mobileOtp": otp, "emailOtpCreatedAt": datetime.now()}})
            if res.modified_count == 1:
                sendsms(mobile['mobile'], sendOtpTpl(otp))

                token = Authorize.create_access_token(subject=str(mobile['_id']),
                                                        user_claims={
                                                        "type": "confidential",
                                                        "email":True,
                                                        })
                return {
                    "status_code": 200,
                    "message": "otp sent successfully",
                    "access_token": token
                        }
                
            else :
                return {
                    "status_code":400,
                    "message":"invalid user"
                }
    
            