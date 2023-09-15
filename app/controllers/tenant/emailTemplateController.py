from app.schemas.tenant.tenantUserSchema import emailTempSchema

from fastapi import Depends

from app.app import app as tdr
# from app.schemas.globalSchemas import userStatusEnum
# from app.models.tenant.tenantModel import EmailTemplate
from datetime import datetime, timedelta

from app.libs.authJWT import AuthJWT
from app.libs.mongoclient import EmailTemplateCollection
from app.schemas.tenant.emailTemplateSchema import idSchema,emailTempSchema,temptype,updateEmailTempSchema
from bson import ObjectId
# #create email template
@tdr.post('/createEmailTemplate', tags=['emailTemplate'])
async def createEmailTemplate(emailTemp: emailTempSchema, Authorize: AuthJWT = Depends()):
    # try:
        data = Authorize.get_raw_jwt()
        emailTempName=EmailTemplateCollection.find_one({'templateName': emailTemp.templateName})
        emailTempType=EmailTemplateCollection.find_one({'templateType': emailTemp.templateType})
        if emailTempName and emailTempType:
            if emailTempName['templateName'] ==emailTemp.templateName and emailTempName['templateType'] ==emailTemp.templateType:
                return {"status_code": 400,
                        "message": "TemplateName already exists"} 
        emailTempData = emailTemp.dict()
        # emailTempData.created_by = 1
        EmailTemplateCollection.insert_one(emailTempData)
        # db.add(emailTempData)
        # db.commit()
        return {"status_code":200,
            "message": "emailTemplate created successfully"}
    # except Exception as e:
    #     return {"status_code": 400,
    #             "message": "emailTemplate not added",
    #             "error": str(e)}
        
        
@tdr.post('/getEmailTemplate', tags=['emailTemplate'])
async def getEmailTemplate(emailTemp: emailTempSchema, Authorize: AuthJWT = Depends()):
    
    # Authorize.jwt_required()
    # current_user = Authorize.get_jwt_subject()
    try:
        # print('SET search_path TO {}'.format(tenant['tenant']))
        # db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        query = {
    'status': 'active'
}
        emailTempData=EmailTemplateCollection.find(query)
        email_template_list = list(emailTempData)
        print(email_template_list)
        if emailTempData:
            return {"status_code": 200,
                    "message": "feteched suucessfully"}
        else:
            return {"status_code": 400,
                    "message": "No emailTemplate found"}
    except Exception as e:
        return {"status_code": 400,
                "message": "emailTemplate not found",
                "error": str(e)}
        

@tdr.post('/updateEmailTemplate', tags=['emailTemplate'])
async def updateEmailTemplate(emailTemp: updateEmailTempSchema, Authorize: AuthJWT = Depends()):
    
    # Authorize.jwt_required()
    # current_user = Authorize.get_jwt_subject()
    try:
        # db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        
        emailTempData=EmailTemplateCollection.find_one({"_id": ObjectId(emailTemp.id)})
        emailTempName=EmailTemplateCollection.find_one({'templateName': emailTemp.templateName,'_id': {'$ne':ObjectId(emailTemp.id)}})
        emailTempType=EmailTemplateCollection.find_one({'templateType': emailTemp.templateType,'_id': {'$ne':ObjectId(emailTemp.id)}})
        if emailTempName and emailTempType:
            if emailTempName.templateName == emailTemp.templateName and emailTempName.templateType == emailTemp.templateType:
                return {"status_code": 400,
                        "message": "TemplateName already exists"}
       
        if emailTempData:
            emailTempData.templateType = emailTemp.templateType
            emailTempData.templateContent = emailTemp.templateContent
            emailTempData.templateName = emailTemp.templateName
            emailTempData.status = emailTemp.status
            return {"status_code": 200,
                    "message": "emailTemplate updated successfully"}
        else:
            return {"status_code": 400,
                    "message": "No emailTemplate found"}
    except Exception as e:
        return {"status_code": 400,
                "message": "emailTemplate not updated",
                "error": str(e)}


# get email template by id
@tdr.post('/getEmailTemplateById', tags=['emailTemplate'])
async def getEmailTemplateById(id: idSchema, Authorize: AuthJWT = Depends()):
    
    # Authorize.jwt_required()
    # current_user = Authorize.get_jwt_subject()
    try:
        # db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        emailTempData=EmailTemplateCollection.find_one({'_id':ObjectId(id.id)})
        # name= db.query(TenantUser).filter(TenantUser.id == emailTempData.created_by).first().email
        if emailTempData:
            return {"status_code": 200,
                    "data": emailTempData,
                    # "created_by":name
                                }                    
        else:
            return {"status_code": 400,
                    "message": "No emailTemplate found"}
    except Exception as e:
        return {"status_code": 400,
                "message": "emailTemplate not found",
                "error": str(e)}                        
#delete email template
@tdr.post('/deleteEmailTemplate', tags=['emailTemplate'])
async def deleteEmailTemplate(id: idSchema, Authorize: AuthJWT = Depends()):
    
    # Authorize.jwt_required()
    # current_user = Authorize.get_jwt_subject()
    try:
        # print('SET search_path TO {}'.format(tenant['tenant']))
        # db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        emailTemp = EmailTemplateCollection.find_one({"_id":ObjectId(id.id)})

        if emailTemp is None:
             return {"status_code": 400,
                 "message": "email not found",}
        
        # result=candidateCollection.delete_one({"_id": ObjectId(candidate['id'])})
        
        return {"status_code": 200,
                    "message": "emailTemplate deleted successfully"
                    }
    except Exception as e:
        return {"status_code": 400,
                "message": "emailTemplate not deleted",
                "error": str(e)}
        
        
# # #get template by type
# @tdr.post('/getEmailTemplateByType', tags=['emailTemplate'])
# async def getEmailTemplateByType(tempType: temptype, Authorize: AuthJWT = Depends()):
    
    # Authorize.jwt_required()
    # current_user = Authorize.get_jwt_subject()
    # try:
        # print('SET search_path TO {}'.format(tenant['tenant']))
        # db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
    #     query = {
    # 'templateType': templateType,
    # 'status': 'active'
    #     }
    #     emailTempData=EmailTemplateCollection.find(query)

    #     if emailTempData:
    #         for i in emailTempData:
    #             # print(i.created_by)
    #             i.created_by = db.query(TenantUser).filter(TenantUser.id == i.created_by).first().email
    #         return {"status_code": 200,
    #                 "data": emailTempData,
    #                 # "created_by":emailTempData.created_by
    #                 }
    #     else:
    #         return {"status_code": 200,
    #                 "data":[]}
    # except Exception as e:
    #     return {"status_code": 400,
    #             "message": "emailTemplate not found",
    #             "error": str(e)}        