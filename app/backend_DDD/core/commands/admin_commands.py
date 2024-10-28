from firebase_admin import exceptions, auth
from app.backend_DDD.core.classes import authentication as auth_class
from app.backend_DDD.core.database.database_api_queries import DatabaseManager as db_man
from app.backend_DDD.core.gpt.gpt_assistant_functions import GptAssistant as gpt_asst



def get_assistants(
        db: db_man,
):
    try:
        assistants_db = db.admin.view_all_assistants()
        return assistants_db
    except Exception as e:
        print(f"Error getting assistants: {e}")
        return e
    

def get_users(
        db: db_man,
):
    try:
        users_db = db.admin.view_all_users()
        return users_db
    except Exception as e:
        print(f"Error getting users: {e}")
        return e
    

def get_user_details(
        db: db_man,
        user_id: str,
):
    try:
        user = db.admin.get_user(user_id)
        return user
    except Exception as e:
        print(f"Error getting user details: {e}")
        return e