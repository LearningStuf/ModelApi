from pydantic import BaseModel

class PredictionResponse(BaseModel):
    '''
    This class denotes the json body response that the /bot-score endpoint will be returning back on a successful api call.
    '''
    p_bot: float
    bot: int