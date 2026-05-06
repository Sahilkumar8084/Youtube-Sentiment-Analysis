import os
from src.Crypto.entity.config_entity import DataTransformationConfig
from src.Crypto.utils.helper import create_directories
from src.Crypto import logger
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer
import numpy as np


class DataTransformationComponent:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.df = pd.read_csv(self.config.data_path)
        self.model = SentenceTransformer('all-mpnet-base-v2')
        # Check if column exists before dropping to avoid error
        if 'Unnamed: 0' in self.df.columns:
            self.df.drop(columns=['Unnamed: 0'], inplace=True)
            
    def remove_null(self):
        # Seedha dropna bhi kar sakte ho, agar null hai toh hat jayenge
        initial_shape = self.df.shape[0]
        self.df.dropna(inplace=True)
        new_shape = self.df.shape[0]
        logger.info(f"Removed {initial_shape - new_shape} null rows.")
            
    def remove_duplicate(self):
        if self.df.duplicated().sum() > 0:
           self.df.drop_duplicates(inplace=True)
           logger.info("Duplicates removed.")
           
    def label_encode(self):
        self.label_map = {"POSITIVE": 1, "NEGATIVE": 0}
        self.df['Label'] = self.df['Label'].map(self.label_map)

        
    def split_data(self):
        # self.train aur self.test banaya taaki poori class mein use ho sake
        self.train, self.test = train_test_split(
            self.df, 
            test_size=0.25, 
            random_state=42,
            stratify=self.df['Label'] # Recommendation for classification
        )
        logger.info(f"Data split into train ({self.train.shape}) and test ({self.test.shape})")
        
    def save_data(self):
        # Directory check
        os.makedirs(self.config.root_dir, exist_ok=True)
        
        # self.train aur self.test use kiya
        train_path = os.path.join(self.config.root_dir, 'train.csv')
        test_path = os.path.join(self.config.root_dir, 'test.csv')
        
        self.train.to_csv(train_path, index=False)
        self.test.to_csv(test_path, index=False)
        logger.info(f"Files saved at: {self.config.root_dir}")
     
    
        
    def text_encode(self):
        self.train_df = pd.read_csv(r"artifacts\data_transformation\train.csv")
        self.test_df = pd.read_csv(r"artifacts\data_transformation\test.csv")
        train_embeddings = self.model.encode(self.train_df['text'].tolist(),show_progress_bar=True)
        test_embeddings = self.model.encode(self.test_df['text'].tolist(),show_progress_bar=True)
        
        create_directories(["artifacts/embeddings"])
        joblib.dump(self.model, self.config.vectorizer_path)
        logger.debug(f"Model saved successfully! Download  from the files tab.")
        np.save(os.path.join("artifacts/embeddings", "train_embeddings.npy"), train_embeddings)
        np.save(os.path.join("artifacts/embeddings", "test_embeddings.npy"), test_embeddings)
        logger.info(f"Embeddings and Model saved successfully!")
      
    def transformation(self):
        # Saare steps sequence mein
        self.remove_null()
        self.remove_duplicate()
        self.label_encode()
        self.split_data()
        self.save_data()
        self.text_encode() # <--- Isse tabhi chalayein agar aapko embeddings save karni ho

        print("All Done...✅")