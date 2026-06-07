import yaml,sys,os
import numpy as np
import pickle
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score


def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,'rb') as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def write_yaml_file(path:str,content:object,replace:bool=False):
    try:
        if replace:
            if os.path.exists(path):
                os.remove(path)
        os.makedirs(os.path.dirname(path),exist_ok=True)
        with open(path,'w') as f:
            yaml.dump(content,f)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_numpy_array_data(file_path:str,array:np.array):
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as f:
            np.save(f,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def save_pickle_file(content:object,file_path:str):
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as f:
            pickle.dump(content,f)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def load_object(file_path:str):
    try:
        with open(file_path,'rb') as f:
            return pickle.load(f)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def load_numpy_array(file_path:str):
    try:
        with open(file_path,'rb') as f:
            return np.load(f)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def evaluate_model(x_train,y_train,x_test,y_test,params,models) -> dict:
    try:
        model_report = {}
        model_params = {}
        for i in range(len(models)):
            model_name = list(models.keys())[i]
            model = list(models.values())[i]
            parameters = params[model_name]
            rscv = RandomizedSearchCV(estimator=model,param_distributions=parameters,cv=5,n_iter=10,scoring='accuracy')
            rscv.fit(x_train,y_train)
            model.set_params(**rscv.best_params_)
            model.fit(x_train,y_train)
            y_pred = model.predict(x_test)
            model_report[model_name] = accuracy_score(y_true=y_test,y_pred=y_pred)
            model_params[model_name] = rscv.best_params_
        return model_report,model_params
    except Exception as e:
        raise NetworkSecurityException(e,sys)
