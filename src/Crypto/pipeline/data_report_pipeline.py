from src.Crypto.components.data_report_component import DataReportComponent
from src.Crypto.components.data_labelling_component import DataLabellingComponent
from src.Crypto.config.configuration import ConfigurationManager
from src.Crypto.components.data_ingestion_component import DataIngestionComponent
from src.Crypto import logger


class DataReportPipeline:
    def __init__(self):
        pass
    
    def intantiate_data_report_pipeline(self):
        
        #Creatign the  Data Ingestion Pipeline
        try:
            cfm = ConfigurationManager()
            data_report = cfm.get_data_report()
            data_report_component = DataReportComponent(data_report)
            
            data_report_component.generate_eda_report()
            data_report_component.data_report()
            # data_ingestion_component.save_comments()
            logger.info("Pipeline Ran Sucessfully...✅")
        except Exception as e:
            logger.error("Pipeline Error...❌")
            raise e

        

