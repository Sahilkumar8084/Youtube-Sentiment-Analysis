from src.Crypto.components.data_labelling_component import DataLabellingComponent
from src.Crypto.config.configuration import ConfigurationManager
from src.Crypto.components.data_ingestion_component import DataIngestionComponent
from src.Crypto import logger


class DataLabellingPipeline:
    def __init__(self):
        pass
    
    def intantiate_data_labelling_pipeline(self):
        
        #Creatign the  Data Ingestion Pipeline

        try:
            logger.debug("Labeling PipeLine Started...")
            cfm = ConfigurationManager()
            di = cfm.get_data_labelling()
            dic = DataLabellingComponent(di)
            dic.fetch_database()
            # dic.alter_db()
            dic.label_db()
            logger.debug("Labeling PipeLine Ran Sucessfully...✅")
            
        except Exception as e:
            logger.error("Something Went Wrong ❌")
            logger.error(e)
            raise e
        
        
if __name__=="__main__":
    
    try:
        STAGE_NAME = "Data Labelling stage" # Stage name define karna zaroori hai
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        
        obj = DataLabellingPipeline()
        obj.intantiate_data_labelling_pipeline() # .main() call karna mat bhulna jo humne pipeline mein banaya hai
        
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
