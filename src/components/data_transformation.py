#this file is for the data transformations processes like changing features handling null values etc. (step 2)

import sys
import os

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer #used to create pipeline.
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

sys.path.append('D:\\coding _sessions\\test_project')
from src.exception import CustomException
from src.logger import logging
from src.utills import save_object


# for providing input

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifact",'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        
    def get_data_transformer_object(self):  #for creating pickle files whcih were responsible for the conversation for data transformations
        try:
            numerical_columns = ['writing_score', "reading_score"]
            categorical_columns =[
                'gender', 
                'race_ethnicity', 
                'parental_level_of_education', 
                'lunch', 
                'test_preparation_course'
            ]

                #need to create pipeline for training dataset

            num_pipeline = Pipeline(

                steps = [

                    ("imputer", SimpleImputer(strategy="median")), # for handling missing values
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info(f'numerical columns {numerical_columns} ')

            cat_pipeline = Pipeline(

                steps= [

                    ('imputer', SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info(f'categorical columns encoding {categorical_columns}')

            preprocessor = ColumnTransformer(

                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns) ##providing the columns for transformation as pipeline
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_transformation(self, train_path, test_path): #starting of data transformation path from data ingestion

        try:
            
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("read train and test data completed")

            logging.info("obtaining preprocessing object")

            preprocessor_obj = self.get_data_transformer_object()

            target_column_name = 'math_score'
            numerical_columns = ['writing_score', "reading_score"]

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info('applying preprocessing object on the training and testing dataframe')
            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            #creating the whole train and test data with the help of concatenation 
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info("saving the preprocesing object")

            #saving the pickle file
            #thing to be written in utills
            save_object(

                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )

            return (
                train_arr,
                test_df,
                self.data_transformation_config.preprocessor_obj_file_path,
            )


        except Exception as e:
            raise CustomException(e, sys)
            




