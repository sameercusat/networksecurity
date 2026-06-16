from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from dotenv import load_dotenv
import os
import pandas as pd
import sys
import numpy as np
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')


class DataIngestion:
    def __init__(self,dataIngestionConfig:DataIngestionConfig):
        try:
            self.dataIngestionConfig = dataIngestionConfig
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def import_data_mongodb(self):
        try:        
                database =self.dataIngestionConfig.database_name
                collection = self.dataIngestionConfig.collection_name
                print("DATABASE",database)
                print("collection",collection)
                print("URI",MONGODB_URI)
                self.mongo_client = MongoClient(MONGODB_URI)
                collections = self.mongo_client[database][collection]
                df = pd.DataFrame(list(collections.find()))
                if '_id' in df.columns.to_list():
                    df.drop(['_id'],inplace=True,axis=1)
                df.replace({'na':np.nan},inplace=True)
                logging.info('Data Fetched from Mongo DB and converted into Pandas DataFrame')
                return df
        except Exception as e:
             raise NetworkSecurityException(e,sys)
    
    def save_data_work_folder(self,dataframe:pd.DataFrame):
         try:
            path_for_work_dir = os.path.dirname(self.dataIngestionConfig.feature_store_file_path)
            os.makedirs(path_for_work_dir,exist_ok=True)
            dataframe.to_csv(self.dataIngestionConfig.feature_store_file_path,index=False,header=True)
            logging.info('Saving Original Data into .csv format in Working Directory')
            return dataframe

         except Exception as e:
              raise NetworkSecurityException(e,sys)
         
    def split_train_test(self,df:pd.DataFrame):
        try:
                train_data,test_data = train_test_split(df,test_size=self.dataIngestionConfig.train_test_split)
                ingester_path = os.path.dirname(self.dataIngestionConfig.training_file_path)
                os.makedirs(ingester_path,exist_ok=True)
                train_data.to_csv(self.dataIngestionConfig.training_file_path,index=False,header=True)
                test_data.to_csv(self.dataIngestionConfig.test_file_path,index=False,header=True)
                logging.info('Splitting data into train and test and saving them in Ingested Folder')
                return self.dataIngestionConfig.training_file_path,self.dataIngestionConfig.test_file_path

        except Exception as e:
             raise NetworkSecurityException(e,sys)
    
    def initiate_data_ingestion(self):
         try:
              logging.info('Data Ingestion Process Initiated')
              dataframe = self.import_data_mongodb()
              dataframe = self.save_data_work_folder(dataframe=dataframe)
              train_path,test_path = self.split_train_test(dataframe)
              dataIngestionArtifact = DataIngestionArtifact(train_path,test_path)
              return dataIngestionArtifact
         except Exception as e:
              raise NetworkSecurityException(e,sys)
    


         
    


