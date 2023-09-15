from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from typing import Union
from app.routes import tenantDashboardRouter as tdr
from io import BytesIO
from app.schemas.tenant.tenantSkillSchema import SkillSchema,SkillIdSchema,SkillUpdateSchema
import pandas as pd
from app.routes import getTenantInfo
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.libs.authJWT import *
from app.libs.psqlDBClient import get_db
from app.models.tenant.tenantModel import TenantWorkspace
from datetime import datetime, timedelta
from sqlalchemy.orm import aliased
from app.models.tenant.tenantModel import Skills


@tdr.post('/add_skill')
async def add_skill(skill: SkillSchema, db: Session = Depends(get_db),tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
    try:
        # Authoriza.jwt_required()
        # getId = Authoriza.get_jwt_subject()
        # print(tenant['tenant'],getId)
# conversion of skillParent to id
        skillId=skill.parent
        db.execute(text('SET search_path TO {}'.format(tenant['tenant']))) 
        if skillId:
            skill.parent=db.query(Skills).filter(Skills.skill == skillId).first().id
        skillData=db.query(Skills).filter(Skills.skill == skill.skill).first()
        if skillData:
            return {"status_code": 400,
                    "message": "Skill already exists"}
        skillModel=skill.dict()
        if skillModel['parent'] == "":
            skillModel['parent'] = []
        db.add(Skills(**skillModel))
        db.commit()
        return {"status_code": 200,
                "message": "skill added successfully"}
    except Exception as e:
        return {"status_code": 400,
                "message": "skill not added",
                "error": str(e)}
        
# to get all skills
@tdr.get('/get_skills')
async def get_skills(db: Session = Depends(get_db),tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
    try:
        getId = Authoriza.get_jwt_subject()
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        skills = db.query(Skills).order_by(Skills.id).all()
        for i in skills:
            parentId = i.parent
            skill_data = db.query(Skills).filter(Skills.id == i.parent).first()
            if skill_data:
                i.parent = skill_data.skill

            
                
        return {"status_code": 200,
                "data": skills,
                }
    except Exception as e:
        return {"status_code": 400,
                "message": "No skills found",
                "error": str(e)}    
        
        
        
        
        
        
        
#to update skills
@tdr.post('/update_skill')
async def update_skill(skill: SkillSchema, db: Session = Depends(get_db),tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
    try:
        # Authoriza.jwt_required()
        # getId = Authoriza.get_jwt_subject()
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))

        if skill.parent:
            print(skill.parent)
            skill.parent = db.query(Skills).filter(Skills.skill == skill.parent).first().id
            print(skill.parent)
        skill_data = db.query(Skills).filter(Skills.id == skill.id).first()
        skill_data.skill = skill.skill
        skill_data.parent = skill.parent
        skill_data.logo = skill.logo
        skill_data.description = skill.description
        db.commit()
        return {"status_code": 200,
                "message": "Skill updated successfully"}
    except Exception as e:
        return {"status_code": 400,
                "message": "Skill not updated",
                "error": str(e)}
        
        
#to delete skills by id
@tdr.post('/delete_skill')
async def delete_skill(id: SkillIdSchema,db: Session = Depends(get_db),tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
    try:
        # Authoriza.jwt_required()
        # getId = Authoriza.get_jwt_subject()
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        skill_data = db.query(Skills).filter(Skills.id == int(id.id)).first()
        db.delete(skill_data)
        db.commit()
        return {"status_code": 200,
                "message": "Skill deleted successfully"}
    except Exception as e:
        return {"status_code": 400,
                "message": "Skill not deleted",
                "error": str(e)}
            
#to get skill by id
@tdr.get('/get_skill_by_id')
async def get_skill_by_id(id: SkillIdSchema, db: Session = Depends(get_db),tenant: str = Depends(getTenantInfo), Authoriza: AuthJWT = Depends()):
    try:
        # Authoriza.jwt_required()
        # getId = Authoriza.get_jwt_subject()
        db.execute(text('SET search_path TO {}'.format(tenant['tenant'])))
        skill_data = db.query(Skills).filter(Skills.id == id.id).first()
        if skill_data:
            return {"status_code": 200,
                    "data": skill_data}
    except Exception as e:
        return {"status_code": 400,
                "message": "No skill found",
                "error": str(e)}
                    
    
         