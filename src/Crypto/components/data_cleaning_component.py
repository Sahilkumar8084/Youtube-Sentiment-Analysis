from src.Crypto.entity.config_entity import DataCleaningConfig
from src.Crypto import logger
import pandas as pd
from transformers import pipeline
import re
import emoji
import nltk
from nltk.corpus import stopwords


class DataCleaningComponent:
    def __init__(self,config: DataCleaningConfig):
        self.config = config
        
        self.df = pd.read_csv(self.config.data_path)
        logger.info(f"file REad Sucessfully...✅")
        print(self.df.head())
        
        # try:
        #     self.stopwords.words('english')
        #     self.STOPWORDS = set(self.stopwords.words('english'))

        #     logger.debug(f"Using the StopWords ")
        # except LookupError:
        #     nltk.download('stopwords')        
        #     self.STOPWORDS = set(self.stopwords.words('english'))
        #     logger.debug(f"Using the NLTK Download")
        
        try:
            self.STOPWORDS = set(stopwords.words('english'))
            logger.debug("Using existing StopWords")
        except LookupError:
            nltk.download('stopwords')        
            self.STOPWORDS = set(stopwords.words('english'))
            logger.debug("NLTK Stopwords downloaded")
            
    def remove_urls(self,text):
        """Removes URLs from the text."""
        self.url_pattern = re.compile(r'https?://\S+|www\.\S+')
        return self.url_pattern.sub(r'', text)

    def remove_emojis(self,text):
        """Removes emojis from the text."""
        return emoji.demojize(text, delimiters=("", "")) # Converts emojis to text like :smiley_face: then remove

    def remove_special_characters(self,text):
        """Removes special characters, keeping only alphanumeric and spaces."""
        # Remove HTML entities like &#39; first
        self.text = re.sub(r'&#\d+;', '', text)
        self.text = re.sub(r'&amp;', '', text)
        self.text = re.sub(r'&quot;', '', text)
        # Keep alphanumeric characters and spaces
        self.pattern = re.compile(f'[^a-zA-Z0-9\s]')
        return self.pattern.sub('', text)

    def remove_stopwords(self,text):
        """Removes stopwords from the text."""
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in self.STOPWORDS]
        return ' '.join(filtered_words)

    def clean_text(self,text):
        """Enhanced cleaning for YouTube comments."""
        # 1. Lowercase
        text = text.lower()
        logger.info("Texts Got Lowered...")
        # Remove URLs
        text = self.remove_urls(text)
        logger.info("URLs Removed...")

        # Handle Emojis
        text = self.remove_emojis(text)
        logger.info("Emojis Are Handeled...")
        # Remove HTML entities and Special Characters
        text = self.remove_special_characters(text)
        logger.info("Special Charachters Removed Sucessfully....")
        # Remove Repeated Characters (e.g., 'looooove' -> 'love')
        text = re.sub(r'(.)\1{2,}', r'\1', text)
        logger.info("Repeaded Chrachters Are Removed Sucessfully...")
        # Remove Extra Whitespaces
        text = re.sub(r'\s+', ' ', text).strip()
        logger.info("Extra White Spaces are REmoved....")
        # Remove Stopwords
        text = self.remove_stopwords(text)
        logger.info("StopWords Removed Sucessfully...")

        return text

    def cleanning(self):
        self.df['text']= self.df['text'].astype(str).apply(self.clean_text)  
        self.df.drop(columns=[ 'comment_id', 'video_id'],inplace=True)
        logger.debug("All the Texts Are Cleaned... SucessFully...✅")

    def save_csv(self):
        self.df.to_csv(self.config.saved_data)
        logger.info(f"Data Saved Sucessfully... to {self.config.saved_data}")