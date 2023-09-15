from app.app import app
from app.libs.authJWT import * 
from app.libs.mongoclient import newQuestion_collection
from app.schemas.student.studentschema import Assessment,assesmsentScheema
from fastapi import FastAPI,Depends
from app.libs.mongoclient import mongoDBClient

@app.get("/listAssessment",tags=["studentdashboard"])
async def listAssessment(data:Assessment, Authoriza: AuthJWT = Depends()):
    try:
        # Authoriza.jwt_required()
        getId = Authoriza.get_jwt_subject()
        assessment_list = []
        # db.execute(text('SET search_path TO public'))
        # assessmentList = db.query(adminAssessmentModel).all()
        # for i in assessmentList:
        #     questions=newQuestion_collection.find({"workspace_id":i.tenantWorkspaceId,"assessment_id":i.id})
        #     i['numberOfQuestions']=len(list(questions))
        for assessment in assessment_list.find():
         question_count = newQuestion_collection.count_documents({
                "workspace_id": assessment['tenantWorkspaceId'],
                "assessment_id": assessment['id']
         })
         
        assessment_dict = assessment.copy()
        assessment_dict['numberOfQuestions'] = question_count
        assessment_list.append(assessment_dict)
        return {"status_code": 200, "data": assessment_list}
    except Exception as e:
        return {"status_code": 400, "message": "No assessment found", "error": str(e)}
    
    
    

