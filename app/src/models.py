from sqlalchemy import Column, String
from databaseConfig.database import Base

class Users(Base):
    '''
    This class denotes the structure of users table in our sqlite db.
    The class has the desctiption of what the table coloums will be, the primary key etc.
    '''
    __tablename__ = "users"
    username =Column(String,primary_key=True,index=True)
    password = Column(String)