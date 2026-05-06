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
        
        

