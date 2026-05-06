# This will make the Template of he project strucutre 
# we will write the Automated Script that will help to crate the automatic  project strucutere 


import os
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO, # Level set karta hai (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s', # Time, Level aur Message ka format
    datefmt='%d-%m-%Y %I:%M:%S %p' # Date aur Time ka dikhne wala format
)

project_name = "Crypto"

list_of_files=[
    
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/helper.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "main.py",
    "Dockerfile",
    "setup.py",
    "research/research.ipynb",
    "templates/index.html"
    
    
]

for filepath in list_of_files:
    filepath=Path(filepath)
    filedir,filename = os.path.split(filepath)
    
    if filedir != "":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating Directory {filedir} for the file: {filename}")
    
    ## Yeh line "src/project_name/components/__init__.py" naam ki file bana degi.   
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath,'w') as f:
            pass 
            logging.info(f"Creating Empty File: {filepath}")
    else:
        logging.info(f"{filename} already exists")
        

        
    