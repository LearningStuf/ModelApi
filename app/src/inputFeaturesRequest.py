from pydantic import BaseModel,ConfigDict


class InputFeaturesRequest(BaseModel):
    '''
    The class will create the request json model for the input features.
    This is the structure of what the user will send as a post request
    to /bot-score endpoint.
    '''
    model_config = ConfigDict(extra='forbid')
    x1: float
    x2: float
