import fastapi,os,sys
from dotenv import load_dotenv
from pymongo import MongoClient
import traceback

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from uvicorn import run as app_run

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,UploadFile,File,Request
from uvicorn import run as run_app
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME,DATA_INGESTION_COLLECTION_NAME
import certifi
from networksecurity.utils.ml_utils.model.estimator import NetoworkModel
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")
ca = certifi.where()
load_dotenv()
monogo_db_uri = os.getenv('MONGO_DB_URI')
client = MongoClient(monogo_db_uri,tlsCAFile =ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)


@app.get('/',tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response('Training is Successful')
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
@app.post("/predict")
async def predict_route(request:Request,file:UploadFile=File(...)):
    try:
            df = pd.read_csv(file.file)
            preprocessor_obj = load_object('final_model/preprocessor.pkl')
            model_obj = load_object('final_model/model.pkl')
            print(df)
            network_model_obj =  NetoworkModel(preprocessor=preprocessor_obj,model=model_obj)
            y_pred = network_model_obj.predict(df)
            print(y_pred)
            df['prediced_column'] = y_pred
            print(df['prediced_column'])
            output_file_path = os.path.dirname('predicted_output/output.csv')
            os.makedirs(output_file_path,exist_ok=True)
            df.to_csv('predicted_output/output.csv',index=False,header=True)
            table_html = df.to_html(classes="table table-striped")
            context = {
                 "request":request,"table":table_html
            }
            template = templates.get_template("table.html")
            rendered_html=template.render(context)
            with open("predicted_output/output.html","w",encoding="utf-8") as f:
                 f.write(rendered_html)
            return templates.TemplateResponse(request=request,name="table.html",context={"table":table_html})
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)