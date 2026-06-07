import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS,TARGET_COLUMN
from networksecurity.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_pickle_file
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class DataTransformation:
    def __init__(self,dataValidatioArtifact:DataValidationArtifact,dataTransformationConfig:DataTransformationConfig):
        try:
            self.dataValidatioArtifact =dataValidatioArtifact
            self.dataTransformationConfig = dataTransformationConfig
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def read_csv_file(file_path:str) -> pd.DataFrame:
        try:
            logging.info("Reading the validated csv files")
            dataframe = pd.read_csv(file_path)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        try:
            logging.info('Implementing the KNN Imputer')
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocessor:Pipeline = Pipeline([('imputer',imputer)])
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
                train_df = DataTransformation.read_csv_file(self.dataValidatioArtifact.valid_train_file_path)
                test_df = DataTransformation.read_csv_file(self.dataValidatioArtifact.valid_test_file_path)
                input_train_df = train_df.iloc[:,:-1]
                output_train_df = train_df.iloc[:,-1].replace(-1,0)
                input_test_df = test_df.iloc[:,:-1]
                output_test_df = test_df.iloc[:,-1].replace(-1,0)
                transformer_obj = self.get_data_transformer_object()
                transformed_train_data = transformer_obj.fit_transform(input_train_df)
                transformed_test_data = transformer_obj.transform(input_test_df)
                logging.info("Data Transformation Completed")
                final_train_array = np.c_[transformed_train_data,np.array(output_train_df)]
                final_test_array = np.c_[transformed_test_data,np.array(output_test_df)]
                save_numpy_array_data(self.dataTransformationConfig.transormed_train_file_path,final_train_array)
                save_numpy_array_data(self.dataTransformationConfig.transormed_test_file_path,final_test_array)
                save_pickle_file(transformer_obj,self.dataTransformationConfig.transforrmed_object_file_path)
                logging.info("Saving Transformed Data and transformer object")
                dataTransformatioArtifact = DataTransformationArtifact(self.dataTransformationConfig.transormed_train_file_path,self.dataTransformationConfig.transormed_test_file_path,self.dataTransformationConfig.transforrmed_object_file_path)
                return dataTransformatioArtifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        



