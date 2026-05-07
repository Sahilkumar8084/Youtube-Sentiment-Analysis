from src.Crypto.constants import *
from src.Crypto.utils.helper import read_yaml,create_directories
from src.Crypto import logger
from src.Crypto.entity.config_entity import *

class ConfigurationManager:
    
    def __init__(self,config_file_path=CONFIG_FILE_PATH,
                      params_file_path = PARAMS_FILE_PATH,
                      schema_file_path = SCHEMA_FILE_PATH):
        self.config =read_yaml( config_file_path)
        self.parmas = read_yaml(params_file_path)
        self.schema = read_yaml(schema_file_path)
        
        create_directories([self.config.artifacts_root])
        logger.debug(f"Till Now all the Yaml Files are Read Sucessfully...✅")

    def get_data_ingestion(self)->DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            local_data_files= config.local_data_files
        )
        logger.debug("get_data_ngestion is working compeletely fine...✅")
        return data_ingestion_config
    
       
    def get_data_labelling(self)->DataLabellingConfig:
        config = self.config.data_labelling
        # create_directories([config.database_path])
        
        data_labelling_config = DataLabellingConfig(
            database_path=config.database_path
            
        )
        logger.debug("get_data_labelling is working compeletely fine...✅")
        return data_labelling_config
    
    def get_data_conversion(self)->DataConversionConfig:
        config = self.config.data_conversion
        create_directories([config.root_dir])
        
        data_conversion_config = DataConversionConfig(
            root_dir=config.root_dir,
            db_path = config.db_path,
            table_name= config.table_name,
            converted_data_path= config.converted_data_path
        )
        logger.debug("get_data_conversion is working compeletely fine...✅")
        return data_conversion_config
    
    def get_data_cleaning(self)->DataCleaningConfig:
        config = self.config.data_cleaning
        create_directories([config.cleaning_root])
        
        data_cleaning_config = DataCleaningConfig(
            cleaning_root=config.cleaning_root,
            data_path=config.data_path,
            saved_data= config.saved_data
        )
        logger.debug("get_data_cleaning is working compeletely fine...✅")
        return data_cleaning_config

    def get_data_report(self)->DataReportConfig:
        config = self.config.data_report
        create_directories([config.root_dir])
        
        data_report_config = DataReportConfig(
            root_dir=config.root_dir,
            data_path= config.data_path,
            report_path = config.report_path
        )
        logger.debug("get_data_ngestion is working compeletely fine...✅")
        return data_report_config

    def get_eda_report(self)->EDAReportConfig:
        config = self.config.eda_report
        create_directories([config.root_dir])
        
        eda_report_config = EDAReportConfig(
            root_dir=config.root_dir,
            data_path= config.data_path,
            output_report = config.output_report
        )
        logger.debug("get_eda_report is working compeletely fine...✅")
        return eda_report_config
    
    def get_data_transformation_config(self)-> DataTransformationConfig:
        config =  self.config.data_transformation
        create_directories([config.root_dir])
        data_transformation_config  = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            vectorizer_path= config.vectorizer_path
        )
        logger.debug("Get_transformation_data is working properly..")
        return data_transformation_config
           
    def get_data_transformation_config(self)-> DataTransformationConfig:
        config =  self.config.data_transformation
        create_directories([config.root_dir])
        data_transformation_config  = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            vectorizer_path= config.vectorizer_path

        )
        return data_transformation_config

            
    def get_model_training(self)->ModelTrainingConfig:
        config = self.config.model_training
        parmas = self.parmas
        create_directories([config.root_dir])
        
        model_trainer = ModelTrainingConfig(
                    root_dir = config.root_dir,
                    train_data_path = config.train_data_path,
                    test_data_path= config.test_data_path,
                    model_path= config.model_path,
                    model_name= config.model_name,
                    p_c= parmas.SVC.C,
                    p_gamma= parmas.SVC.gamma,
                    p_kernel= parmas.SVC.kernel,
                    train_embedding= config.train_embedding,
                    test_embedding= config.test_embedding
                    
        )
        logger.debug("Model Trainer is working compeletely fine...✅")
        return model_trainer
    
    def get_model_evaluation(self)->ModelEvaluationConfig:
        config = self.config.model_evaluation
        mlflow_config = self.config.mlflow
        parmas = self.parmas.SVC
        create_directories([config.root_dir])
        
        model_evaluation_config = ModelEvaluationConfig(
            root_dir=config.root_dir,
            test_data_path=config.test_data_path,
            model_path=config.model_path,
            test_embedding= config.test_embedding,
            vectorizer_path = config.vectorizer_path,
            mlflow_tracking_uri=mlflow_config.mlflow_tracking_uri,
            mlflow_experiment_name=mlflow_config.mlflow_experiment_name,
            mlflow_registered_model_name=mlflow_config.mlflow_registered_model_name,
            evaluation_metrics_path=config.evaluation_metrics_path,
            curve_img= config.curve_img,
            all_parmas = parmas
            # f1_score_threshold=config.f1_score_threshold
        )
        logger.debug("Model Evaluation is working compeletely fine...✅")
        return model_evaluation_config


    
