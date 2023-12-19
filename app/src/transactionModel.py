import joblib
from pathlib import Path

class TransactionModel:
    '''
    The class is used to point the application to the trained model.
    The class will load the trained_model.pkl file placed in the model folder in the application

    '''
    project_path = Path(__file__).resolve().parent
    path = project_path / "machineLearningModel" / "trained_model.pkl"
    
    model = joblib.load(path)