from src.Crypto import logger
import feedparser
import pandas as pd
from transformers import pipeline
import torch
from sources import Links,links
import sqlite3
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from src.Crypto.entity.config_entity import DataIngestionConfig


class DataIngestionComponent:
    def __init__(self,config: DataIngestionConfig):
        self.config = config
        load_dotenv()
        self.v_ids = [i.split("v=")[1] for i in links]
        print("VIDEO IDS CONST: ",self.v_ids)
        logger.debug("Load Dot Env  and V_ids is loaded Sucessfully.....")


    def initialize_db(self):
        conn = sqlite3.connect(self.config.local_data_files)
        cursor = conn.cursor()
        
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS comments (
                           comment_id TEXT PRIMARY KEY,
                           video_id TEXT,
                            text TEXT,
                            Label TEXT,
                            Score Float32
                       )
                       ''') #This one Create the comments Table
        logger.debug("COMMENTS TABLE Create Scessfully...")
        cursor.execute(''' CREATE TABLE IF NOT EXISTS progress(
            video_id TEXT PRIMARY KEY,
            next_page_token TEXT        
            
            
            )''') # This one creates the Progress Table in the DataBase
        logger.debug("PROGReSS Table Created Sucessully.......")
        conn.commit()
        return conn
    
    def fetch_comments(self,video_id,youtube,db_conn):
        cursor = db_conn.cursor()
        
        #First We have to check whether do we have something saved Tokens to Resume???
        cursor.execute("  SELECT next_page_token FROM progress WHERE video_id = ?",(video_id,))
        #In Python, when you pass a single variable into a SQL query using a tuple, you must include a trailing comma. Without it, Python treats the parentheses as simple grouping, and sqlite3 will try to iterate over the string video_id character by character.
        
        result = cursor.fetchone()
        next_token = result[0] if result else None
        
        print("Fetching The Main Coments for: ",video_id)
        logger.info(f"Fetching The Main Coments for: {video_id}")
        
        while True:
            try:
                logger.info("Entered the Fetching Zone...")
                request = youtube.commentThreads().list(
                    part = "snippet",
                    videoId= video_id,
                    maxResults = 100,
                    pageToken = next_token,
                    fields  ="nextPageToken,items(id,snippet/topLevelComment/snippet/textDisplay)"
                    
                )
                logger.debug("Requestare Got Generated... ")
                response = request.execute()
                
                logger.debug(f"Response Generated... \n {response} ")
                #Lets Make the Batch 
                batch = []
                logger.debug("Batch Procesing IS Started...")
                print("I Am WORKING>>>>>>>>>>>>>>>>>")
                for item in response.get("items",[]):
                    
                    c_id = item['id']
                    print("C_ID: ",c_id)
                    text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    print("TEXT: ",text)
                    batch.append((c_id,video_id,text))
                    
                    
                logger.debug("Batch Processing Finished...")    
                cursor.executemany("INSERT OR IGNORE INTO comments VALUES (?,?,?,NULL,NULL)",batch)
                
                next_token = response.get("nextPageToken")
                cursor.execute("INSERT OR REPLACE INTO progress VALUES(?,?)",(video_id,next_token))
                
                db_conn.commit()
                
                if not next_token:
                    logger.debug(f"There is No New Token: {next_token}")
                    print(f"Done with video: {video_id}")
                    logger.debug("FETCHING STOPPED..........")
                    break
            
            except Exception as e:
                print(f"Error or Quota Limit: {e}")
                logger.error(f"Error or Quota Limit: {e}")
                
                # Yahan token save ho chuka hai, next time run karoge toh yahin se shuru hoga
                break
        
    def save_comments(self):
        try:
            
            api_key = os.getenv("API_KEY")
            logger.info("API_KEY Loaded Sucessfully....")
            youtube = build("youtube", "v3", developerKey=api_key)
            logger.info("Youtube Build Sucessfully....")

            db_conn = self.initialize_db()
            logger.info("DB Connection Established Sucessfully....")

            # v_ids = ["6MI0f6YjJIk"]

            for v_id in self.v_ids:
                print("VIDEO_ID: ",v_id)
                self.fetch_comments(v_id, youtube, db_conn)
                logger.info("Fetching the Comments to the Data...")

            print("All Done..........")
            db_conn.close()
        except Exception as e:
            logger.error("Something Went Wrong! ",e)
            raise e
                
                    