import os 
import yaml
from src.Crypto import logger
from ensure import ensure_annotations
from pathlib import Path
from box import ConfigBox
from box.exceptions import BoxValueError
import json

@ensure_annotations
def read_yaml(yaml_path: Path)->ConfigBox:
    try:
        with open(yaml_path) as f:
            content = yaml.safe_load(f)
            logger.info(f"Yaml File :{yaml_path} Read Sucessfully✅")
            return ConfigBox(content)
    except BoxValueError:
        logger.error("Yaml File is Empty Check ur Path Again ❌")
        raise ValueError("Yaml File is Empty Check ur Path Again ❌")
    except Exception as e:
        logger.error(f"Error:  \n {e}")
        raise e
    
@ensure_annotations
def create_directories(dirct:list):
    try:
        for path in dirct:
            os.makedirs(path,exist_ok=True)
            logger.info(f"Folder Created Sucessfully: {path}" )
    except Exception as e:
        logger.error(f"Some Error Occured: \n {e}")
        raise e
    

@ensure_annotations
def save_json(path,data):
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
            logger.debug(f"JSON Saved Sucessfully... to {path}")
    except Exception as e:
        logger.error(e)
        raise e
    

        
    
    

