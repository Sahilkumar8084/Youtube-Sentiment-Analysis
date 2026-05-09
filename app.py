# # app.py
# import streamlit as st
# import pandas as pd
# import mlflow.sklearn
# import plotly.express as px
# from googleapiclient.discovery import build
# import re
# import os
# from dotenv import load_dotenv
# import numpy as np

# import numpy as np
# import pickle
# import json
# import mlflow
# import mlflow.sklearn
# from mlflow.tracking import MlflowClient
# from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
# from src.Crypto import logger
# import pandas as pd
# import joblib
# from sklearn.pipeline import Pipeline
# import matplotlib.pyplot as plt
# from sklearn.metrics import RocCurveDisplay, PrecisionRecallDisplay, roc_auc_score
# import os
# from dotenv import load_dotenv
# load_dotenv()


# # Page setup
# st.set_page_config(page_title="YouTube Sentiment Analyzer", layout="wide")
# st.title("🎬 YouTube Comment Sentiment Analyzer")

# # YouTube se video ID nikalo
# def get_video_id(url):
#     pattern = r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]+)'
#     match = re.search(pattern, url)
#     return match.group(1) if match else None

# # YouTube se comments fetch karo
# @st.cache_data
# def fetch_comments(video_url, max_results=50):
#     api_key = os.getenv('API_KEY')
#     youtube = build('youtube', 'v3', developerKey=api_key)
#     video_id = get_video_id(video_url)
    
#     comments = []
#     request = youtube.commentThreads().list(
#         part="snippet",
#         videoId=video_id,
#         maxResults=max_results,
#         textFormat="plainText"
#     )
    
#     while request and len(comments) < max_results:
#         response = request.execute()
#         for item in response['items']:
#             comment = item['snippet']['topLevelComment']['snippet']
#             comments.append({
#                 'text': comment['textDisplay'],
#                 'author': comment['authorDisplayName'],
#                 'likes': comment['likeCount']
#             })
        
#         if 'nextPageToken' in response:
#             request = youtube.commentThreads().list(
#                 part="snippet", videoId=video_id,
#                 pageToken=response['nextPageToken'],
#                 maxResults=min(50, max_results - len(comments)),
#                 textFormat="plainText"
#             )
#         else:
#             break
    
#     return pd.DataFrame(comments)

# # Model load karo
# @st.cache_resource
# def load_model():
#     mlflow.set_tracking_uri("https://dagshub.com/sahilkumarrock8084/Youtube-Sentiment-Analysis.mlflow")
#     try:
#         vector = joblib.load(r"artifacts\data_transformation\vectorizer.joblib")
#         model = mlflow.sklearn.load_model("models:/sentiment_model/Production")
#         st.sidebar.success("✅ Production Model Loaded!")
#     except:
#         st.sidebar.warning("⚠️ Production model nahi mila, fallback use kar rahe hain")
#         vector = joblib.load(r"artifacts\data_transformation\vectorizer.joblib")
#         model = joblib.load(r"artifacts\model_training\model.joblib")

#         # model = Pipeline([
#         #     ('vectorizer', TfidfVectorizer()),
#         #     ('classifier', RandomForestClassifier())
#         # ])
#         # Quick train on sample data
#         # model.fit(['good', 'bad', 'great', 'terrible'], [1, 0, 1, 0])
#     return model,vector

# # Sidebar
# with st.sidebar:
#     st.header("⚙️ Settings")
#     url = st.text_input("YouTube Video URL", placeholder="https://youtube.com/watch?v=...")
#     num_comments = st.slider("Number of Comments", 10, 200, 50)
#     analyze_btn = st.button("🔍 Analyze Comments", type="primary")

# # Main logic
# if analyze_btn and url:
#     try:
#         # Fetch comments
#         with st.spinner("📥 Comments fetch ho rahe hain..."):
#             df = fetch_comments(url, num_comments)
        
#         if df.empty:
#             st.error("Koi comments nahi mile!")
#         else:
#             # Predict
#             with st.spinner("🤖 AI analyze kar raha hai..."):
#                 model,vector = load_model()
#                 t = vector.encode(df['text'].tolist())
#                 predictions = model.predict(t)
#                 df['Sentiment'] = ['Positive 😊' if p == 1 else 'Negative 😞' for p in predictions]
            
#             # Show results
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.metric("Total Comments", len(df))
#             with col2:
#                 st.metric("Positive 😊", sum(predictions == 1))
#             with col3:
#                 st.metric("Negative 😞", sum(predictions == 0))
            
#             # Charts
#             col1, col2 = st.columns(2)
#             with col1:
#                 fig = px.pie(
#                     values=[sum(predictions == 1), sum(predictions == 0)],
#                     names=['Positive', 'Negative'],
#                     title='Sentiment Distribution'
#                 )
#                 st.plotly_chart(fig)
            
#             with col2:
#                 fig = px.histogram(df, x='Sentiment', title='Sentiment Count')
#                 st.plotly_chart(fig)
            
#             # Comments table
#             st.subheader("📝 Comments Analysis")
#             st.dataframe(df[['text', 'Sentiment', 'author', 'likes']], use_container_width=True)
            
#             # Download
#             csv = df.to_csv(index=False)
#             st.download_button("📥 Download Results", csv, "results.csv", "text/csv")
            
#     except Exception as e:
#         st.error(f"Error: {str(e)}")
#         st.info("YouTube API key sahi hai? .env file check karo")
        
# elif analyze_btn:
#     st.warning("Please enter a YouTube URL")



import streamlit as st
import pandas as pd
import plotly.express as px
from googleapiclient.discovery import build
import re
import os
from dotenv import load_dotenv
import joblib
import mlflow.sklearn
from wordcloud import WordCloud
import matplotlib.pyplot as plt

load_dotenv()

# Page setup
st.set_page_config(page_title="YouTube Sentiment Pro", layout="wide", page_icon="🎬")

# Custom CSS for styling
st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stMetric { background-color: #000000; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgb(250, 250, 250); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 YouTube Comment Sentiment Dashboard")

# YouTube Helpers
def get_video_id(url):
    pattern = r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

@st.cache_data
def fetch_comments(video_url, max_results=50):
    api_key = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_id = get_video_id(video_url)
    
    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet", videoId=video_id, maxResults=max_results, textFormat="plainText"
        )
        while request and len(comments) < max_results:
            response = request.execute()
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'text': comment['textDisplay'],
                    'author': comment['authorDisplayName'],
                    'likes': comment['likeCount'],
                    'published_at': comment['publishedAt']
                })
            if 'nextPageToken' in response:
                request = youtube.commentThreads().list(
                    part="snippet", videoId=video_id,
                    pageToken=response['nextPageToken'],
                    maxResults=min(50, max_results - len(comments))
                )
            else: break
    except Exception as e:
        st.error(f"API Error: {e}")
    return pd.DataFrame(comments)

@st.cache_resource
def load_model():
    # Note: MLflow URI and paths remains same as your original
    try:
        mlflow.set_tracking_uri("https://dagshub.com/sahilkumarrock8084/Youtube-Sentiment-Analysis.mlflow")
        vector = joblib.load(r"https://dagshub.com/sahilkumarrock8084/Youtube-Sentiment-Analysis/src/78e70e9533f34dc0a06fa05d5e16ab0c898546c7/artifacts/data_transformation/vectorizer.joblib")
        
        model = mlflow.sklearn.load_model("models:/sentiment_model/Production")
        return model, vector, "Production"
    except:
        vector = joblib.load(r"https://dagshub.com/sahilkumarrock8084/Youtube-Sentiment-Analysis/src/78e70e9533f34dc0a06fa05d5e16ab0c898546c7/artifacts/data_transformation/vectorizer.joblib")
        model = joblib.load(r"https://dagshub.com/sahilkumarrock8084/Youtube-Sentiment-Analysis/src/3cb7da03efad6e94c0bb92baf0745b90272027f2/artifacts/model_training/model.joblib")
        return model, vector, "Fallback"

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    url = st.text_input("YouTube URL", placeholder="https://youtube.com/watch?v=...")
    num_comments = st.slider("Max Comments", 20, 500, 100)
    analyze_btn = st.button("🔍 Analyze Now", type="primary")
    st.divider()
    st.info("Bhai, model production se load hota hai automatic!")

if analyze_btn and url:
    df = fetch_comments(url, num_comments)
    
    if not df.empty:
        model, vector, status = load_model()
        
        # Predictions
        # Assuming your vectorizer has a 'transform' or 'encode' method
        # Adjust 'encode' to 'transform' if it's a standard Sklearn vectorizer
        text_data = vector.transform(df['text']) if hasattr(vector, 'transform') else vector.encode(df['text'].tolist())
        preds = model.predict(text_data)
        df['Sentiment_Score'] = preds
        df['Sentiment'] = df['Sentiment_Score'].map({1: 'Positive 😊', 0: 'Negative 😞'})

        # --- 1. METRICS ROW ---
        total_c = len(df)
        unique_c = df['text'].nunique()
        pos_count = sum(preds == 1)
        # 3. Sentiment Rating out of 10
        rating = round((pos_count / total_c) * 10, 1)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Comments", total_c)
        m2.metric("Unique Comments", unique_c)
        m3.metric("Positive Ratio", f"{(pos_count/total_c)*100:.1f}%")
        m4.metric("Video Rating", f"{rating}/10")

        st.divider()

        # --- 2. VISUALIZATIONS ---
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            # Pie Chart
            fig_pie = px.pie(df, names='Sentiment', title='Overall Sentiment Breakdown',
                             color='Sentiment', color_discrete_map={'Positive 😊':'#2ecc71', 'Negative 😞':'#e74c3c'})
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_right:
            # 4. Word Cloud
            st.subheader("☁️ Trending Words")
            all_text = " ".join(df['text'].tolist())
            wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(all_text)
            fig_wc, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig_wc)

        # --- 3. TOP COMMENTS & DATA ---
        st.divider()
        c1, c2 = st.columns([1, 1])
        
        with c1:
            # 5. Top 5 Liked Comments
            st.subheader("🔥 Top 5 Liked Comments")
            top_5 = df.nlargest(5, 'likes')[['author', 'likes', 'text', 'Sentiment']]
            for _, row in top_5.iterrows():
                st.markdown(f"**{row['author']}** ({row['likes']} 👍) - {row['Sentiment']}")
                st.caption(f"{row['text'][:150]}...")
                st.write("---")

        with c2:
            st.subheader("📊 Sentiment distribution")
            fig_bar = px.histogram(df, x='Sentiment', color='Sentiment', 
                                   color_discrete_map={'Positive 😊':'#2ecc71', 'Negative 😞':'#e74c3c'})
            st.plotly_chart(fig_bar, use_container_width=True)

        # 6. Full Data Table
        with st.expander("📂 View 10 Sample Comments Data"):
            st.dataframe(df.iloc[:11], use_container_width=True)
            csv = df.to_csv(index=False)
            st.download_button("📥 Download CSV", csv, "yt_analysis.csv", "text/csv")

    else:
        st.error("Bhai comments nahi mile. Check karo video public hai ya nahi.")