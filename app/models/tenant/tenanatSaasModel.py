from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, create_engine, MetaData, Table
from sqlalchemy.orm import relationship
from app.libs.psqlDBClient import Base, get_db, engine
from app.utills.helper import generate_aplhanum_random
from sqlalchemy import Enum
from datetime import datetime, timedelta
from app.schemas.admin.adminUserSchema import adminRoleEnum
from app.schemas.globalSchemas import userStatusEnum,StatusEnum




from sqlalchemy.schema import CreateSchema


#python function to create a new schema in the database if schema doesnot exist
def createSchema(schemaName):
    engine = create_engine('postgresql://trovendb:troven@trovenapi.smartinternz.com:5432/trovenBeta', echo=False)
    metadata = MetaData(schema=schemaName)
    
    
    tenantUser = Table('tenantUser', metadata,
                            Column("id", Integer, primary_key=True),
                            Column("name",String, nullable=False),
                            Column("email",String, unique=True, nullable=False),
                            Column("mobile",String, nullable=False, unique=True),
                            Column("sortname",String, nullable=False),
                            Column("company",String, nullable=False),
                            Column("password",String, nullable=False),
                            Column("role",Enum(adminRoleEnum), nullable=False, default=adminRoleEnum.admin),
                            Column("status",Enum(userStatusEnum), nullable=False, default=userStatusEnum.active),
                            Column("profilePic",String, nullable=True),
                            Column("mobileOtp",String, nullable=True, default=generate_aplhanum_random(6)),
                            Column("mobileOtpCreatedAt",DateTime, nullable=True, default = datetime.now()),
                            Column("mfa",Boolean, nullable=True, default=False),
                            Column("Tfa",Boolean, nullable=True, default=False),
                            Column("mfaSecretCode",String, nullable=True, default="3453453453"),
                            Column("isMobileVerified",Boolean, nullable=True, default=False),
                            Column("emailOtp",String, nullable=True, default=generate_aplhanum_random(6)),
                            Column("emailOtpCreatedAt",DateTime, nullable=True, default = datetime.now()),
                            Column("isEmailVerified",Boolean, nullable=True, default=False),
                            Column("subscriptionId",Integer, nullable=True),
                            Column("created_by",Integer, nullable=True),
                            Column("created_at",DateTime, nullable=True, default = datetime.now()),
                            Column("updated_at",DateTime, nullable=True, default = datetime.now()),
                            Column("deleted_at",DateTime, nullable=True, default = datetime.now())
                          
                            )
    
    
    
    tenantWorkspace = Table('tenantWorkspace', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String, nullable=False),
                            Column('description', String, nullable=False),
                            Column('color', String, nullable=True),
                            Column('image', String, nullable=True),
                            Column('status', Enum(StatusEnum), nullable=True, default=StatusEnum.active),
                            Column('created_by', Integer, ForeignKey('tenantUser.id'), nullable=True),
                            Column('created_at', DateTime, default=datetime.now()),
                            Column('updated_at', DateTime),
                            Column('deleted_at', DateTime)
                             )
    
    
    
    tenantAssessment = Table('tenantAssessment', metadata,
                            Column("id", Integer, primary_key=True),
                            Column("name",String, nullable=False),
                            Column("color",String, unique=False, nullable=False),
                            Column("description",String, nullable=False, unique=False),
                            Column("instructions",String, nullable=True),
                            Column("tenantWorkspaceId", Integer, ForeignKey("tenantWorkspace.id"), nullable=False),
                            Column('difficultyLevel', String, nullable=False),
                            # Column("section",String, nullable=False),
                            Column("duration",Integer, nullable=True),
                            Column("totalMarks",Integer, nullable=False),
                            Column("negativeMarks",Integer, nullable=False, default=False),
                            Column("passMarks",Integer, nullable=True),
                            Column("examStartDate",DateTime, nullable=False, default = datetime.now()),
                            Column("examEndDate",DateTime, nullable=False, default = datetime.now()),
                            Column("showResult",Boolean, nullable=False),
                            Column("status",Enum(StatusEnum), nullable=False, default=StatusEnum.active),
                            Column("bannerImage",String, nullable=False, default=False),
                            Column("sponserId", Integer, ForeignKey("sponser.id"), nullable=True),
                            Column("registered",Integer, nullable=False, default=0),
                            Column("qualified",Integer, nullable=False, default=0),
                            Column("completed",Integer, nullable=False, default=0),
                            Column("disableRightClick",Boolean, nullable=False, default=False),
                            Column("disableCopyPaste",Boolean, nullable=False, default=False),
                            Column("startWithFullScreen",Boolean, nullable=False, default=False),
                            Column("submitOnTabSwitch",Boolean, nullable=False, default=False),
                            Column("enableWebCam",Boolean, nullable=False, default=False),
                            Column("enableMicrophone",Boolean, nullable=False, default=False),
                            Column("allowMobile",Boolean, nullable=False, default=False),
                            Column("mfaVerification",Boolean, nullable=False, default=False),
                            Column("isEmailOtpVerified",Boolean, nullable=False, default=False),
                            Column("created_at",DateTime, nullable=False, default = datetime.now()),
                            Column("created_by",Integer, ForeignKey("tenantUser.id"), nullable=True),
                            Column("updated_at",DateTime, nullable=False, default = datetime.now()),
                            Column("deleted_at",DateTime, nullable=False, default = datetime.now())
                            )
    
    sponser = Table('sponser', metadata,
                            Column("id", Integer, primary_key=True),
                            Column("name",String, nullable=False),
                            Column("description",String, nullable=False),
                            Column("website",String, nullable=False),
                            Column("logo",String, nullable=True),
                            )
    
    
    skills = Table('skills', metadata,
                   Column("id", Integer, primary_key=True),
                   Column("skill",String, nullable=False),
                   Column("description",String, nullable=False),
                   Column("logo",String, nullable=False),
                   Column("parent", Integer, ForeignKey("skills.id"), nullable=True),
                   )   
    
    
    emailTemplate = Table('emailTemplate', metadata,
                          Column("id", Integer, primary_key=True),
                          Column("templateName",String, nullable=True),
                          Column("templateType",String, nullable=False),
                          Column('templateContent', String, nullable=True),
                          Column("created_at",DateTime, nullable=False, default = datetime.now()),
                          Column("created_by",Integer,ForeignKey("tenantUser.id"), nullable=True),
                          Column("status",Enum(StatusEnum), nullable=True, default=StatusEnum.active),
                          Column("visibility",Boolean, nullable=False, default=False),
    )
    
    
    
    #CREATE TABLE FOR ASSESSMENT QUESTIONSTABLE FOR ACTIVITY
    activity = Table('activity', metadata,
                     Column("id", Integer, primary_key=True),
                     Column("APIKEY", String, nullable=False),
                     Column("userId", Integer, ForeignKey("tenantUser.id"), nullable=False),
                     Column("created_at", DateTime, nullable=False, default = datetime.now()),
                     Column("status", Enum(StatusEnum), nullable=False, default=StatusEnum.active),
                    )
                     
                     
    # create a table for credits
    uses = Table('uses', metadata,
                 Column("id", Integer, primary_key=True),
                 Column("name", String, nullable=True),
                 Column("credits", Integer, nullable=False),
                 Column("duration", Integer, nullable=True),
                 )                
                    
                    
                    
                    
                    
    conn = engine.connect()
    if schemaName not in conn.dialect.get_schema_names(conn):
        conn.execute(CreateSchema(schemaName))
        conn.commit()
        
    else:
        print("Schema already exists")
        
    metadata.create_all(engine)
    
    
    