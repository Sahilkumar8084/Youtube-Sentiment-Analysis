from src.Crypto.entity.config_entity import ModelTrainingConfig
from src.Crypto import logger
import pandas as pd
from transformers import pipeline
import numpy as np
from imblearn.over_sampling import SMOTE
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score,f1_score, classification_report
import joblib
import os

class ModelTrainerComponent:
    def __init__(self, config: ModelTrainingConfig):
        self.config = config
        
        # 1. Data Loading
        self.df = pd.read_csv(self.config.train_data_path)
        self.test_df = pd.read_csv(self.config.test_data_path)
        
        # 2. Embeddings load karna (Train aur Test dono ki zaroorat padegi)
        self.x_train_emb = np.load(self.config.train_embedding) 
        self.x_test_emb = np.load(self.config.test_embedding) # <--- Test embeddings bhi chahiye!
        
        self.y_train = self.df['Label']
        self.y_test = self.test_df['Label']
        
        self.smote = SMOTE(random_state=42)

    def prepare_data(self):
        # self.smote use hoga aur result ko self mein save karein taaki train function use kar sake
        self.x_resampled, self.y_resampled = self.smote.fit_resample(self.x_train_emb, self.y_train)
        logger.info(f"Oversampling complete: {Counter(self.y_resampled)}")
        
    def train_model(self):
        logger.info("Training SVM Model...")
        
        # Parameters ke naam sahi karein (C capital hota hai)
        clf = SVC(
            C=self.config.p_c,
            gamma=self.config.p_gamma, # Gamma ki spelling theek ki
            kernel=self.config.p_kernel,
            probability=True, # Recommendation: Prediction scores ke liye zaroori hai
            class_weight='balanced'
        )
        
        # Train on resampled embeddings
        clf.fit(self.x_resampled, self.y_resampled)
        
        # 3. CRITICAL FIX: Predict hamesha test EMBEDDINGS par hoga, text par nahi
        y_pred = clf.predict(self.x_test_emb)
        
        # Metrics calculation
        acc = accuracy_score(self.y_test, y_pred)
        f1 = f1_score(self.y_test, y_pred, average='weighted')
        
        logger.info(f"Test Accuracy: {acc}")
        logger.info(f"Test F1 Score: {f1}")
        
        # Model saving
        os.makedirs(os.path.dirname(self.config.model_path), exist_ok=True)
        joblib.dump(clf, self.config.model_path)
        
        logger.info(f"Model saved at: {self.config.model_path}")