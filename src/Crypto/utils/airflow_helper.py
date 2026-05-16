# src/Crypto/utils/airflow_helper.py

import mlflow
from mlflow.tracking import MlflowClient
import json
import os
from datetime import datetime
from src.Crypto import logger

class AirflowHelper:
    """Airflow tasks ke liye helper functions"""
    
    @staticmethod
    def get_production_model_info():
        """Production model ki info fetch karo"""
        try:
            mlflow.set_tracking_uri("sqlite:///mlflow.db")
            client = MlflowClient()
            
            prod_versions = client.get_latest_versions(
                "sentiment_model",
                stages=["Production"]
            )
            
            if prod_versions:
                model = prod_versions[0]
                return {
                    "version": model.version,
                    "f1_score": model.tags.get("f1_score", "N/A"),
                    "stage": model.current_stage,
                    "creation_time": datetime.fromtimestamp(
                        model.creation_timestamp / 1000
                    ).isoformat()
                }
            return None
            
        except Exception as e:
            logger.error(f"Model info fetch error: {str(e)}")
            return None
    
    @staticmethod
    def trigger_retrain_if_needed(threshold=0.8):
        """Agar model performance kam hai to retrain trigger karo"""
        try:
            model_info = AirflowHelper.get_production_model_info()
            
            if model_info and float(model_info['f1_score']) < threshold:
                logger.warning(f"Model F1 ({model_info['f1_score']}) is below threshold ({threshold})")
                logger.info("Retrain trigger hona chahiye!")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Retrain check error: {str(e)}")
            return False
    
    @staticmethod
    def save_pipeline_metrics(metrics, stage_name):
        """Pipeline metrics save karo for monitoring"""
        try:
            os.makedirs("artifacts/pipeline_metrics", exist_ok=True)
            filename = f"artifacts/pipeline_metrics/{stage_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w') as f:
                json.dump({
                    "stage": stage_name,
                    "timestamp": datetime.now().isoformat(),
                    "metrics": metrics
                }, f, indent=4)
            
            logger.info(f"Metrics saved to {filename}")
            
        except Exception as e:
            logger.error(f"Metrics save error: {str(e)}")