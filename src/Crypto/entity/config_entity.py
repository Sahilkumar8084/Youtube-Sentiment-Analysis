from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    local_data_files: Path 
    
@dataclass
class DataConversionConfig:
    root_dir: Path
    db_path: Path
    table_name: str
    converted_data_path: Path 
    
@dataclass
class DataLabellingConfig:
    database_path : Path
    
@dataclass
class DataCleaningConfig:
    cleaning_root: Path
    data_path: Path
    saved_data: Path
    
@dataclass
class DataReportConfig:
    root_dir: Path
    data_path: Path 
    report_path: Path
    
@dataclass
class EDAReportConfig:
    root_dir: Path
    data_path: Path 
    output_report: Path
    
@dataclass
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    vectorizer_path: Path

@dataclass
class ModelTrainingConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_path: Path
    model_name: str
    train_embedding: Path
    test_embedding: Path
    p_c: int
    p_gamma: str
    p_kernel: str
    

@dataclass
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path 
    model_path: Path
    vectorizer_path: Path
    test_embedding: Path
    evaluation_metrics_path : Path
    curve_img: Path
    mlflow_tracking_uri: str
    mlflow_experiment_name: str
    mlflow_registered_model_name :str
    all_parmas: dict