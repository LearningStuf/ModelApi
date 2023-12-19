from pydantic import BaseModel, ConfigDict

class AuthDetails(BaseModel):
    '''
    This class denotes the json body of the user registration and user login request.
    '''
  
    model_config = ConfigDict(extra='forbid')
    username: str
    password: str
    
