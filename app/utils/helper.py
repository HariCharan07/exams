# function to encrypt and decrypt data using AES

# from Crypto.Cipher import AES
# from Crypto import Random
import base64
import hashlib
# from cryptography.fernet import Fernet
import string
import secrets
import os
# import pandas as pd
# import cv2
from app.libs.mongoclient import mongoDBClient
import uuid


def generate_aplhanum_random(num):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(num))
    return password

def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]



# def encrypt(key, data):
#     fernet = Fernet(key)
#     encMessage = fernet.encrypt(data.encode())
#     return encMessage

# def decrypt(key, data):
#     fernet = Fernet(key)
#     decMessage = fernet.decrypt(data).decode()
#     return decMessage


# # function to convert password into sha1 hash
# def sha1_hash(password):
#     return hashlib.sha1(password.encode('utf-8')).hexdigest()

# # function to get ip address of the client
# def get_ip_address(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

# # function to get user agent of the client
# def get_user_agent(request):
#     return request.META.get('HTTP_USER_AGENT')

# #function to check device type of the client (mobile or desktop)
# def is_mobile(request):
#     if request.user_agent.is_mobile:
#         return True
#     else:
#         return False
    

    
    
# from enum import Enum

# def programmingLanguage(code:Enum):
#     lang1="python",
#     lang2="java",
#     lang3="javascript",
#     lang4="C++"    
    
    
    
# def checkStringinfile(filename, stringToSearch):
#     # Open the file in read only mode
#     with open(filename, 'r') as read_obj:
#         # Read all lines in the file one by one
#         for line in read_obj:
#             # For each line, check if line contains the string
#             if stringToSearch in line:
#                 return True
#     return False



# def addStringtofile(filename, stringToSearch):
#     # Open the file in read only mode
#     with open(filename, 'a') as read_obj:
#         # Read all lines in the file one by one
#         read_obj.write('\n' + stringToSearch)
#         return True



# def encrypt(key, data):
#     fernet = Fernet(key)
#     encMessage = fernet.encrypt(data.encode())
#     return encMessage

# def decrypt(key, data):
#     fernet = Fernet(key)
#     decMessage = fernet.decrypt(data).decode()
#     return decMessage


# def serializeDict(a) -> dict:
#     return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

# def serializeList(entity) -> list:
#     return [serializeDict(a) for a in entity]




# def video_maker(folde: str):
#     folder_path = folde
#     video_name = os.path.join(folder_path, 'video.avi')

#     if not os.path.exists(folder_path):
#         return {"file_path": "path not found", "message": "Image folder does not exist"}

#     images = [img for img in os.listdir(folder_path) if img.endswith('.png')]
#     if not images:
#         return {"file_path": "Hello", "message": "No PNG images found in the folder"}

#     frame = cv2.imread(os.path.join(folder_path, images[0]))
#     height, width, layers = frame.shape

#     video = cv2.VideoWriter(video_name, 0, 1, (width, height))
#     for image in images:
#         video.write(cv2.imread(os.path.join(folder_path, image)))
    
#     video.release()

#     if os.path.exists(video_name):
#         return {"file_path": video_name,
#                 "message": "Video created successfully"}
#     else:
#         return {"file_path": "", "message": "Error creating video file"}


# def process_file(file,workspace_id,assessment_id,tenant_id,sectionId, sortname=None,user_id=None):
#     unique_id = uuid.uuid4()

#     if file.filename.endswith('.csv'):
#         # Read CSV file into a DataFrame
#         df = pd.read_csv(file.file)
#     elif file.filename.endswith('.xlsx') or file.filename.endswith('.xlsx'):
#         # Read Excel file into a DataFrame
#         df = pd.read_excel(file.file)


#         # Print the unique ID
#         df['tenant_id']=tenant_id
#         df['workspace_id']=workspace_id
#         df['assessment_id']=int(assessment_id)
#         df['sectionId']=sectionId
#         df['tenant_sortname']=sortname
#         df['user_id']=user_id
#         df['imgUrl']=None
#         df['selectedOptions'] = df['selectedOptions'].str.split(',').apply(lambda x: [i for i in x] if isinstance(x, list) else [])
#     else:
#         raise ValueError('Unsupported file format. Only CSV and Excel files are supported.')

#     # Convert DataFrame to dictionary records
#     records = df.to_dict(orient='records')
#     for i in records:
#         i['id']=str(uuid.uuid4())
#     print(records)
#     return records
    
#     # Save records to MongoDB
    
    
    
    
# import openpyxl
# from fastapi import UploadFile
# from tempfile import NamedTemporaryFile

# async def process_excel_file(file,workspace_id,assessment_id,sectionId, sortname):
#     temp_file = NamedTemporaryFile(delete=False)
#     temp_file.write(await file.read())
#     temp_file.close()

#     workbook = openpyxl.load_workbook(temp_file.name)

#     # Process the workbook as needed

#     # Remove the temporary file
#     temp_file.unlink()

#     # Continue with your FastAPI logic
