from app.libs.mongoCLient import mongoDBClient
from datetime import datetime

# Record user login time
def record_user_login(username):
    user_task_collection.update_one({"logsInfo": username}, {"$set": {"last_login": datetime.now()}}, upsert=True)

# Record user logout time
def record_user_logout(username):
    user_task_collection.update_one({"logsInfo": username}, {"$set": {"last_logout": datetime.now()}})

# Record user creation
def record_user_creation(username):
    user_task_collection.insert_one({"logsInfo": username, "created_at": datetime.now()})

# Record task creation
def record_task_creation(task_name, assigned_to):
    user_task_collection.insert_one({"task_name": task_name, "assigned_to": assigned_to, "created_at": datetime.now()})