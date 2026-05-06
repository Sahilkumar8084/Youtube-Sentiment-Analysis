from src.Crypto.entity.config_entity import DataConversionConfig
from src.Crypto import logger
import feedparser
import pandas as pd
from transformers import pipeline
import torch
import sqlite3
import csv

class DataConversionComponent:
    def __init__(self,config: DataConversionConfig):
        self.config = config
        
    def data_conversion(self,db_name,table_name,csv_name):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        
        headers = [description[0] for description in cursor.description]
        
        with open(csv_name,'w',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(cursor.fetchall())
            
        conn.close()
        
    def csv_conversion(self):
        try:
            self.data_conversion(self.config.db_path,self.config.table_name,self.config.converted_data_path)
        except Exception as e:
            
            raise e
        



