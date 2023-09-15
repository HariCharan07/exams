from app.app import adminApp
from app.routes import tenantDashboardRouter as tdr
from fastapi import  UploadFile, File,Depends
from app.libs.authJWT import *
import shutil
import os
import cv2
from sqlalchemy.orm import Session
from app.routes import getTenantInfo
from app.libs.awsMods import generate_upload_url


class fileNameSchema(BaseModel):
    filename: str   
    
class ImageFolderSchema(BaseModel):
    folder_path: str

class VideoFileSchema(BaseModel):
    file_path: str  


@adminApp.post("/upload-image-user-screen/", tags=["proctoring"])
async def upload_image(image: fileNameSchema = File(...),Authorize: AuthJWT = Depends()):
    try:
        claims=Authorize.get_raw_jwt()
        tenant="stack"
        assessment=claims['assessmentId']
        student=claims['studentId']
        # tenant=claims['tenant']
        # Create a new folder named "upload" if it doesn't exist
        path="/home/ubuntu/{0}/{1}/{2}".format(tenant,assessment,student)
        if not os.path.exists(path):
            os.makedirs(path)
        
        # Save the uploaded image to the "upload" folder
        with open(path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        
        return {"status_code": 200,
                "message": "Image uploaded successfully",
                "filename": image.filename}
    except Exception as e:
        return {"status_code": 500,
                "message": "Error uploading image",
                "error": str(e)}   
        
        
        
        
@adminApp.post("/upload-image-user-face/", tags=["proctoring"])
async def upload_image(image: fileNameSchema = File(...),Authorize: AuthJWT = Depends()):
    try:
        claims=Authorize.get_raw_jwt()
        tenant="stack"
        assessment=claims['assessmentId']
        student=claims['studentId']
        path="/home/ubuntu/{0}/{1}/{2}".format(tenant,assessment,student)
        # Create a new folder named "upload" if it doesn't exist
        if not os.path.exists(path):
            os.makedirs(path)
        
        # Save the uploaded image to the "upload" folder
        with open(f"/home/ubuntu/tenant1/assessment2/userface1/{image.filename}.".format(path), "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # video_maker(image_folder=ImageFolderSchema(folder_path="upload/tenant1/assessment2/userface1"))
        return {"status_code": 200,
                "message": "Image uploaded successfully",
                "filename": image.filename}
    except Exception as e:
        return {"status_code": 500,
                "message": "Error uploading image",
                "error": str(e)}          




@adminApp.post('/imageToVideo', response_model=VideoFileSchema, tags=["proctoring"])
async def video_maker(image_folder: ImageFolderSchema):
    folder_path = image_folder.folder_path
    video_name = os.path.join(folder_path, 'video.avi')
    
    if os.path.exists(video_name):
        return {"file_path": video_name, "message": "Video already exists"}

    if not os.path.exists(folder_path):
        return {"file_path": "", "message": "Image folder does not exist"}

    images = [img for img in os.listdir(folder_path) if img.endswith('.png')]
    if not images:
        return {"file_path": "", "message": "No PNG images found in the folder"}

    frame = cv2.imread(os.path.join(folder_path, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 1, (width, height))
    for image in images:
        video.write(cv2.imread(os.path.join(folder_path, image)))
    
    video.release()

    if os.path.exists(video_name):
        return {"file_path": video_name, "message": "Video created successfully"}
    else:
        return {"file_path": "", "message": "Error creating video file"}
    
    
    
@tdr.post('/videoUrl')
async def test(filename: fileNameSchema,Authorize: AuthJWT = Depends()):  
    claims=Authorize.get_raw_jwt()
    tenant="stack"
    assessment="assessment2"
    student="userScreen1"
    path="{0}/{1}/{2}/".format(tenant,assessment,student) + filename.filename
    return generate_upload_url(path)    
    
    
@adminApp.post('/imageUrlScreen')
async def test(filename: fileNameSchema):  
    # claims=Authorize.get_raw_jwt()
    tenant="stack"
    # assessment=claims['assessmentId']
    # student=claims['studentId']
    assessment="assessment2"
    student="userScreen1"
    path="{0}/{1}/{2}/".format(tenant,assessment,student) + filename.filename
    return generate_upload_url(path)    
    
    
@adminApp.post('/imageUrlFace')
async def test(filename: fileNameSchema):
    # claims=Authorize.get_raw_jwt()
    tenant="stack"
    # assessment=claims['assessmentId']
    # student=claims['studentId']  
    assessment="assessment2"
    student="userFace1"
    path="{0}/{1}/{2}/".format(tenant,assessment,student) + filename.filename
    return generate_upload_url(path)     


@adminApp.post('/newimageToVideo', response_model=VideoFileSchema, tags=["proctoring"])
async def video_maker(folde: str):
    folder_path = folde
    video_name = os.path.join(folder_path, 'video.avi')

    if not os.path.exists(folder_path):
        return {"file_path": "path not found", "message": "Image folder does not exist"}

    images = [img for img in os.listdir(folder_path) if img.endswith('.png')]
    if not images:
        return {"file_path": "Hello", "message": "No PNG images found in the folder"}

    frame = cv2.imread(os.path.join(folder_path, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 1, (width, height))
    for image in images:
        video.write(cv2.imread(os.path.join(folder_path, image)))
    
    video.release()

    if os.path.exists(video_name):
        return {"file_path": video_name,
                "message": "Video created successfully"}
    else:
        return {"file_path": "", "message": "Error creating video file"}
