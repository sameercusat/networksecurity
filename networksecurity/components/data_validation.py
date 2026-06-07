from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifact
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constant.training_pipeline import SCHEMA_FILE__PATH
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
import sys,os
import pandas as pd
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self,dataValidationConfig:DataValidationConfig,dataIngestionArtifact:DataIngestionArtifact):
        try:
            self.dataValidationConfig = dataValidationConfig
            self.dataIngestionArtifact = dataIngestionArtifact
            self.schema_config = read_yaml_file(SCHEMA_FILE__PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_file(file_path)->pd.DataFrame:
        logging.info('Reading CSV File')
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame) -> bool:
        logging.info('Validate Number of columns in Schema and DataFrame')
        try:
            schema_columns = len(self.schema_config['columns'])
            dataframe_columns = len(dataframe.columns)
            if schema_columns == dataframe_columns:
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def detect_dataset_drift(self,base_df,current_df,threshold = 0.05) ->bool:
        logging.info('Calculate Dataset Drift')
        try:
            report ={}
            status = True
            for col in base_df.columns:
                is_same_dist = ks_2samp(base_df[col],current_df[col])
                if is_same_dist.pvalue >= threshold:
                    is_found = False
                else:
                    logging.error(f'Failed for column : {col} and PValue is {is_same_dist.pvalue}')
                    is_found= True
                    status = False
                report.update({col:{'pvalue':float(is_same_dist.pvalue),'drift_status':is_found}})
            write_yaml_file(content=report,path=self.dataValidationConfig.data_validation_drift_report_path)
            return status
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    
    def initiate_data_validation(self):
        try:
                train_file_path = self.dataIngestionArtifact.train_file_path
                train_df = self.read_file(train_file_path)
                test_file_path = self.dataIngestionArtifact.test_file_path
                test_df = self.read_file(test_file_path)
                status1 = self.validate_number_of_columns(train_df)
                status2 = self.validate_number_of_columns(test_df)
                base_df = self.schema_config
                if not status1:
                    error_msg = 'Train DataFrame does not contain all columns'
                    logging.error(error_msg)
                if not status2:
                    error_msg = 'Test DataFame does not contain all columns'
                    logging.error(error_msg)
                status3 = self.detect_dataset_drift(base_df=train_df,current_df=test_df)
                if not status3:
                    logging.error('Dataset Drift Report is Negative')
                if status1 and status2 and status3 :
                    logging.info('All status and validations are passed')
                    train_dir_file_path = os.path.dirname(self.dataValidationConfig.data_validation_valid_train_file_path)

                    os.makedirs(train_dir_file_path,exist_ok=True)
                    logging.info('Creating .csv file for Training Data')
                    train_df.to_csv(self.dataValidationConfig.data_validation_valid_train_file_path,header=True,index=False)
                    logging.info('Creating .csv file for Test DataFrame')
                    test_df.to_csv(self.dataValidationConfig.data_validation_valid_test_file_path,header=True,index=False)
                    dataValidationArtifact = DataValidationArtifact(
                        validation_status=status1 and status2 and status3,
                        valid_train_file_path = self.dataIngestionArtifact.train_file_path,
                        valid_test_file_path = self.dataIngestionArtifact.test_file_path,
                        invalid_train_file_path = None,
                        invalid_test_file_path= None,
                        drift_report_file_path= self.dataValidationConfig.data_validation_drift_report_path
                    )
                return dataValidationArtifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

        






