import sys
import os
sys.path.append(os.getcwd()) # Root directory ko path mein add karta hai


from src.Crypto.config.configuration import ConfigurationManager
from src.Crypto.components.data_ingestion_component import DataIngestionComponent
from src.Crypto import logger


class DataIngestionPipeline:
    def __init__(self):
        pass
    
    def intantiate_data_ingestion_pipeline(self):
        
        #Creatign the  Data Ingestion Pipeline
        try:
            cfm = ConfigurationManager()
            data_ingestion = cfm.get_data_ingestion()
            data_ingestion_component = DataIngestionComponent(data_ingestion)
            data_ingestion_component.initialize_db()
            # data_ingestion_component.fetch_comments()
            data_ingestion_component.save_comments()
            logger.info("Pipeline Ran Sucessfully...✅")
        except Exception as e:
            logger.error("Pipeline Error...❌")
            raise e
        
        
if __name__ == "__main__":
    try:
        logger.info(">>>>>> Stage: Data Ingestion Started <<<<<<")
        obj = DataIngestionPipeline()
        obj.intantiate_data_ingestion_pipeline()
        logger.info(">>>>>> Stage: Data Ingestion Completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
        
        
        
        

