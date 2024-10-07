from firebase_admin import exceptions, auth
from app.backend_DDD.core.classes import authentication as auth_class
from app.backend_DDD.core.database.database_api_queries import DatabaseManager as db_man



def create_user(
    email: str,
    password: str,
    full_name: str,
    fb_svc: auth_class.AbstractFirebaseService,
    db_man: db_man,
) -> str:
    user_already_exists = False

    try:
        firebase_uid = fb_svc.create_user(
            email=email,
            password=password,
            full_name=full_name,
        )

        return firebase_uid
    except Exception as e:
        if isinstance(e, exceptions.AlreadyExistsError):
            user_already_exists = True
        else:
            print(f"Error creating user: {e}")
            return e
        
    if not user_already_exists:
        # create user instance in db
        user_id = db_man.create_user(user_name=full_name, uid=firebase_uid)
        return user_id
    else:
        firebase_uid = fb_svc.get_user(email=email)
        db_user_id = db_man.get_user(user_id=firebase_uid)

        if not db_user_id:
            # create user instance in db
            user_id = db_man.create_user(user_name=full_name, uid=firebase_uid)
            return user_id


    
