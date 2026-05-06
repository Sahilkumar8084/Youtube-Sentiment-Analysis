
from src.Crypto.entity.config_entity import DataReportConfig
from src.Crypto import logger
import feedparser
import pandas as pd
from transformers import pipeline
import torch
from sources import Links,links
import sqlite3
from googleapiclient.discovery import build
from dotenv import load_dotenv
import sys

class DataReportComponent:
    def __init__(self,config: DataReportConfig):
        self.config = config
        self.df = pd.read_csv(self.config.data_path)
        self.df.drop(columns=['Unnamed: 0'],inplace=True)
        
        
    def generate_eda_report(self, report_path="data_report.txt"):
        """Saves DataFrame summary and statistics to a text file."""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*50 + "\n")
            f.write("       DEEP EDA REPORT - CRYPTO GUARDIAN\n")
            f.write("="*50 + "\n\n")

            # 1. Dataset Shape
            f.write(f"Dataset Shape: {self.df.shape}\n")
            
            f.write("-" * 30 + "\n")

            # 2. Info (Thoda tricky hai isliye 'buf' use karenge)
            f.write("\n1. DATASET INFO:\n")
            import io
            buffer = io.StringIO()
            self.df.info(buf=buffer)
            f.write(buffer.getvalue())
            f.write("-" * 30 + "\n")

            # 3. Statistical Summary (Describe)
            f.write("\n2. STATISTICAL SUMMARY:\n")
            f.write(self.df.describe(include='all').to_string())
            f.write("\n" + "-" * 30 + "\n")

            # 4. Null Values
            f.write("\n3. NULL VALUES COUNT:\n")
            f.write(self.df.isnull().sum().to_string())
            f.write("\n" + "-" * 30 + "\n")

            # 5. Duplicate Rows
            f.write(f"\n4. DUPLICATE ROWS: {self.df.duplicated().sum()}\n")
            
            f.write("\n" + "="*50 + "\n")
            f.write("REPORT GENERATED SUCCESSFULLY\n")
            
        print(f"Bhai, EDA report save ho gayi hai yahan: {report_path}")
        logger.info(f"Bhai, EDA report save ho gayi hai yahan: {report_path}")
    
    def data_report(self):
        self.generate_eda_report(self.config.report_path)
        logger.info("Data Report Generated Sucessfully...✅")
    