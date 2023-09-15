from fastapi import APIRouter, Depends, HTTPException, status   
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.libs.psqlDBClient import get_db
from app.libs.mongoCLient import newQuestion_admin_collection
from app.libs.authJWT import *
from app.routes import tenantDashboardRouter as tdr
from app.models.admin.adminWorkspaceAssessmentModel import  adminAssessmentModel,adminWorkspace
   


# to list all assessments
# @tdr.get("/listAdminAssessment")
# async def listAssessment(db: Session = Depends(get_db), Authoriza: AuthJWT = Depends()):
#     try:
#         # Authoriza.jwt_required()
#         getId = Authoriza.get_jwt_subject()
#         db.execute(text('SET search_path TO public'))
#         assessmentList = db.query(adminAssessmentModel).all()
#         assessmentList = [i.__dict__ for i in assessmentList]
#         for i in assessmentList:
#             questions= newQuestion_admin_collection.distinct('assessment_id')
#             print(questions)
#             questions=newQuestion_admin_collection.find()
#             i['numberOfQuestions']=len(list(questions))
            
#         return {"status_code": 200,
#                 "data": assessmentList}
        
#     except Exception as e:
#         return {"status_code": 400,
#                 "message": "No assessment found",
#                 "error": str(e)}     
        



@tdr.get("/listAdminAssessment")
async def listAssessment(db: Session = Depends(get_db), Authoriza: AuthJWT = Depends()):
    try:
        # Authoriza.jwt_required()
        getId = Authoriza.get_jwt_subject()
        db.execute(text('SET search_path TO public'))
        assessmentList = db.query(adminAssessmentModel).all()
        assessmentList = [i.__dict__ for i in assessmentList]
        for i in assessmentList:
            i['numberOfQuestions']=0
            pipeline = [
            {"$group": {
                "_id": {"workspace_id": "$workspace_id", "assessment_id": "$assessment_id"},
                "count": { "$sum": 1 },
                "category": {"$push": "$$ROOT"}
            }}
        ]
            output = newQuestion_admin_collection.aggregate(pipeline)
            
            for group in output:
                # print(group)
                category = group["category"]

                if int(i['id'])==int(group['_id']['assessment_id']) and int(i['tenantWorkspaceId'])==int(group['_id']['workspace_id']):
                    i['numberOfQuestions']=group['count']
                # workspace_id = group["_id"]["workspace_id"]
                # assessment_id = group["_id"]["assessment_id"]
                # Process each category as per your requirement
                # print(f"Workspace ID: {workspace_id}, Assessment ID: {assessment_id}")
                    # i['numberOfQuestions']=len(list(category))
                # print(i['numberOfQuestions'])
                
                # for document in category:
                #     # Access individual documents in the category
                #     print(document)
            print(i)

            
        return {"status_code": 200,
                "data": assessmentList}
        
    except Exception as e:
        return {"status_code": 400,
                "message": "No assessment found",
                "error": str(e)} 
