import os 
import sys
import logging

logging_str="[%(asctime)s - %(module)s - %(levelname)s - %(message)s]"
log_dir = "logs"
log_filepath = os.path.join(log_dir,"logging.log")
os.makedirs(log_dir,exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    
    datefmt='%d-%m-%Y %I:%M:%S %p',
    
    handlers=[
        logging.FileHandler(log_filepath,encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
    
)

logger = logging.getLogger() #yaha pe Logger aek objet ban gaya hia jo baas call karnge aur bass kam karna xhalu hoo jayega


# logger.info("I ma in the __INIT__.py file me hu")