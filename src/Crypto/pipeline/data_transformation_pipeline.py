from src.Crypto.components.data_transformation_component import DataTransformationComponent
from src.Crypto.components.data_report_component import DataReportComponent
from src.Crypto.components.data_labelling_component import DataLabellingComponent
from src.Crypto.config.configuration import ConfigurationManager
from src.Crypto.components.data_ingestion_component import DataIngestionComponent
from src.Crypto import logger


class DataTransformationPipeline:
    def __init__(self):
        pass
    
    def intantiate_data_transformation_pipeline(self):
        
        #Creatign the  Data Ingestion Pipeline
        try:
            cfm = ConfigurationManager()
            data_transformation_config_manager = cfm.get_data_transformation_config()
            data_transformation_component = DataTransformationComponent(data_transformation_config_manager)
            data_transformation_component.transformation()
            logger.info("Pipeline Ran Sucesssfully ✅😭 ")
        except Exception as e:
            logger.error("Are bhia kuch Error Aaa Gaya hai Yaar....")
            raise e

        
if __name__ =="__main__":
    try:
        STAGE_NAME = "Data Transformation stage" # Stage name define karna zaroori hai
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        
        obj = DataTransformationPipeline()
        obj.intantiate_data_transformation_pipeline() # .main() call karna mat bhulna jo humne pipeline mein banaya hai
        
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
    
    
