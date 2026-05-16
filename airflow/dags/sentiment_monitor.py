# airflow/dags/sentiment_monitoring_dag.py

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd
import json
import os
from src.Crypto import logger


default_args = {
    'owner': 'crypto_guardian',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='sentiment_model_monitoring',
    default_args=default_args,
    description='Model performance monitoring aur data drift detection',
    schedule_interval='@daily',
    catchup=False,
    tags=['monitoring', 'ml', 'drift']
)

def check_model_performance(**context):
    """Production model ka performance check karega"""
    try:
        mlflow.set_tracking_uri("sqlite:///mlflow.db")
        client = MlflowClient()
        
        # Get production model info
        prod_versions = client.get_latest_versions(
            "sentiment_model",
            stages=["Production"]
        )
        
        if prod_versions:
            model = prod_versions[0]
            logger.info(f"Production Model V{model.version}")
            logger.info(f"F1 Score: {model.tags.get('f1_score', 'N/A')}")
            
            # Check model age
            creation_time = datetime.fromtimestamp(model.creation_timestamp / 1000)
            age_days = (datetime.now() - creation_time).days
            
            if age_days > 30:
                logger.warning(f"⚠️ Model {age_days} din purana hai! Retrain karo!")
            
            # Save metrics
            metrics = {
                "model_version": model.version,
                "stage": model.current_stage,
                "age_days": age_days,
                "f1_score": model.tags.get('f1_score'),
                "last_updated": str(creation_time)
            }
            
            os.makedirs("artifacts/monitoring", exist_ok=True)
            with open("artifacts/monitoring/model_health.json", 'w') as f:
                json.dump(metrics, f, indent=4)
            
            return metrics
        
    except Exception as e:
        logger.error(f"Monitoring failed: {str(e)}")
        raise

def check_data_drift(**context):
    """Data drift detection"""
    try:
        # Load reference data (training data statistics)
        ref_path = "artifacts/data_report/data_report.txt"
        
        # Current data statistics
        current_data_path = "artifacts/data_cleaning/cleaned_data.csv"
        if os.path.exists(current_data_path):
            df = pd.read_csv(current_data_path)
            
            current_stats = {
                "total_samples": len(df),
                "positive_ratio": (df['Label'] == 'POSITIVE').mean(),
                "avg_text_length": df['text'].str.len().mean(),
                "unique_words": len(set(' '.join(df['text'].fillna('')).split()))
            }
            
            os.makedirs("artifacts/monitoring", exist_ok=True)
            with open("artifacts/monitoring/data_stats.json", 'w') as f:
                json.dump(current_stats, f, indent=4)
            
            logger.info(f"Current data stats: {current_stats}")
            
            # Simple drift check
            # Agar positive ratio 30% se zyada change hua to alert
            if 0.3 < current_stats['positive_ratio'] > 0.7:
                logger.warning("⚠️ Possible data drift detected!")
            
            return current_stats
        
    except Exception as e:
        logger.error(f"Drift check failed: {str(e)}")
        raise

# Tasks
with dag:
    start = BashOperator(
        task_id='start_monitoring',
        bash_command='echo "📊 Starting Model Monitoring..."'
    )
    
    check_perf = PythonOperator(
        task_id='check_performance',
        python_callable=check_model_performance,
        provide_context=True
    )
    
    check_drift = PythonOperator(
        task_id='check_data_drift',
        python_callable=check_data_drift,
        provide_context=True
    )
    
    end = BashOperator(
        task_id='monitoring_complete',
        bash_command='echo "✅ Monitoring Complete!"',
        trigger_rule='all_done'
    )
    
    start >> [check_perf, check_drift] >> end