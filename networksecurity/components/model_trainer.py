from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact,ClassificationReportArtifact,DataTransformationArtifact
from networksecurity.utils.main_utils.utils import load_numpy_array
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score
from networksecurity.utils.main_utils.utils import evaluate_model,save_pickle_file,load_object
from networksecurity.utils.ml_utils.metric import classification_metric
from networksecurity.utils.ml_utils.model.estimator import NetoworkModel
import mlflow
#import dagshub
#dagshub.init(repo_owner='sameercusat', repo_name='networksecurity', mlflow=True)



class ModelTrainer:
    def __init__(self,modelTrainerConfig:ModelTrainerConfig,dataTransformerArtifact:DataTransformationArtifact):
        self.modelTrainerConfig = modelTrainerConfig
        self.dataTransformationArtifact = dataTransformerArtifact
    
    def track_mlflow(self,best_model,metric:classification_metric):
         with mlflow.start_run():
              f1_score = metric.f1_score
              accuracy_score = metric.accuracy_score
              recall_score = metric.recall_score
              precison_score = metric.recall_score

              mlflow.log_metric('f1_score',f1_score)
              mlflow.log_metric('accuracy_score',accuracy_score)
              mlflow.log_metric('recall_score',recall_score)
              mlflow.log_metric('precision_score',precison_score)
              mlflow.sklearn.log_model(best_model,'best_model')

         
    
    def train_model(self,x_train,y_train,x_test,y_test):
        try:
                logging.info("Importing Models for Classification")
                models = {
                    'LogisticRegressor': LogisticRegression(verbose=1),
                    'KNNClassifier': KNeighborsClassifier(),
                    'DecisionTeeClassifier': DecisionTreeClassifier(),
                    'RandomForestClassifier' : RandomForestClassifier(verbose=1),
                    'AdaBoostClassifier': AdaBoostClassifier(),
                    'GradientBoostClassifier': GradientBoostingClassifier(verbose=1)
                }
                params = {
                    'DecisionTeeClassifier' : {
                            "criterion": ["gini", "entropy", "log_loss"],
                            "max_depth": [None, 5, 10, 15, 20],
                            "min_samples_split": [2, 5, 10, 20],
                            "min_samples_leaf": [1, 2, 4, 8],
                            "max_features": [None, "sqrt", "log2"],
                            "splitter": ["best", "random"]
                    },
                    'RandomForestClassifier':{
                            'n_estimators':[8,16,32,64,128,256],
                            "max_depth": [1, 10, 20, 30],
                            "min_samples_split": [2, 5, 10],
                            "min_samples_leaf": [1, 2, 4],
                            "max_features": ["sqrt", "log2"]
                    },
                    'GradientBoostClassifier':{    "n_estimators": [8,16,32,64,128,256],
                                            "learning_rate": [0.01, 0.05, 0.1, 0.2],
                                            "max_depth": [3, 5, 7],
                                            "min_samples_split": [2, 5, 10],
                                                "subsample": [0.8, 1.0]
                                        },
                    'KNNClassifier':{
                        "n_neighbors": [3, 5, 7, 9, 11],
                        "weights": ["uniform", "distance"],
                        "metric": ["euclidean", "manhattan", "minkowski"]
                    },
                    'LogisticRegressor':{
                            "C": [0.001, 0.01, 0.1, 1, 10, 100],
                            "penalty": ["l1", "l2"],
                            "solver": ["liblinear", "saga"]
                    },
                    'AdaBoostClassifier':{
                            "n_estimators": [50, 100, 200, 300],
                            "learning_rate": [0.01, 0.1, 0.5, 1.0]
                    }
                }
                model_report,model_params = evaluate_model(x_train,y_train,x_test,y_test,params,models)
                logging.info("Got Model Report")
                print(model_report)
                best_model_score = max(sorted(model_report.values()))
                best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
                logging.info(f"Best Model is {str(best_model_name)}")
                best_model = models[best_model_name]
                best_params = model_params[best_model_name]
                best_model.set_params(**best_params)
                best_model.fit(x_train,y_train)
                y_pred_train = best_model.predict(x_train)
                y_pred_test = best_model.predict(x_test)
                model_dir_name = os.path.dirname(self.modelTrainerConfig.model_trainer_trained_model_path)
                os.makedirs(model_dir_name,exist_ok=True)
                logging.info('Importing the Preprocessor Object')
                preprocessor_obj = load_object(self.dataTransformationArtifact.transformed_obj_file_path)
                os.makedirs('final_model',exist_ok=True)
                save_pickle_file(preprocessor_obj,'final_model/preprocessor.pkl')
                save_pickle_file(best_model,'final_model/model.pkl')
                network_model = NetoworkModel(preprocessor=preprocessor_obj,model = best_model)
                save_pickle_file(network_model,self.modelTrainerConfig.model_trainer_trained_model_path)
                logging.info("Saving the Netowrk Model")
                report_train:ClassificationReportArtifact = classification_metric.get_classification_score(y_train,y_pred_train)
                self.track_mlflow(best_model,report_train)
                report_test:ClassificationReportArtifact = classification_metric.get_classification_score(y_test,y_pred_test)
                self.track_mlflow(best_model=best_model,metric=report_test)
                modelTrainerArtifact = ModelTrainerArtifact(trained_model_file_path=self.modelTrainerConfig.model_trainer_trained_model_path,
                                                            train_metrics_artifact=report_train,
                                                            test_metrics_artifact=report_test)
                logging.info("Model Training Completed")
                return modelTrainerArtifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_numpy_array = load_numpy_array(self.dataTransformationArtifact.transformed_train_file_path)
            test_numpy_array = load_numpy_array(self.dataTransformationArtifact.transformed_test_file_path)

            x_train,x_test,y_train,y_test = (train_numpy_array[:,:-1],test_numpy_array[:,:-1],train_numpy_array[:,-1],test_numpy_array[:,-1])
            modelTrainerArtifact:ModelTrainerArtifact = self.train_model(x_train,y_train,x_test,y_test)
            return modelTrainerArtifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
