from src.Crypto.entity.config_entity import DataLabellingConfig
from src.Crypto import logger
import feedparser
import pandas as pd
from transformers import pipeline
import torch
from sources import Links,links
import sqlite3
from googleapiclient.discovery import build
from dotenv import load_dotenv
import sqlite3

class DataLabellingComponent:
    def __init__(self,config:DataLabellingConfig):
        self.config = config
        self.conn = sqlite3.connect(self.config.database_path)
        self.cursor = self.conn.cursor()
        logger.info("Connnection IS Established from the DATA Labelling Componennt")
        

    
    def fetch_database(self):
           
        logger.debug("Entered into the Fetch DataBAse")
        try:
            text = self.cursor.execute(
                    ''' SELECT text FROM comments'''
                ).fetchall()
            self.conn.commit()
            logger.debug("Texts and the Connecton has benn All Set... Returning the Texts")
        except Exception as e:
            logger.error("Error Occured...❌")
            raise e
        return text
    
    # def alter_db(self):
    #     self.cursor.execute(''' ALTER TABLE comments ADD COLUMN label TEXT''')
    #     self.cursor.execute(''' ALTER TABLE comments ADD COLUMN score float32''')
    #     self.conn.commit()
        
    def label_db(self):
        logger.debug("Enterered into the Label_DB")
        device = 0 if torch.cuda.is_available() else -1
        print(f"Using device: {'GPU' if device == 0 else 'CPU'}")
        logger.debug(f"Using device: {'GPU' if device == 0 else 'CPU'}")
        sentiment_pipeline = pipeline("sentiment-analysis", device=device)
        # conn = sqlite3.connect("sample_data.db")
        # cursor = conn.cursor()
        try:
            logger.info("Fetchign the Data Frome the DataBase...")
            texts = self.fetch_database()
            # print( "texts: \n ",texts[10:20])
            logger.debug( "Sample texts: \n ",texts[10:20])
            for i in range(len(texts)):
                # print(f"texts: {texts[i][0]}")
                results = sentiment_pipeline(texts[i][0])
                logger.debug("Results are Generating...")
                # print("Results: \n " ,results[0])
                # print("Label: " ,results[0]['label'])
                # print("Score: " ,results[0]['score'])
                
                self.cursor.execute(""" UPDATE comments set "label" = ? ,'score'=?  where "text" = ?""",(results[0]['label'],results[0]['score'],texts[i][0]))
                logger.debug(f"Data Updated of iter: {i}--> {texts[i][0]}")
                self.conn.commit()
            print("All Done...✅")
            logger.info("All Done...✅")
        except Exception as e:
            logger.error("Soething Went Wrong...❌")
            logger.error(e)
            raise e