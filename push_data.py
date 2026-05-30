import os
import json
from dotenv import load_dotenv
import certifi
import pandas as pd
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')


certifi.where()


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def csv_to_json(self,file_path):
        try:
            logging.info('Converting JSON TO CSV to save the data in MongoDB')
            df = pd.read_csv(file_path)
            df.reset_index(drop=True,inplace=True)
            records = list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            logging.error(f'Error occured in converting file from csv to json - {e}')
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            logging.info('Saving Data in MongoDB post coversion')
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = pymongo.MongoClient(MONGODB_URI)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            logging.error(f'Error in sending data to MongoDB -{e}')
            raise NetworkSecurityException(e,sys)
        

if __name__ == '__main__':
    net_sec_obj = NetworkDataExtract()
    file_path = r'Network_Data\phisingData.csv'
    records = net_sec_obj.csv_to_json(file_path=file_path)
    database = 'NET_SEC'
    collection = 'CSV_TO_JSON'
    no_records = net_sec_obj.insert_data_mongodb(database=database,collection=collection,records=records)
    print(no_records)