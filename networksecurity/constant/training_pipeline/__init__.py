import os
import numpy as np


'''
defining common constants variables for training pipeline
'''

TARGET_COLUMN = "Result"
PIPELINE_NAME = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phisingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

PREPROCESSING_OBJECT_FILE_NAME:str = "preprocessing.pkl"


'''
Data Ingestion related Constants starts with DATA_INGESTION 
'''
 
DATA_INGESTION_COLLECTION_NAME:str = "CSV_TO_JSON"
DATA_INGESTION_DATABASE_NAME:str = "NET_SEC"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION:float = 0.2


DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "validated"
DATA_VALIDATION_INVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"

SCHEMA_FILE__PATH = os.path.join("data_schema","schema.yaml")

DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = "transormed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_obj"

DATA_TRANSFORMATION_IMPUTER_PARAMS:dict = {
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform"
}

'''MODEL TRAINER PARAMETERS'''

MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD:float = 0.05

TRAINING_BUCKET_NAME = 'networksecurity7890'
