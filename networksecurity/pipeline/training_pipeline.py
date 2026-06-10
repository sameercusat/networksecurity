from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.cloud.s3_syncer import S3sync
from networksecurity.constant.training_pipeline import TRAINING_BUCKET_NAME

class TrainingPipeline:
    def __init__(self):
        self.trainingPipelineConfig = TrainingPipelineConfig()
        self.s3_sync = S3sync()
    
    def start_data_ingestion(self):
        try:
            logging.info('Data Ingestion Started')
            self.data_ingestion_config = DataIngestionConfig(trainPipelineConfig=self.trainingPipelineConfig)
            dataIngestion = DataIngestion(dataIngestionConfig=self.data_ingestion_config)
            dataIngestionArtifact:DataIngestionArtifact = dataIngestion.initiate_data_ingestion()
            logging.info(f'Data Ingestion Completed with artifacts : {dataIngestionArtifact}')
            return dataIngestionArtifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_data_validation(self,dataIngestionArtifact:DataIngestionArtifact):
        try:
            logging.info('Data Validation Started')
            self.dataValidationConfig = DataValidationConfig(self.trainingPipelineConfig)
            dataValidation = DataValidation(dataValidationConfig=self.dataValidationConfig,dataIngestionArtifact=dataIngestionArtifact)
            dataValidationArtifact = dataValidation.initiate_data_validation()
            logging.info(f'Data Validation Completed with artifact: {dataValidationArtifact}')
            return dataValidationArtifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_transformation(self,dataValidationArtifact:DataValidationArtifact):
        try:
            logging.info('Data Transformation Started')
            self.dataTransformationConfig = DataTransformationConfig(self.trainingPipelineConfig)
            dataTransformation = DataTransformation(dataTransformationConfig=self.dataTransformationConfig,dataValidatioArtifact=dataValidationArtifact)
            dataTransformationArtifact = dataTransformation.initiate_data_transformation()
            logging.info(f'Data Transformation Ended with artifact: {dataTransformationArtifact}')
            return dataTransformationArtifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_model_training(self,dataTransformationArtifact:DataTransformationArtifact):
        try:
            modelTrainerConfig = ModelTrainerConfig(self.trainingPipelineConfig)
            modelTrainer = ModelTrainer(modelTrainerConfig=modelTrainerConfig,dataTransformerArtifact=dataTransformationArtifact)
            modelTraierArtifact:ModelTrainerArtifact = modelTrainer.initiate_model_trainer()
            return modelTraierArtifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.trainingPipelineConfig.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.trainingPipelineConfig.artifact_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.trainingPipelineConfig.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.trainingPipelineConfig.model_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
        
    def run_pipeline(self):
        try:
            dataIngestionArtifact = self.start_data_ingestion()
            dataValidationArtifact = self.start_data_validation(dataIngestionArtifact=dataIngestionArtifact)
            dataTranformationArtifact = self.start_data_transformation(dataValidationArtifact=dataValidationArtifact)
            modelTrainerArtifact = self.start_model_training(dataTransformationArtifact=dataTranformationArtifact)
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
            return modelTrainerArtifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)