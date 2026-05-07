from src.Crypto.components.data_conversion_component import DataConversionComponent
from src.Crypto.config.configuration import ConfigurationManager
from src.Crypto.components.data_ingestion_component import DataIngestionComponent
from src.Crypto import logger


class DataConversionPipeline:
    def __init__(self):
        pass
    
    def intantiate_data_conversion_pipeline(self):
        
        #Creatign the  Data Ingestion Pipeline
            try:
                cfm = ConfigurationManager()
                data_conversion= cfm.get_data_conversion()
                data_conversion_component = DataConversionComponent(data_conversion)
                data_conversion_component.csv_conversion()
                logger.info("Pipeline Ran Sucessfully...✅")
            except Exception as e:
                logger.error("Pipeline Error...❌")
                raise e
            
if __name__ =="__main__":
           
    try:
        STAGE_NAME = "Data Conversion stage" # Stage name define karna zaroori hai
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        
        obj = DataConversionPipeline()
        obj.intantiate_data_conversion_pipeline() # .main() call karna mat bhulna jo humne pipeline mein banaya hai
        
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

