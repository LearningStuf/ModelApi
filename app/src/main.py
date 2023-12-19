import os
from fastapi import FastAPI,Request,Depends,exceptions
from src.predictionResponse import *
from src.inputFeaturesRequest import *
from src.transactionModel import *
from src.auth import *;
from src.userAuthRequest import *;
import time;
from src import models
from databaseConfig.database import engine, SessionLocal;
from sqlalchemy.orm import Session;
from sqlalchemy.exc import IntegrityError;
import logging.config
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from pathlib import Path

app = FastAPI()

auth_handler = AuthHandler()


# To create the db if it's not already present 
models.Base.metadata.create_all(bind=engine)

project_path = Path(__file__).resolve().parent.parent


path_config = project_path / "config"

load_dotenv(dotenv_path=path_config /".env")


#  loading the logging_config file
logging.config.fileConfig(path_config / "logging_config.ini")


    
custom_logger = logging.getLogger()






@app.exception_handler(exceptions.RequestValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    '''
    Middleware function to log any validation error the logger is set to Error
    '''
    endpoint = request.url.path
    custom_logger.error(f"Endpoint that cause the issue:  {endpoint}")
    custom_logger.error(f"Validation error occurred because: {exc.errors()}")
    return JSONResponse(content={"detail": exc.errors()}, status_code=422)



def get_db():
    '''
    Function will allow us to open and close a database connection subsequetly against an api call.
    '''
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close





@app.middleware("http")
async def add_process_time(request: Request, call_next):
    '''
    Function is a middleware, this will allow us to add functionality before a request is recieved on an endpoint and after
    the request has been committed.\n
    Currenlty utilizing this to log api processing time and give warnings if it crosses a certain threshold
    '''

    start_time = time.time()
    endpoint = request.url.path
    response = await call_next(request)
    process_time = (time.time() - start_time)/1000

    custom_logger.debug(f"Time to complete the reqeuest: {process_time} milliseconds")
    
    if process_time >  int(os.getenv("API_THRESHOLD")):
        
        custom_logger.critical(f"Endpoint that is causing the issue:  {endpoint}")
        custom_logger.critical(f"API is needs to be monitored processing time: {process_time}")

    return response




@app.post('/register', status_code=200)
def register(auth_details: AuthDetails,db: Session = Depends(get_db)):
    '''
    The api endpoint allows the user to successfuly register it self in the application.
    sending username and password in the Post request.
    Only registered user can utilize the login endpoint to generate authentication tokens
    to hit protected endpoints.
    '''
    
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    user_model = models.Users()
    user_model.username = auth_details.username
    user_model.password = hashed_password

    try:
        db.add(user_model)
        db.commit()
    except IntegrityError as e:
        db.rollback()  # Rollback the transaction to prevent partially inserted data
        custom_logger.error(f"on registering the user:{e}")
        raise HTTPException(status_code=400, detail="Username is not unique")
        
    return {"message": "User registered successfully"}




@app.post('/login')

def login(auth_details: AuthDetails, db: Session = Depends(get_db)):
    '''
    The api endpoint allows the user to login to the application. This will return the user a jwt token that will need to be
    part of the authorization header to call the protected endpoints. To call this endpoint successfully the client
    must have a registered user in the application using the /register endpoint.

    :param auth_details: The json request sent to the endpoint by the client

    '''



    custom_logger.debug(f"Request json recieved for /login endpoint: {auth_details.username}")

    user = db.query(models.Users).filter_by(username=auth_details.username).first()
   

    if (user is None) or (not auth_handler.verify_password(auth_details.password, user.password)):
        custom_logger.error("Invalid username and/or password")
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user.username)
    return { 'token': token }




@app.post("/bot-score")
def predict_model(input_features: InputFeaturesRequest) -> PredictionResponse:
    '''
    This is the unprotected bot-score prediction endpoint. The user can send a post request giving x1 and x2 with numeric values.
    The end point will return a json object back containing\n
    p_bot: The probability that the transaction was committed by a bot\n
    bot: The boolean value of 0 and 1 to determine whether the transcation was human initiated or bot initiated
    0 explains the transaction was human initiated and 1 means that the transaction was initiated by a bot.

    :param input_features: The Json request sent to the endpoint by the client.

    '''

    iput_features_array = [[input_features.x1,input_features.x2]]
    bot = TransactionModel.model.predict(iput_features_array)[0]
    p_bot = TransactionModel.model.predict_proba(iput_features_array)[0,1]
    responsedata = PredictionResponse(bot=bot,p_bot=p_bot)

    return responsedata



@app.post("/protected/bot-score", dependencies=[Depends(auth_handler.auth_wrapper)])
def predict_model(input_features: InputFeaturesRequest) -> PredictionResponse:
    '''
    The is the protected bot-score prediction endpoint. Before calling this enpoint the client needs to  call the
    /login endpoint to get the JWT token that needs to a part of the request header.\n
    The rest of the conventions that will be followed for this endpoint will be the same as /bot-score
    ## Sample Authorization request header:
    Authorization: Bearer "JWT token generated by /login" 
    
    '''

    iput_features_array = [[input_features.x1,input_features.x2]]
    bot = TransactionModel.model.predict(iput_features_array)[0]
    p_bot = TransactionModel.model.predict_proba(iput_features_array)[0,1]
    responsedata = PredictionResponse(bot=bot,p_bot=p_bot)

    return responsedata



@app.get("/health")
async def health_check():
    '''
    This endpoint can be used to check whether the application is up and running.
    '''
    # Perform custom health checks here
    return {"status": "ok"}





