from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from networksecurity.logging.logger import logging

trainingPipelineConfig = TrainingPipelineConfig()
logging.info('Calling Training Pipeline Config')
dataIngestionConfig = DataIngestionConfig(trainingPipelineConfig)
logging.info('Calling Data Ingestion Config')
dataIngestion = DataIngestion(dataIngestionConfig)
output = dataIngestion.initiate_data_ingestion()
logging.info(f'Training Data is stored at {output.train_file_path}')
logging.info(f'Test Data is stored at {output.test_file_path}')
logging.info('Calling Data Validation Config')
dataValidationConfig = DataValidationConfig(trainingPipelineConfig)
logging.info('Calling Data Validation')
dataValidation = DataValidation(dataValidationConfig,dataIngestionArtifact=output)
logging.info('Extracting Validated Data')
output2 = dataValidation.initiate_data_validation()
logging.info('Data Transformation Begins')
dataTransformationConfig = DataTransformationConfig(trainingPipelineConfig)
dataTransformation = DataTransformation(dataValidatioArtifact=output2,dataTransformationConfig=dataTransformationConfig)
output3 = dataTransformation.initiate_data_transformation()
logging.info("Model Training Started")
modelTrainerConfig = ModelTrainerConfig(trainerPipelineConfig=trainingPipelineConfig)
modelTrainer = ModelTrainer(modelTrainerConfig=modelTrainerConfig,dataTransformerArtifact=output3)
output4 = modelTrainer.initiate_model_trainer()
print(output4)





