from dataclasses import dataclass
from abc import ABC, abstractmethod
from app.backend_DDD.core.firebase import firebase_service as fb_svc

@dataclass
class AbstractFirebaseService(ABC):
    @abstractmethod
    def create_user(
        self, email: str, password: str, full_name: str
    ) -> str:
        pass

    @abstractmethod
    def reset_password(self, firebase_uid: str, new_password: str):
        pass

    @abstractmethod
    def update_password_and_name(self, firebase_uid: str, new_password: str, new_full_name: str):
        pass

    @abstractmethod
    def get_user_email(self, email: str) -> str:
        pass


@dataclass
class FakeFirebaseService(AbstractFirebaseService):
    user_exists: bool = False

    def set_user_exists(self, user_exists: bool):
        self.user_exists = user_exists

    def create_user(
        self, email: str, password: str, full_name: str, 
    ):
        if self.user_exists:
            raise Exception("User already exists")
        return "24100300"

    def update_password_and_name(self, firebase_uid: str, new_password: str, new_full_name: str)-> str:
        pass

    def get_user_email(self, email: str) -> str:
        return ""

    def reset_password(self, firebase_uid: str, new_password: str) -> str:
        return 


class FirebaseService(AbstractFirebaseService):
    def create_user(
        self, email: str, password: str, full_name: str
    ) -> str:
        return fb_svc.create_user(
            email=email,
            email_verified=False,
            password=password,
            full_name=full_name,
            disabled=False,
        )

    def update_password_and_name(self, firebase_uid: str, new_password: str, new_full_name: str):
        fb_svc.update_password_and_name(
            firebase_uid=firebase_uid,
            new_password=new_password,
            new_full_name=new_full_name,
        )

    def reset_password(self, firebase_uid: str, new_password: str):
        # TODO: Check if the old pwd is the same as the old password
        fb_svc.update_password(
            firebase_uid=firebase_uid,
            new_password=new_password,
        )

    def get_user_email(self, email: str) -> str:
        return fb_svc.get_user_email(email=email)