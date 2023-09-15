# from fastapi import Depends
# from app.routes import getTenantInfo,tenantDashboardRouter as tdr
# from sqlalchemy.orm import Session
# from app.libs.psqlDBClient import get_db
# from app.libs.authJWT import *
# from sqlalchemy import text
# from app.libs.mongoCLient import mongoDBClient,newQuestion_collection,assessment_collection,UploadAssessmentExcel
# from app.models.admin.adminWorkspaceAssessmentModel import  adminAssessmentModel
# from datetime import datetime
# from app.models.admin.adminUserModel import AdminUser
# from app.schemas.admin.skillQuestionbankSchema import skillQiestionSchema,updateSkillQuestionSchema,idSchema
# from app.models.admin.adminQuestionbankModel import adminQuestionBankModel
# from app.models.admin.skillsAndSponsersModel import Skills


# @tdr.post("/createSkillQuestionBank")
# def createSkillQuestion(skillQuestion: skillQiestionSchema,db: Session = Depends(get_db), Authoriza: AuthJWT = Depends(),tenant: str = Depends(getTenantInfo)):
#     # try:
#         getId = Authoriza.get_jwt_subject()
#         db.execute(text('SET search_path TO public'))
#         skillQuestion.created_by = getId
#         skillQuestionList = db.query(adminQuestionBankModel).filter(adminQuestionBankModel.skill == skillQuestion.skill).first()    
#         if skillQuestionList:
#             return {"status_code": 400,
#                 "message": "skillQuestion already exists"}  
#         # if skillQuestion.topic:
#         #     skill_topic = db.query(Skills).filter(Skills.id ==skillQuestion.topic).first().skill
#         #     skillQuestion.topic = skill_topic
            
#         skillQuestionInsertData = adminQuestionBankModel(**skillQuestion.dict())
#         db.add(skillQuestionInsertData)
#         db.commit()
#         return {"status_code":200,
#             "message": "skillQuestion created successfully"}
#     # except Exception as e:
#     #     return{"status_code":400,
#     #            "message": str(e)}
    


    
# # to list all assessments
# @tdr.get("/listSkillQuestionBank")
# async def listSkillquestion(db: Session = Depends(get_db), Authoriza: AuthJWT = Depends(),tenant: str = Depends(getTenantInfo)):
#     try:
#         # Authoriza.jwt_required()
#         getId = Authoriza.get_jwt_subject()
#         db.execute(text('SET search_path TO public'))
#         skillQuestion_admin_collection=mongoDBClient["skillQuestionAdmin"]
#         skillQuestion = db.query(adminQuestionBankModel).order_by(adminQuestionBankModel.id.desc()).all()
#         skillQuestion = [i.__dict__ for i in skillQuestion]
#         for i in skillQuestion:
#             i['created_by'] = db.query(AdminUser).filter(AdminUser.id == i['created_by']).first().name

                        
#             pipeline = [
#             {"$group": {
#                 "_id": {"questionBankId": "$questionBankId"},
#                 "category": {"$push": "$$ROOT"}
#             }}
#         ]
#             output=skillQuestion_admin_collection.aggregate(pipeline)
#             for group in output:
#                 questionBankId = group["_id"]["questionBankId"]
#                 category = group["category"]
#                 i['numberOfQuestions']=len(list(category))           
                    
                
        
#         return {"status_code": 200,
#                 "data": skillQuestion}
#     except Exception as e:
#         return {"status_code": 400,
#                 "message": "No question found",
#                 "error": str(e)}     
        
        
        
# # get assessment by id
# @tdr.post("/getSkillQuestionBankById")
# async def getSkillQuestiont(id: idSchema,db: Session = Depends(get_db), Authoriza: AuthJWT = Depends(),tenant: str = Depends(getTenantInfo)):
#     try:
#         # Authoriza.jwt_required()
#         get_id = Authoriza.get_jwt_subject()
#         db.execute(text('SET search_path TO public'))
#         question = db.query(adminQuestionBankModel).filter(adminQuestionBankModel.id==id.id).first()
#         if question is None:
#             return {"status_code": 400,
#                     "message": "Question not found"}
#         return {"status_code": 200,
#                     "data": question}
#     except Exception as e:
#             return {
#                 "status_code": 400,
#                 "data": str(e)
#                 }
            
            
            
        

        
# # update assessment
# @tdr.post("/updateSkillQuestionBank")
# async def updateSkillQuestion(questionbank: updateSkillQuestionSchema,db: Session = Depends(get_db), Authoriza: AuthJWT = Depends(),tenant: str = Depends(getTenantInfo)):
#     try:
#         # Authoriza.jwt_required()
#         get_id = Authoriza.get_jwt_subject()
#         db.execute(text('SET search_path TO public'))
#         questionList=db.query(adminQuestionBankModel).filter(adminQuestionBankModel.id==questionbank.id).first()
#         if questionList == None:
#             return {"status_code": 400,
#                 "message": "questionbank not found"}
#         else:
#             db.query(adminQuestionBankModel).filter(adminQuestionBankModel.id==questionbank.id).update(questionbank.dict())
#             db.commit()
#         return {"status_code":200,
#             "message": "questionbank updated successfully"}
        
#     except Exception as e:
#         return {"status_code":400,
#                 "message": str(e)}
        
    
# #delete assessment
# @tdr.post("/deleteSkillQuestionBank")
# async def deleteSkillQuestion(id: idSchema,db: Session = Depends(get_db), Authoriza: AuthJWT = Depends(),tenant: str = Depends(getTenantInfo)):
#     # Authoriza.jwt_required()
#     try:
#         get_id = Authoriza.get_jwt_subject()
#         db.execute(text('SET search_path TO public'))
#         skillQuestion = db.query(adminQuestionBankModel).get(id.id)

#         if skillQuestion is None:
#             return {"status_code": 400,
#                 "message": "questionBank not found"}
#         else:
#             db.query(adminQuestionBankModel).filter(adminQuestionBankModel.id==id.id).delete()
#             db.commit()
#             return {
#                 "status_code": 200,
#                 "message": "QuestionBank deleted successfully"
#             }
#     except Exception as e:
#         return {
#             "status_code": 400,
#             "message": "questionBank not found",
#             "error": str(e)
#         }        
   
   