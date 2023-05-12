from models.user_model import UserModel
from utils.cryp_manager import generate_encrypt
from schemas.user_schema import UserSchema

class UserService():
    def __init__(self, db):
        self.db = db

    def get_users(self):
        return self.db.query(UserModel).all()

    def get_user(self, id):
        result = self.db.query(UserModel).filter(UserModel.id == id).one_or_none()
        return result

    def get_user_by_nickname(self, nickname:str):
        result = self.db.query(UserModel).filter(UserModel.nickname == nickname).all()
        return result

    def get_user_by_email(self, email:str):
        result = self.db.query(UserModel).filter(UserModel.email == email).one_or_none()
        return result

    def create_user(self, user: UserSchema):
        exists = self.get_user_by_email(user.email)
        if not exists:
            user.password = generate_encrypt(user.password)
            new_user = UserModel(**user.dict())
            self.db.add(new_user)
            self.db.commit()
            return True
        return False

    def update_user(self, id: int, user: UserSchema):
        user_found = self.db.query(UserModel).filter(UserModel.id == id).one_or_none()
        if not user_found:
            return False
        user.password = generate_encrypt(user.password)
        update_user = user.dict()
        user_found.update( **update_user )
        self.db.commit()
        return True

    def delete_user(self, id):
        user_to_delete = self.db.query(UserModel).filter(UserModel.id == id).one_or_none()
        if not user_to_delete:
            return False
        self.db.delete(user_to_delete)
        self.db.commit()
        return True