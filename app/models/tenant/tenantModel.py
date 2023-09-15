# # from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
# from sqlalchemy.orm import relationship
# from app.libs.psqlDBClient import Base
# from app.utills.helper import generate_aplhanum_random
# from sqlalchemy import Enum
# from datetime import datetime, timedelta
# from app.schemas.globalSchemas import userStatusEnum
# from app.schemas.admin.adminUserSchema import adminRoleEnum

# class TenantTemp(Base):
#     __tablename__ = 'tenantTemp'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     company = Column(String, nullable=False)
#     sortname = Column(String, nullable=False)
#     email = Column(String, unique=True, nullable=False)
#     mobile = Column(String, nullable=False, unique=True)
#     password = Column(String, nullable=False)
#     profilePic = Column(String, nullable=True)
#     mfa = Column(Boolean, nullable=False, default=False)
#     Tfa = Column(Boolean, nullable=False, default=False)
#     status = Column(Enum(userStatusEnum), nullable=False, default=userStatusEnum.active)
#     mfaSecretCode = Column(String, nullable=True)
#     role= Column(Enum(adminRoleEnum), nullable=False, default=adminRoleEnum.moderator)
#     mobileOtp = Column(String, nullable=False, default=generate_aplhanum_random(6))
#     mobileOtpCreatedAt = Column(DateTime, nullable=False, default = datetime.now())
#     isMobileVerified = Column(Boolean, nullable=False, default=False)
#     emailOtp = Column(String, nullable=False, default=generate_aplhanum_random(6))
#     emailOtpCreatedAt = Column(DateTime, nullable=False, default = datetime.now() )
#     isEmailVerified = Column(Boolean, nullable=False, default=False)
#     created_at = Column(DateTime, default=datetime.now())
#     updated_at = Column(DateTime)
#     deleted_at = Column(DateTime)

#     class Config:
#         orm_mode = True



# class TenantUser(Base):
#     __tablename__ = 'tenantUser'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     company = Column(String, nullable=False)
#     sortname = Column(String, nullable=False)
#     email = Column(String, unique=True, nullable=False)
#     mobile = Column(String, nullable=False, unique=True)
#     password = Column(String, nullable=False)
#     profilePic = Column(String, nullable=True)
#     mfa = Column(Boolean, nullable=False, default=False)
#     Tfa = Column(Boolean, nullable=False, default=False)
#     status = Column(Enum(userStatusEnum), nullable=False, default=userStatusEnum.active)
#     mfaSecretCode = Column(String, nullable=True)
#     role= Column(Enum(adminRoleEnum), nullable=False, default=adminRoleEnum.moderator)
#     mobileOtp = Column(String, nullable=True, default=generate_aplhanum_random(6))
#     mobileOtpCreatedAt = Column(DateTime, nullable=False, default = datetime.now())
#     isMobileVerified = Column(Boolean, nullable=False, default=False)
#     emailOtp = Column(String, nullable=False, default=generate_aplhanum_random(6))
#     emailOtpCreatedAt = Column(DateTime, nullable=False, default = datetime.now())
#     subscriptionId = Column(Integer, nullable=True)
#     isEmailVerified = Column(Boolean, nullable=False, default=False)
#     created_at = Column(DateTime, default=datetime.now())
#     updated_at = Column(DateTime)
#     deleted_at = Column(DateTime)
    
    
# class TenantWorkspace(Base):
#     __tablename__ = 'tenantWorkspace'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     color = Column(String, nullable=True)
#     image = Column(String, nullable=True)
#     status = Column(Enum(userStatusEnum), nullable=False, default=userStatusEnum.active)
#     created_by = Column(Integer, ForeignKey('tenantUser.id'), nullable=False)
#     created_at = Column(DateTime, default=datetime.now())
#     updated_at = Column(DateTime)
#     deleted_at = Column(DateTime)    
    
    
# class Sponser(Base):
#     __tablename__ = 'sponser'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     website = Column(String, nullable=False)
#     logo = Column(String, nullable=False)
    
    
    
# class Skills(Base):
#     __tablename__ = 'skills'
#     id = Column(Integer, primary_key=True)
#     skill = Column(String, nullable=False)
#     parent = Column(String, nullable=True)
#     logo = Column(String, nullable=True)
#     description = Column(String, nullable=True)        



# class EmailTemplate(Base):
#     __tablename__ = 'emailTemplate'
#     id = Column(Integer, primary_key=True)
#     templateType = Column(String, nullable=False)
#     templateName = Column(String, nullable=True)
#     templateContent = Column(String, nullable=True)
#     created_at = Column(DateTime, default=datetime.now())
#     created_by = Column(Integer, ForeignKey('tenantUser.id'), nullable=False)
#     status= Column(Enum(userStatusEnum), nullable=False, default=userStatusEnum.active)
#     visibility = Column(Boolean, nullable=False, default=False)
    
    
# class Uses(Base):
#     __tablename__ = 'uses'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     credits = Column(Integer, nullable=False)
#     duration= Column(Integer, nullable=False)
     
    
    

        

    
             
        
        
        
