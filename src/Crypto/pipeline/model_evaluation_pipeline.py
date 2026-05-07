from src.Crypto.components.model_evaluation_component import ModelEvaluationComponent
from src.Crypto.config.configuration import ConfigurationManager
from src.Crypto.components.data_ingestion_component import DataIngestionComponent
from src.Crypto import logger


class ModelEvaluationPipeline:
    def __init__(self):
        pass
    
    def intantiate_model_evaluation_pipeline(self):
        
        #Creatign the  Data Ingestion Pipeline
        try:
            cfm = ConfigurationManager()
            data_ingestion = cfm.get_model_evaluation()
            data_ingestion_component = ModelEvaluationComponent(data_ingestion)
            data_ingestion_component.evaluate()
            # data_ingestion_component.train_model()
            logger.info("Pipeline Ran Sucessfully...✅")
        except Exception as e:
            logger.error("Pipeline Error...❌")
            raise e
        
        

if __name__ =="__main__":
    
    try:
        STAGE_NAME = "Model Evaluation stage" # Stage name define karna zaroori hai
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        
        obj =ModelEvaluationPipeline()
        obj.intantiate_model_evaluation_pipeline() # .main() call karna mat bhulna jo humne pipeline mein banaya hai
        
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
    
    