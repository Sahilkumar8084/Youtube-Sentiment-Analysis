from src.Crypto.components.data_cleaning_component import DataCleaningComponent
from src.Crypto.config.configuration import ConfigurationManager
from src.Crypto import logger


class DataCleaningPipeline:
    def __init__(self):
        pass
    
    def intantiate_data_cleaning_pipeline(self):
        
        try:
            cfm = ConfigurationManager()
            data_Cleaning = cfm.get_data_cleaning()
            data_Cleaning_component = DataCleaningComponent(data_Cleaning)
            data_Cleaning_component.cleanning()
            data_Cleaning_component.save_csv()
            logger.info("Pipeline Ran Sucessfully...✅")
        except Exception as e:
            logger.error("Pipeline Error...❌")
            raise e
        
if __name__ == "__main__":
    
    try:
        STAGE_NAME = "Data Cleaning stage" # Stage name define karna zaroori hai
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        
        obj = DataCleaningPipeline()
        obj.intantiate_data_cleaning_pipeline() # .main() call karna mat bhulna jo humne pipeline mein banaya hai
        
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
    

