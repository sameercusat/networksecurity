from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from networksecurity.logging.logger import logging

trainingPipelineConfig = TrainingPipelineConfig()
logging.info('Calling Training Pipeline Config')
dataIngestionConfig = DataIngestionConfig(trainingPipelineConfig)
logging.info('Calling Data Ingestion Config')
dataIngestion = DataIngestion(dataIngestionConfig)
output = dataIngestion.initiate_data_ingestion()
logging.info(f'Training Data is stored at {output.train_file_path}')
logging.info(f'Test Data is stored at {output.test_file_path}')


