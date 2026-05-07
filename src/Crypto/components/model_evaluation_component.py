


import numpy as np
import pickle
import json
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
from src.Crypto.entity.config_entity import ModelEvaluationConfig
from src.Crypto import logger
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
from sklearn.metrics import RocCurveDisplay, PrecisionRecallDisplay, roc_auc_score
import os
from dotenv import load_dotenv
load_dotenv()

class ModelEvaluationComponent:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config
        self.x_test_emb = np.load(self.config.test_embedding)
        self.test_df = pd.read_csv(self.config.test_data_path)
        self.y_test = self.test_df['Label']
        self.vectorizer = joblib.load(self.config.vectorizer_path)
        self.model = joblib.load(self.config.model_path)
        
    def evaluate(self):
        self.y_pred = self.model.predict(self.x_test_emb)
        self.y_score = self.model.predict_proba(self.x_test_emb)[:, 1] 
        
        # Calculate metrics
        logger.info("Evaluation metrics calculate kar rahe hain...")
        accuracy = accuracy_score(self.y_test, self.y_pred)
        precision = precision_score(self.y_test, self.y_pred, average='weighted')
        recall = recall_score(self.y_test, self.y_pred, average='weighted')
        f1 = f1_score(self.y_test, self.y_pred, average='weighted')
        roc_auc = roc_auc_score(self.y_test, self.y_score)
        
        # Plots (ROC & PR)
        os.makedirs(self.config.root_dir, exist_ok=True)
        roc_plot_path = os.path.join(self.config.root_dir, "roc_curve.png")
        pr_plot_path = os.path.join(self.config.root_dir, "pr_curve.png")
        
        RocCurveDisplay.from_estimator(self.model, self.x_test_emb, self.y_test)
        plt.savefig(roc_plot_path)
        plt.close()

        PrecisionRecallDisplay.from_estimator(self.model, self.x_test_emb, self.y_test)
        plt.savefig(pr_plot_path)
        plt.close()

        # MLFLOW
        mlflow.set_tracking_uri(self.config.mlflow_tracking_uri)
        mlflow.set_experiment(self.config.mlflow_experiment_name)
        
        with mlflow.start_run() as run:
            mlflow.log_params(self.config.all_parmas)
            mlflow.log_param("vectorizer_model", "all-mpnet-base-v2")
            mlflow.log_metrics({"accuracy": accuracy, "precision": precision, "recall": recall, "f1_score": f1, "roc_auc": roc_auc})
            
            mlflow.log_artifact(roc_plot_path, "plots")
            mlflow.log_artifact(pr_plot_path, "plots")
            
            # Model Logging (Pipeline skip kar di taaki fast ho)
            model_info = mlflow.sklearn.log_model(
                sk_model=self.model,
                artifact_path="model",
                registered_model_name=self.config.mlflow_registered_model_name
            )

            current_version = model_info.registered_model_version
            logger.info(f"Model version {current_version} register ho gaya!")

            # FIX 1: Tag set karne ka sahi tareeka
            client = MlflowClient()
            client.set_model_version_tag(
                name=self.config.mlflow_registered_model_name,
                version=current_version,
                key="f1_score",
                value=str(f1)
            )

            # Promotion Logic call
            should_promote = self.check_and_promote_model(f1, current_version)
            
            if should_promote:
                logger.info(f"Version {current_version} PRODUCTION mein hai! 🚀")
            else:
                logger.info(f"Version {current_version} STAGING mein rakha gaya.")

    def check_and_promote_model(self, current_f1, current_version):
        try:
            client = MlflowClient()
            model_name = self.config.mlflow_registered_model_name
            
            # Latest production version check
            prod_versions = client.get_latest_versions(model_name, stages=['Production'])
            
            if prod_versions:
                prod_model = prod_versions[0]
                # Tag se F1 score nikalna (safety ke liye 0 default)
                prod_f1 = float(prod_model.tags.get("f1_score", 0))
                
                if current_f1 > prod_f1:
                    logger.info(f"New model (F1: {current_f1}) better hai old (F1: {prod_f1}) se.")
                    # Purane ko hatao
                    client.transition_model_version_stage(model_name, prod_model.version, "Archived")
                    # Naye ko promote karo
                    client.transition_model_version_stage(model_name, current_version, "Production")
                    return True
                else:
                    client.transition_model_version_stage(model_name, current_version, "Staging")
                    return False
            else:
                # Pehla production model
                client.transition_model_version_stage(model_name, current_version, "Production")
                return True
        except Exception as e:
            logger.error(f"Promotion error: {e}")
            return False
                        