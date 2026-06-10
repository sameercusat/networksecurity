from datetime import datetime
import os
from networksecurity.constant import training_pipeline
from datetime import datetime


class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime('%m_%d_%Y_%H_%M_%S')
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.model_dir = 'final_model'
        self.timestamp: str = timestamp

class DataIngestionConfig:
    def __init__(self,trainPipelineConfig:TrainingPipelineConfig):
        self.data_ingestion_dir:str = os.path.join(trainPipelineConfig.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME)
        self.feature_store_file_path:str = os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME)
        self.training_file_path:str = os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TRAIN_FILE_NAME)
        self.test_file_path:str = os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TEST_FILE_NAME)
        self.train_test_split = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.database_name= training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME

class DataValidationConfig:
    def __init__(self,trainPipelineConfig:TrainingPipelineConfig):
        self.data_validation_dir:str = os.path.join(trainPipelineConfig.artifact_dir,training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.data_validation_valid_dir:str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.data_validation_invalid_dir:str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.data_validation_valid_train_file_path:str = os.path.join(self.data_validation_valid_dir,training_pipeline.TRAIN_FILE_NAME)
        self.data_validation_valid_test_file_path:str = os.path.join(self.data_validation_valid_dir,training_pipeline.TEST_FILE_NAME)
        self.data_validation_invalid_train_file_path:str = os.path.join(self.data_validation_invalid_dir,training_pipeline.TRAIN_FILE_NAME)
        self.data_validation_invalid_test_file_path:str = os.path.join(self.data_validation_invalid_dir,training_pipeline.TEST_FILE_NAME)
        self.data_validation_drift_report_dir:str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR)
        self.data_validation_drift_report_path:str = os.path.join(self.data_validation_drift_report_dir,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)


class DataTransformationConfig:
    def __init__(self,trainingPipelineConfig:TrainingPipelineConfig):
        self.data_transformation_dir:str = os.path.join(trainingPipelineConfig.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.transormed_train_file_path:str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,training_pipeline.TRAIN_FILE_NAME.replace('csv','npy'))
        self.transormed_test_file_path:str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,training_pipeline.TEST_FILE_NAME.replace('csv','npy'))
        self.transforrmed_object_file_path:str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,training_pipeline.PREPROCESSING_OBJECT_FILE_NAME)
        


class ModelTrainerConfig:
    def __init__(self,trainerPipelineConfig:TrainingPipelineConfig):
        self.model_trainer_dir:str = os.path.join(trainerPipelineConfig.artifact_dir,training_pipeline.MODEL_TRAINER_DIR_NAME)
        self.model_trainer_trained_model_path:str = os.path.join(self.model_trainer_dir,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME)
        self.model_trainer_expected_score:float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.model_trainer_overfit_underfit_threshold:float = training_pipeline.MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD
        