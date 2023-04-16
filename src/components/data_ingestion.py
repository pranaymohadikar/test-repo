#this will have all the code related to reading the data (step 1)
import os
import sys
sys.path.append('D:\\coding _sessions\\test_project')
from src.logger import logging
from src.exception import CustomException

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass #used to create class variable
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

#for input 

@dataclass #decorator you will be able to define the class variable
class DataIngestionConfig:
    train_data_path:str = os.path.join("artifact","train.csv") #make sure to create artifact folder so that we will be able to see output will be saved in this path
    test_data_path:str = os.path.join("artifact","test.csv")
    raw_data_path:str = os.path.join("artifact","data.csv")

    #the above are the input to data ingestion componenet and now they know 
    #where to save the data

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig() #when called this will be saved in this variable
    
    def initiate_data_ingestion(self): #this code is for getting/read data from any database
        logging.info("Entered the data engestion method or component")
        try:
            df=pd.read_csv('D:\\coding _sessions\\test_project\\notebook\\data\\stud.csv') # this can from anywhere
            logging.info('exported or read dataset as dataframe')

               #creating the directory 

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok = True)

            df.to_csv(self.ingestion_config.raw_data_path, index = False, header = True)

            logging.info("train test split initiated")

            train_set,test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index = False, header = True)

            test_set.to_csv(self.ingestion_config.test_data_path, index = False, header = True)

            logging.info("Ingestion of data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
        
            )
        except Exception as e:
            raise CustomException(e, sys)


if __name__ =="__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data, test_data)