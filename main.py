from src.Crypto.pipeline.model_trainer_pipeline import ModelTrainerPipeline
from src.Crypto.pipeline.data_transformation_pipeline import DataTransformationPipeline
from src.Crypto.pipeline.eda_report_pipeline import EDAReportPipeline
from src.Crypto.pipeline.data_report_pipeline import DataReportPipeline
from src.Crypto.pipeline.data_cleaning_pipeline import DataCleaningPipeline
from src.Crypto.pipeline.data_labelling_pipeline import DataLabellingPipeline
from src.Crypto.pipeline.data_conversioin_pipeline import DataConversionPipeline
from src.Crypto import logger
from src.Crypto.pipeline.data_ingestion_pipeline import DataIngestionPipeline



if __name__ == "__main__":
    try:
        STAGE_NAME = "Data Ingestion stage" # Stage name define karna zaroori hai
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        
        obj = DataIngestionPipeline()
        obj.intantiate_data_ingestion_pipeline() # .main() call karna mat bhulna jo humne pipeline mein banaya hai
        
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
    
    
    try:
        STAGE_NAME = "Data Labelling stage" # Stage name define karna zaroori hai
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        
        obj = DataLabellingPipeline()
        obj.intantiate_data_labelling_pipeline() # .main() call karna mat bhulna jo humne pipeline mein banaya hai
        
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
    
    
    
    try:
        STAGE_NAME = "Data Conversion stage" # Stage name define karna zaroori hai
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        
        obj = DataConversionPipeline()
        obj.intantiate_data_conversion_pipeline() # .main() call karna mat bhulna jo humne pipeline mein banaya hai
        
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
    
    
    try:
        STAGE_NAME = "Data Cleaning stage" # Stage name define karna zaroori hai
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        
        obj = DataCleaningPipeline()
        obj.intantiate_data_cleaning_pipeline() # .main() call karna mat bhulna jo humne pipeline mein banaya hai
        
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
    
    
    try:
        STAGE_NAME = "Data Report stage" # Stage name define karna zaroori hai
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        
        obj = DataReportPipeline()
        obj.intantiate_data_report_pipeline() # .main() call karna mat bhulna jo humne pipeline mein banaya hai
        
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
    
    
    try:
        STAGE_NAME = "EDA Report stage" # Stage name define karna zaroori hai
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        
        obj = EDAReportPipeline()
        obj.intantiate_eda_report_pipeline() # .main() call karna mat bhulna jo humne pipeline mein banaya hai
        
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
    
    
    try:
        STAGE_NAME = "Data Transformation stage" # Stage name define karna zaroori hai
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        
        obj = DataTransformationPipeline()
        obj.intantiate_data_transformation_pipeline() # .main() call karna mat bhulna jo humne pipeline mein banaya hai
        
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
    
    
    
    try:
        STAGE_NAME = "Model Trainer stage" # Stage name define karna zaroori hai
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        
        obj =ModelTrainerPipeline()
        obj.intantiate_model_trainer_pipeline() # .main() call karna mat bhulna jo humne pipeline mein banaya hai
        
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
    
    

    
    
    
    