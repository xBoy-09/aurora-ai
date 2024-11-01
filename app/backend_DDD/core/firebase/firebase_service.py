import firebase_admin 
from firebase_admin import auth



def create_user(
    email: str,
    email_verified: bool,
    password: str,
    full_name: str,
    disabled: bool,
) -> str:
    user_record = auth.create_user(        
        email=email,
        email_verified=email_verified,
        password=password,
        display_name=full_name,
        disabled=disabled,
    )

    return user_record.uid


def update_password_and_name(firebase_uid: str, new_password: str, new_full_name: str):
    auth.update_user(
        uid=firebase_uid,
        password=new_password,
        display_name=new_full_name,
    )


def update_password(firebase_uid: str, new_password: str):
    auth.update_user(
        uid=firebase_uid,
        password=new_password,
    )


def get_user_email(email: str) -> str:
    user_record = auth.get_user_by_email(email=email)

    return user_record.uid
