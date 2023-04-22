#specifically for training the model (step 3)

import pandas as pd
import sys
import os
from dataclasses import dataclass

sys.path.append('D:\\coding _sessions\\test_project')
from src.exception import CustomException
from src.logger import logging

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.utills import save_object, evaluate_models

@dataclass

#for providing input par=th is given

class ModelTrainerConfig: 
    trained_model_file_path = os.path.join('artifact',"model.pkl")

#class which will be responsible for training of model
 
class ModelTrainer:
    def __init__(self):
        self.model_trainer_conf = ModelTrainerConfig()


    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("splitting training and test input data")
            X_train, y_train = train_array[:, :-1], train_array[:, -1]
            X_test, y_test = test_array[:, :-1], test_array[:, -1]

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree" : DecisionTreeRegressor(),
                "Gradient Boosting":GradientBoostingRegressor(),
                "Linear Regression" : LinearRegression(),
                "K-neighbour Regressor": KNeighborsRegressor(),
                "XGB Regressor":XGBRegressor(),
                "Catboost Regressor": CatBoostRegressor(),
                "Adaboost Regressor":AdaBoostClassifier(),
            }
            #evaluate model will be function to be created in utils as common function

            model_report:dict = evaluate_models(X_train = X_train, y_train = y_train, X_test = X_test, y_test = y_test, models = models)

            #to get the best model score from  dict

            best_model_score = max(sorted(model_report.values()))

            #to get best model name form dict 

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best Model")
            logging.info(f"Best found model on both training and test dataset ")

            save_object(
                file_path=self.model_trainer_conf.trained_model_file_path,
                obj = best_model
                
            )

            predicted = best_model.predict(X_test)

            r2_square = r2_score(y_test, predicted)
            return r2_square
        

        except Exception as e:
            raise CustomException (e, sys)