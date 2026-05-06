
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import os
from src.Crypto.entity.config_entity import EDAReportConfig
from src.Crypto import logger
import pandas as pd
import seaborn as sns

class EDAReportComponent:
    def __init__(self, config: EDAReportConfig):
        self.config = config
        self.df = pd.read_csv(self.config.data_path)
    
    # Yahan output_dir add kiya taaki function ko pata chale save kahan karna hai
    def save_wordcloud(self, data_subset, title, filename, output_dir):
        text_data = ' '.join(data_subset['text'].astype(str))
        if len(text_data.strip()) > 0:
            wc = WordCloud(width=800, height=400, background_color='white').generate(text_data)
            plt.figure(figsize=(10, 5))
            plt.imshow(wc, interpolation='bilinear')
            plt.title(title)
            plt.axis('off')
            plt.savefig(os.path.join(output_dir, filename)) # Better way to join paths
            plt.close()
        else:
            print(f"Bhai, {title} ke liye data nahi mila!")

    def download_eda_report(self, output_dir): 
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Directory '{output_dir}' created.")

        # self.df use kiya har jagah
        self.df['char_count'] = self.df['text'].astype(str).apply(len)
        self.df['word_count'] = self.df['text'].astype(str).apply(lambda x: len(x.split()))

        # Label filtering from self.df
        pos_df = self.df[self.df['Label'].isin([1, 'POSITIVE'])]
        neg_df = self.df[self.df['Label'].isin([0, 'NEGATIVE'])]
        
        # --- Plot 1 ---
        plt.figure(figsize=(12, 6))
        sns.kdeplot(pos_df['word_count'], fill=True, color="green", label="Positive")
        sns.kdeplot(neg_df['word_count'], fill=True, color="red", label="Negative")
        plt.title("Word Count Distribution by Sentiment")
        plt.legend()
        plt.savefig(f"{output_dir}/word_count_dist.png")
        plt.close()

        # --- Plot 2 (Fixed self.df) ---
        plt.figure(figsize=(12, 6))
        sns.histplot(self.df["word_count"], bins=30, color='skyblue')
        plt.title("Word Length Distribution")
        plt.savefig(f"{output_dir}/word_length_hist.png")
        plt.close()
        
        # --- WordCloud (Added output_dir parameter) ---
        self.save_wordcloud(pos_df, "Positive Comments Cloud", "wc_positive.png", output_dir)
        self.save_wordcloud(neg_df, "Negative Comments Cloud", "wc_negative.png", output_dir)
        
        # --- Plot 3 (Fixed self.df) ---
        plt.figure(figsize=(8, 5))
        sns.histplot(data=self.df, x="Score", hue="Label", kde=True, element="step", bins=20)
        plt.title("Model Confidence Score Distribution")
        plt.savefig(f"{output_dir}/score_distribution.png")
        plt.close()
        
        # --- Plot 4 (Fixed self.df) ---
        plt.figure(figsize=(12, 6))
        sns.histplot(data=self.df, x="Score", hue="Label", kde=True,
                    element="step", palette="viridis", bins=50)
        plt.xlim(0.90, 1.0)
        plt.title("Deep Analysis: High Confidence Score (0.90 - 1.0)")
        plt.grid(axis='y', alpha=0.3)
        plt.savefig(f"{output_dir}/high_confidence_zoom.png")
        plt.close()

        print(f"Saaare graphs '{output_dir}' folder mein save ho gaye hain!")

    def download(self):
        # Yahan config se path uthaya
        self.download_eda_report(self.config.output_report)
        logger.info(f"Reports Downloaded Successfully...{self.config.output_report}...✅")