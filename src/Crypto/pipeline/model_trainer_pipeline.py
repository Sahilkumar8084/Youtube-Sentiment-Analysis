from src.Crypto.components.model_trainer_component import ModelTrainerComponent
from src.Crypto.components.data_labelling_component import DataLabellingComponent
from src.Crypto.config.configuration import ConfigurationManager
from src.Crypto.components.data_ingestion_component import DataIngestionComponent
from src.Crypto import logger


class ModelTrainerPipeline:
    def __init__(self):
        pass
    
    def intantiate_model_trainer_pipeline(self):
        
        #Creatign the  Data Ingestion Pipeline
        try:
            cfm = ConfigurationManager()
            data_ingestion = cfm.get_model_training()
            data_ingestion_component = ModelTrainerComponent(data_ingestion)
            data_ingestion_component.prepare_data()
            data_ingestion_component.train_model()
            logger.info("Pipeline Ran Sucessfully...✅")
        except Exception as e:
            logger.error("Pipeline Error...❌")
            raise e
                

