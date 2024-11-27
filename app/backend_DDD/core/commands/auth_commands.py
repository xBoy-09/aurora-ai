from firebase_admin import exceptions, auth
from app.backend_DDD.core.classes import authentication as auth_class
from app.backend_DDD.core.scripts.pdc_extract_menu_script import start_extracting_pdc_menu
from app.backend_DDD.core.database.database_api_queries import DatabaseManager as db_man



def create_user(
    email: str,
    password: str,
    full_name: str,
    fb_svc: auth_class.AbstractFirebaseService,
    db_man: db_man,
) -> str:
    user_already_exists = False

    # create user in firebase, if already exist in firebase then raise exception
    try:
        firebase_uid = fb_svc.create_user(
            email=email,
            password=password,
            full_name=full_name,
        )
    except Exception as e:
        if isinstance(e, exceptions.AlreadyExistsError):
            user_already_exists = True
        else:
            print(f"Error creating user: {e}")
            return e
        
    # if not in firebase, make one in db
    if not user_already_exists:
        # create user instance in db
        user_id = db_man.create_user(user_name=full_name, uid=firebase_uid, email=email)
        return user_id
    # if already in firebase, check if in db, if not make one in db
    else:
        firebase_uid = fb_svc.get_user(email=email)
        db_user_id = db_man.get_user_id(user_id=firebase_uid)

        if not db_user_id:
            # create user instance in db
            user_id = db_man.create_user(user_name=full_name, uid=firebase_uid)
            return user_id


def create_user_without_firebase(
    email: str,
    user_id: str,
    full_name: str,
    fb_svc: auth_class.AbstractFirebaseService,
    db_man: db_man,
):
    firebase_uid = fb_svc.get_user_email(email=email)
    if firebase_uid == user_id:
        user = db_man.get_user(user_id=user_id)
        if user:
            return user_id
        else:
            db_man.create_user(user_name=full_name, uid=firebase_uid, email=email)
        return firebase_uid
    else:
        raise Exception("User does not exists in firebase")
        


def get_user(
        uid:str,
        db_man: db_man,
) -> str:
    user = db_man.get_user(user_id=uid)
    user["user_setup"] = db_man.get_user_setup(user_id=uid)
    return user

def update_pdc_menu(
        db_man: db_man
):
    pdc_menu_data = start_extracting_pdc_menu()

    if pdc_menu_data:
        db_man.scripts.update_pdc_menu(pdc_menu_data)