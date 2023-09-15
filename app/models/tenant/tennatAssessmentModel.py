# from datetime import datetime
# from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, ForeignKey

# from pydantic import BaseModel

# class assessmentModel(Base):
#     __tablename__ = 'tenantAssessment'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     color = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     instructions = Column(String, unique=False, nullable=True)
#     tenantWorkspaceId = Column(Integer, ForeignKey('tenantWorkspace.id'))
#     difficultyLevel = Column(String, nullable=False)
#     # section = Column(String, nullable=False)
#     duration = Column(String, nullable=False, unique=False)
#     totalMarks = Column(Integer, nullable=False)
#     negativeMarks = Column(Integer, nullable=False)
#     passMarks = Column(Integer, nullable=False)
#     examStartDate = Column(DateTime, nullable=False, default = datetime.now()) 
#     examEndDate = Column(DateTime, nullable=False, default = datetime.now())
#     showResult = Column(Boolean, nullable=False, default=False)
#     status= Column(Enum(userStatusEnum), nullable=False, default=userStatusEnum.active)
#     bannerImage = Column(String, nullable=False)
#     sponserId = Column(String, ForeignKey('sponser.id'),nullable=True)
#     registered=Column(Integer,nullable=False,default=0)
#     qualified=Column(Integer,nullable=False,default=0)
#     completed=Column(Integer,nullable=False,default=0)
#     disableRightClick=Column(Boolean,nullable=False,default=False)
#     disableCopyPaste=Column(Boolean,nullable=False,default=False)
#     startWithFullScreen=Column(Boolean,nullable=False,default=False)
#     submitOnTabSwitch=Column(Boolean,nullable=False,default=False)
#     enableWebCam=Column(Boolean,nullable=False,default=False)
#     enableMicrophone=Column(Boolean,nullable=False,default=False)
#     allowMobile=Column(Boolean,nullable=False,default=False)
#     mfaVerification=Column(Boolean,nullable=False,default=False)
#     isEmailOtpVerified = Column(Boolean, nullable=False, default=False)
#     created_by = Column(Integer, ForeignKey('tenantUser.id'))
#     created_at = Column(DateTime, default=datetime.now())
#     updated_at = Column(DateTime, default=datetime.now())
#     deleted_at = Column(DateTime, default=datetime.now())

#     class Config:
#         orm_mode = True
