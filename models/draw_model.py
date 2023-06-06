from config.database import Base
from sqlalchemy import Column, Integer, String

class DrawModel(Base):
    __tablename__="draws"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    details = Column(String)
    id_owner = Column(Integer)

    def update( self, **kwargs ):
        for key, value in kwargs.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)