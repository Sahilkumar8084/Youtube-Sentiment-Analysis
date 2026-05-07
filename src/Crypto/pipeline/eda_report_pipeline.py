from src.Crypto.components.eda_report_component import EDAReportComponent
from src.Crypto.components.data_cleaning_component import DataCleaningComponent
from src.Crypto.config.configuration import ConfigurationManager
from src.Crypto import logger


class EDAReportPipeline:
    def __init__(self):
        pass
    
    def intantiate_eda_report_pipeline(self):
        
        try:
            cfm = ConfigurationManager()
            data_report = cfm.get_eda_report()
            data_report_component = EDAReportComponent(data_report)
            
            data_report_component.download()
            logger.info("Pipeline Ran Sucessfully...✅")
        except Exception as e:
            logger.error("Pipeline Error...❌")
            raise e
                
                
if __name__ == "__main__":
    try:
        STAGE_NAME = "EDA Report stage" # Stage name define karna zaroori hai
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        
        obj = EDAReportPipeline()
        obj.intantiate_eda_report_pipeline() # .main() call karna mat bhulna jo humne pipeline mein banaya hai
        
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
    
    
    
        

