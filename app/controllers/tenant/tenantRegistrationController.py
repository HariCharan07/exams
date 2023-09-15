from app.routes import tenantAppRouter as tar
from app.app import adminApp
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.libs.psqlDBClient import get_db
from app.schemas.tenant.tenantUserSchema import tenantTempSchema,tenantUserSchema
from sqlalchemy import text
import os
from app.utills.helper import *
from app.utills.helper import generate_aplhanum_random
from app.models.tenant.tenanatSaasModel import createSchema
from app.models.tenant.tenantModel import TenantTemp,TenantUser
from app.settings import FERNET_KEY
from app.libs.awsMods import sendEmail
import hashlib
import json
from app.models.admin.paymentAdminModel import paymentPlans 
from app.models.tenant.tenantModel import Uses
from app.schemas.tenant.tenantUserSchema import tenantUserMeSchema


@adminApp.post("/register",tags=["TenantRegistrtion"])
def register(tenant: tenantTempSchema , db: Session = Depends(get_db)):
    try:
        if len(tenant.mobile)<10 or len(tenant.mobile)>12:
            return {"status_code": 400,
                "message": "mobile number must be 10 to 12 digits"}
        db.execute(text('SET search_path TO public'))
        tenantModel = tenant.dict()
        tenantDomain = tenantModel['email'].split('@')[1]
        path = os. getcwd() + '/app/utills/emailDomain.txt'
        if checkStringinfile(path, tenantDomain) == False:
            tenantData = db.query(TenantTemp).filter(TenantTemp.email.like("%" + tenantDomain)).first()
            tenantMobile = db.query(TenantTemp).filter(TenantTemp.mobile==tenant.mobile).first()
            if tenantMobile:
                return {"status_code": 402,
                        "message": "mobile number already registered"}
            if tenantData == None:
                okey = generate_aplhanum_random(6) 
                emailOtp = okey
                tenantModel['emailOtp']  = okey
                linkText = tenantModel['email'] + ":" + emailOtp 
                password = tenantModel['password'] 
                tenantModel['password'] = hashlib.sha256(tenant.password.encode()).hexdigest()    
                print("linkText",linkText)
                activationLink = encrypt(FERNET_KEY, linkText)
                data=decrypt(FERNET_KEY,activationLink)
                link=activationLink.decode()
                actLink = 'https://trovenfe.smartinternz.com/tenant/activation?activationLink=' +(link)
                sendEmail(tenantModel['email'], actLink)
                db.add(TenantTemp(**tenantModel))
                db.commit()
                return {"message": "success",
                        "status_code": 200, 
                        "activationLink": activationLink}

            else:
                return {"status_code":402,
                    "message": "this org already registered"}
        else:
            return {"status_code":401,
                "message": "this domain is not allowed"}
       
    except Exception as e:
        return {"status_code": 500,
            "message": str(e),
            "details": "duplicacy error"}    

@adminApp.get("/activation",tags=["TenantRegistrtion"])
def activation(activationLink: str, db: Session = Depends(get_db)):
    # try:
        db.execute(text('SET search_path TO public'))

        data = decrypt(FERNET_KEY,activationLink)
        email=data.split(':')[0]
        otp=data.split(':')[1]
        tenant=db.query(TenantTemp).filter(TenantTemp.email== email).first()
        sort=tenant.sortname
        print("tenant",tenant)
        print("tenant.emailOtp",tenant.emailOtp)
        print("otp",otp)

        if tenant.emailOtp == otp:
                    createSchema(tenant.sortname)
                    tenantData = TenantUser(
                        name=tenant.company,
                        sortname=tenant.sortname,
                        email=tenant.email,
                        mobile=tenant.mobile,
                        password=tenant.password,
                        company=tenant.company,
                        mfaSecretCode=tenant.mfaSecretCode, 
                        )
                    db.add(tenantData)
                    db.commit()

                    db.execute(text('SET search_path TO {}'.format(tenant.sortname)))

                    tenantUser = TenantUser(
                        name=tenant.name, 
                        email= tenant.email,
                        mobile= tenant.mobile,
                        sortname= tenant.sortname,
                        password= tenant.password,
                        role = 'superAdmin',
                        company=tenant.company,
                        mfaSecretCode=tenant.mfaSecretCode,
                        subscriptionId=1,

                    )
                    db.add(tenantUser)
                    db.commit()
                    
                    db.execute(text('SET search_path TO public'))
                    addStringtofile(os. getcwd() + '/app/utills/clients.txt', tenant.email.split('@')[1])
                    addStringtofile(os. getcwd() + '/app/utills/companySortnames.txt', tenant.sortname)                   
                    
                    db.execute(text('SET search_path TO public'))
                    yourPlans=db.query(paymentPlans).first()
                    print("yourPlans",yourPlans)
                    db.execute(text('SET search_path TO {}'.format(sort)))
                    getUser = db.query(TenantUser).filter(TenantUser.id == 1).first()
                    print("getUser",getUser)
                    print("getUser",getUser)
                    if getUser and yourPlans:
                        getUser = tenantUserMeSchema(**getUser.__dict__)
                        userDetails = getUser.dict()
                        userDetails = getUser.__dict__
                        plan=yourPlans.__dict__
                        planModules = plan['modules']
                        moduleJson = json.loads(planModules)
                        userDetails['planModules']=moduleJson
                        name=userDetails['planModules'][0]['moduleNames']
                        credits=userDetails['planModules'][0]['credits']
                        duration=userDetails['planModules'][0]['duration']
                        
                        
                        planDetail={"name":name,"credits":credits,"duration":duration}
                        print("planDetail",planDetail)
                        db.add(Uses(**planDetail))
                        db.commit()
                        print("commit done")
                        sendEmail(email, "You can access your account now click on this Link https://{0}trovenfe.smartinternz.com/tenant/login".format(sort+ '.') )


                    
                        return {
                            "status_code" : 200,
                            "message": "success"
                         
                            }
                    return {"status_code": 400,
                            "message": "user not found"}
                            
        else:
                return {"status_code":400,
                    "message": "email not found"}
    # except Exception as e:
    #     return {"status_code": 500,
    #         "message": str(e),
    #         "details": "duplicacy error"}                    