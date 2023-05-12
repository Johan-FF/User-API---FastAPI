from config.database import Base
from sqlalchemy import Column, Integer, String

class UserModel(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    nickname = Column(String)
    email = Column(String)
    password = Column(String)

    def update( self, **kwargs ):
        for key, value in kwargs.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)