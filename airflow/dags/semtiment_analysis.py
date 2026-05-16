# airflow/dags/crypto_sentiment_pipeline.py

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.models import Variable
import sys

import os
# print(os.listdir)

# Project root path add karo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


from src.Crypto.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.Crypto.pipeline.data_labelling_pipeline import DataLabellingPipeline
from src.Crypto.pipeline.data_conversioin_pipeline import DataConversionPipeline
from src.Crypto.pipeline.data_cleaning_pipeline import DataCleaningPipeline
from src.Crypto.pipeline.data_report_pipeline import DataReportPipeline
from src.Crypto.pipeline.eda_report_pipeline import EDAReportPipeline
from src.Crypto.pipeline.data_transformation_pipeline import DataTransformationPipeline
from src.Crypto.pipeline.model_trainer_pipeline import ModelTrainerPipeline
from src.Crypto.pipeline.model_evaluation_pipeline import ModelEvaluationPipeline
from src.Crypto import logger

# Default arguments for DAG
default_args = {
    'owner': 'Sahil Kumar',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': Variable.get('alert_email', default_var='hakla0123456789@gmail.com'),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2)
}

# DAG define karo
dag = DAG(
    dag_id='Youtube_sentiment_analysis_pipeline',
    default_args=default_args,
    description='YouTube Sentiment Analysis ML Pipeline with Auto-Promotion',
    schedule_interval='@weekly',  # Har Monday subah 6 AM UTC
    catchup=False,
    max_active_runs=1,
    tags=['ml', 'sentiment', 'youtube', 'production'],
    doc_md="""
    ## Sentiment Analysis Pipeline
    
    Ye DAG complete ML pipeline run karta hai:
    1. **Data Ingestion** - YouTube/nayi data source se data fetch
    2. **Data Processing** - Labelling, Conversion, Cleaning
    3. **Data Analysis** - EDA aur Data Reports
    4. **Feature Engineering** - Text vectorization
    5. **Model Training** - Random Forest training
    6. **Model Evaluation** - MLflow metrics aur auto-promotion
    
    ### Schedule:
    - Weekly (Har Monday 11:30 AM IST)
    
    ### Alerts:
    - Failure pe email alert jayega
    """
)

# ==================== TASK DEFINITIONS ====================

def run_data_ingestion(**context):
    """Data Ingestion Stage"""
    try:
        logger.info("=" * 50)
        logger.info("STAGE: Data Ingestion Started")
        logger.info("=" * 50)
        
        pipeline = DataIngestionPipeline()
        pipeline.intantiate_data_ingestion_pipeline()
        
        logger.info("STAGE: Data Ingestion Completed Successfully")
        return "Data Ingestion - SUCCESS"
    except Exception as e:
        logger.error(f"Data Ingestion Failed: {str(e)}")
        raise

def run_data_labelling(**context):
    """Data Labelling Stage"""
    try:
        logger.info("=" * 50)
        logger.info("STAGE: Data Labelling Started")
        logger.info("=" * 50)
        
        pipeline = DataLabellingPipeline()
        pipeline.intantiate_data_labelling_pipeline()
        
        logger.info("STAGE: Data Labelling Completed Successfully")
        return "Data Labelling - SUCCESS"
    except Exception as e:
        logger.error(f"Data Labelling Failed: {str(e)}")
        raise

def run_data_conversion(**context):
    """Data Conversion Stage"""
    try:
        logger.info("=" * 50)
        logger.info("STAGE: Data Conversion Started")
        logger.info("=" * 50)
        
        pipeline = DataConversionPipeline()
        pipeline.intantiate_data_conversion_pipeline()
        
        logger.info("STAGE: Data Conversion Completed Successfully")
        return "Data Conversion - SUCCESS"
    except Exception as e:
        logger.error(f"Data Conversion Failed: {str(e)}")
        raise

def run_data_cleaning(**context):
    """Data Cleaning Stage"""
    try:
        logger.info("=" * 50)
        logger.info("STAGE: Data Cleaning Started")
        logger.info("=" * 50)
        
        pipeline = DataCleaningPipeline()
        pipeline.intantiate_data_cleaning_pipeline()
        
        logger.info("STAGE: Data Cleaning Completed Successfully")
        return "Data Cleaning - SUCCESS"
    except Exception as e:
        logger.error(f"Data Cleaning Failed: {str(e)}")
        raise

def run_data_report(**context):
    """Data Report Stage"""
    try:
        logger.info("=" * 50)
        logger.info("STAGE: Data Report Started")
        logger.info("=" * 50)
        
        pipeline = DataReportPipeline()
        pipeline.intantiate_data_report_pipeline()
        
        logger.info("STAGE: Data Report Completed Successfully")
        return "Data Report - SUCCESS"
    except Exception as e:
        logger.error(f"Data Report Failed: {str(e)}")
        raise

def run_eda_report(**context):
    """EDA Report Stage"""
    try:
        logger.info("=" * 50)
        logger.info("STAGE: EDA Report Started")
        logger.info("=" * 50)
        
        pipeline = EDAReportPipeline()
        pipeline.intantiate_eda_report_pipeline()
        
        logger.info("STAGE: EDA Report Completed Successfully")
        return "EDA Report - SUCCESS"
    except Exception as e:
        logger.error(f"EDA Report Failed: {str(e)}")
        raise

def run_data_transformation(**context):
    """Data Transformation Stage"""
    try:
        logger.info("=" * 50)
        logger.info("STAGE: Data Transformation Started")
        logger.info("=" * 50)
        
        pipeline = DataTransformationPipeline()
        pipeline.intantiate_data_transformation_pipeline()
        
        logger.info("STAGE: Data Transformation Completed Successfully")
        return "Data Transformation - SUCCESS"
    except Exception as e:
        logger.error(f"Data Transformation Failed: {str(e)}")
        raise

# def run_data_splitting(**context):
#     """Data Splitting Stage"""
#     try:
#         logger.info("=" * 50)
#         logger.info("STAGE: Data Splitting Started")
#         logger.info("=" * 50)
        
#         pipeline = DataSplittingPipeline()
#         pipeline.intantiate_data_splitting_pipeline()
        
#         logger.info("STAGE: Data Splitting Completed Successfully")
#         return "Data Splitting - SUCCESS"
#     except Exception as e:
#         logger.error(f"Data Splitting Failed: {str(e)}")
#         raise

def run_model_training(**context):
    """Model Training Stage"""
    try:
        logger.info("=" * 50)
        logger.info("STAGE: Model Training Started")
        logger.info("=" * 50)
        
        pipeline = ModelTrainerPipeline()
        pipeline.intantiate_model_training_pipeline()
        
        logger.info("STAGE: Model Training Completed Successfully")
        return "Model Training - SUCCESS"
    except Exception as e:
        logger.error(f"Model Training Failed: {str(e)}")
        raise

def run_model_evaluation(**context):
    """Model Evaluation Stage with MLflow"""
    try:
        logger.info("=" * 50)
        logger.info("STAGE: Model Evaluation Started")
        logger.info("=" * 50)
        
        pipeline = ModelEvaluationPipeline()
        pipeline.intantiate_model_evaluation_pipeline()
        
        # Check if model was promoted to production
        import mlflow
        from mlflow.tracking import MlflowClient
        
        mlflow.set_tracking_uri("sqlite:///mlflow.db")
        client = MlflowClient()
        
        prod_versions = client.get_latest_versions(
            "sentiment_model", 
            stages=["Production"]
        )
        
        if prod_versions:
            prod_model = prod_versions[0]
            f1_score = prod_model.tags.get("f1_score", "N/A")
            logger.info(f"Production Model - Version: {prod_model.version}, F1: {f1_score}")
            
            # Push to XCom for downstream tasks
            context['task_instance'].xcom_push(
                key='model_promoted',
                value=True
            )
            context['task_instance'].xcom_push(
                key='model_version',
                value=prod_model.version
            )
            context['task_instance'].xcom_push(
                key='f1_score',
                value=f1_score
            )
        
        logger.info("STAGE: Model Evaluation Completed Successfully")
        return "Model Evaluation - SUCCESS"
    except Exception as e:
        logger.error(f"Model Evaluation Failed: {str(e)}")
        raise

def check_model_promotion(**context):
    """Check if model was promoted to production"""
    ti = context['task_instance']
    promoted = ti.xcom_pull(task_ids='evaluate_model', key='model_promoted')
    version = ti.xcom_pull(task_ids='evaluate_model', key='model_version')
    f1 = ti.xcom_pull(task_ids='evaluate_model', key='f1_score')
    
    if promoted:
        logger.info(f"✅ Model V{version} PRODUCTION mein promote hua! F1: {f1}")
        return True
    else:
        logger.info("❌ Model production worthy nahi tha")
        return False

def send_success_notification(**context):
    """Success notification bhejo"""
    ti = context['task_instance']
    version = ti.xcom_pull(task_ids='evaluate_model', key='model_version')
    f1 = ti.xcom_pull(task_ids='evaluate_model', key='f1_score')
    
    dag_run = context['dag_run']
    execution_date = dag_run.execution_date
    
    message = f"""
    ✅ ML Pipeline Successfully Completed!
    
    Execution Date: {execution_date}
    Model Version: V{version}
    F1 Score: {f1}
    
    Model PRODUCTION mein promote ho gaya hai!
    """
    logger.info(message)
    
    # Yahan Slack/Discord webhook bhi add kar sakte ho
    return message

def run_data_validation(**context):
    """Data quality checks"""
    import pandas as pd
    import numpy as np
    
    try:
        logger.info("Running data validation checks...")
        
        # Load processed data
        data_path = "artifacts/data_cleaning/cleaned_data.csv"
        df = pd.read_csv(data_path)
        
        # Validation checks
        checks = {
            "total_rows": len(df),
            "null_values": df.isnull().sum().sum(),
            "empty_text": (df['text'].str.strip() == '').sum(),
            "duplicate_rows": df.duplicated().sum()
        }
        
        logger.info(f"Validation Results: {checks}")
        
        # Quality gates
        if checks['null_values'] > df.shape[0] * 0.1:  # 10% threshold
            raise ValueError(f"Too many nulls: {checks['null_values']}")
        
        if checks['empty_text'] > df.shape[0] * 0.05:
            raise ValueError(f"Too many empty texts: {checks['empty_text']}")
        
        # Push results to XCom
        context['task_instance'].xcom_push(key='validation_results', value=checks)
        
        logger.info("Data validation passed!")
        return "Validation - PASSED"
        
    except Exception as e:
        logger.error(f"Data validation failed: {str(e)}")
        raise

# ==================== TASK DEFINITION ====================

with dag:
    # Start pipeline
    start_pipeline = BashOperator(
        task_id='start_pipeline',
        bash_command='echo "🚀 ML Pipeline Starting at $(date)"',
        dag=dag
    )
    
    # Data validation
    validate_data = PythonOperator(
        task_id='validate_data',
        python_callable=run_data_validation,
        provide_context=True,
        dag=dag
    )
    
    # Data Processing Stage
    t1_ingestion = PythonOperator(
        task_id='ingest_data',
        python_callable=run_data_ingestion,
        provide_context=True,
        execution_timeout=timedelta(minutes=30),
        dag=dag
    )
    
    t2_labelling = PythonOperator(
        task_id='label_data',
        python_callable=run_data_labelling,
        provide_context=True,
        dag=dag
    )
    
    t3_conversion = PythonOperator(
        task_id='convert_data',
        python_callable=run_data_conversion,
        provide_context=True,
        dag=dag
    )
    
    t4_cleaning = PythonOperator(
        task_id='clean_data',
        python_callable=run_data_cleaning,
        provide_context=True,
        dag=dag
    )
    
    # Analysis Stage
    t5_data_report = PythonOperator(
        task_id='generate_data_report',
        python_callable=run_data_report,
        provide_context=True,
        dag=dag
    )
    
    t6_eda_report = PythonOperator(
        task_id='generate_eda_report',
        python_callable=run_eda_report,
        provide_context=True,
        dag=dag
    )
    
    # Feature Engineering Stage
    t7_transformation = PythonOperator(
        task_id='transform_data',
        python_callable=run_data_transformation,
        provide_context=True,
        dag=dag
    )
    
    # t8_splitting = PythonOperator(
    #     task_id='split_data',
    #     python_callable=run_data_splitting,
    #     provide_context=True,
    #     dag=dag
    # )
    
    # Model Training Stage
    t9_training = PythonOperator(
        task_id='train_model',
        python_callable=run_model_training,
        provide_context=True,
        dag=dag
    )
    
    # Model Evaluation Stage
    t10_evaluation = PythonOperator(
        task_id='evaluate_model',
        python_callable=run_model_evaluation,
        provide_context=True,
        dag=dag
    )
    
    # Promotion check
    check_promotion = PythonOperator(
        task_id='check_promotion',
        python_callable=check_model_promotion,
        provide_context=True,
        dag=dag
    )
    
    # Success notification
    notify_success = PythonOperator(
        task_id='notify_success',
        python_callable=send_success_notification,
        provide_context=True,
        dag=dag
    )
    
    # End pipeline
    end_pipeline = BashOperator(
        task_id='end_pipeline',
        bash_command='echo "✅ ML Pipeline Completed at $(date)"',
        trigger_rule='all_done',
        dag=dag
    )
    
    # ==================== PIPELINE FLOW ====================
    # Data Processing Flow
    start_pipeline >> validate_data >> t1_ingestion >> t2_labelling >> t3_conversion >> t4_cleaning
    
    # Parallel Analysis
    t4_cleaning >> [t5_data_report, t6_eda_report]
    
    # Feature Engineering Flow
    [t5_data_report, t6_eda_report] >> t7_transformation 
    
    # Model Training & Evaluation Flow
    t9_training >> t10_evaluation >> check_promotion >> notify_success
    
    # End flow
    notify_success >> end_pipeline