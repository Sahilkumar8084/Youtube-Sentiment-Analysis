

# YouTube Sentiment Analysis

An end-to-end MLOps pipeline for analyzing viewer sentiment from YouTube comments with real-time dashboard visualization.

## 🎯 Features

- **Automated Data Pipeline**: Fetches YouTube comments via Data API v3 and processes them through ingestion, cleaning, transformation, and labeling stages <cite repo="Sahilkumar8084/Youtube-Sentiment-Analysis" path="app.py" start="196-226" />
- **ML Model Training**: Uses SVM classifier with SMOTE for handling class imbalance <cite repo="Sahilkumar8084/Youtube-Sentiment-Analysis" path="src/Crypto/components/model_trainer_component.py" start="33-48" />
- **Model Registry**: Automatic model promotion to Production via MLflow based on F1-score performance <cite repo="Sahilkumar8084/Youtube-Sentiment-Analysis" path="src/Crypto/components/model_evaluation_component.py" start="95-124" />
- **Real-time Dashboard**: Streamlit interface for sentiment analysis with visualizations <cite repo="Sahilkumar8084/Youtube-Sentiment-Analysis" path="app.py" start="178-334" />
- **Interactive Visualizations**: Pie charts, word clouds, histograms, and sentiment metrics <cite repo="Sahilkumar8084/Youtube-Sentiment-Analysis" path="app.py" start="274-326" />

## 🚀 Quick Start

### Prerequisites

- Python 3.10.11 <cite repo="Sahilkumar8084/Youtube-Sentiment-Analysis" path="runtime.txt" start="1-1" />
- YouTube Data API v3 Key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Sahilkumar8084/Youtube-Sentiment-Analysis.git
cd Youtube-Sentiment-Analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file in the root directory and add your YouTube API key:
```
API_KEY=your_youtube_api_key_here
```

### Running the Dashboard

Start the Streamlit application:
```bash
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`

## 📊 Usage

1. **Enter YouTube URL**: Paste any YouTube video URL in the sidebar
2. **Configure Analysis**: Adjust the number of comments to analyze (20-500)
3. **Analyze**: Click "🔍 Analyze Now" to fetch comments and run sentiment analysis
4. **View Results**: 
   - Overall sentiment breakdown (pie chart)
   - Trending words (word cloud)
   - Top liked comments with sentiment
   - Sentiment distribution histogram
   - Download results as CSV

## 🏗️ Project Structure

```
Youtube-Sentiment-Analysis/
├── app.py                          # Streamlit dashboard
├── main.py                         # Pipeline orchestration
├── requirements.txt                # Python dependencies
├── config/
│   ├── config.yaml                 # Pipeline configuration
│   ├── params.yaml                 # Model parameters
│   └── schema.yaml                 # Data schema
├── src/Crypto/
│   ├── components/                 # Pipeline components
│   │   ├── data_ingestion_component.py
│   │   ├── data_cleaning_component.py
│   │   ├── data_transformation_component.py
│   │   ├── model_trainer_component.py
│   │   └── model_evaluation_component.py
│   ├── pipeline/                   # Pipeline orchestration
│   ├── config/                     # Configuration management
│   └── entity/                     # Data classes
└── artifacts/                      # Generated artifacts
    ├── data_transformation/
    ├── model_training/
    └── model_evaluation/
```

## 🔧 Technical Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.10.11 |
| Data Ingestion | YouTube Data API v3, SQLite3 |
| NLP & Embeddings | sentence-transformers (all-mpnet-base-v2) |
| ML Framework | scikit-learn (SVC), imbalanced-learn (SMOTE) |
| Experiment Tracking | MLflow, DagsHub |
| Orchestration | DVC |
| Frontend | Streamlit, Plotly |

## 📝 Pipeline Stages

The MLOps pipeline consists of the following stages orchestrated by DVC:

1. **Data Ingestion**: Fetches comments from YouTube API and stores in SQLite
2. **Data Labelling**: Uses HuggingFace pipeline for initial sentiment labels
3. **Data Cleaning**: Removes URLs, emojis, and stopwords
4. **Data Transformation**: Converts text to 768-dimensional embeddings
5. **Model Training**: Trains SVM with SMOTE for class imbalance
6. **Model Evaluation**: Evaluates and promotes models to Production in MLflow

## ⚙️ Configuration

The pipeline uses YAML configuration files located in the `config/` directory:

- `config.yaml`: Pipeline paths and stage configurations
- `params.yaml`: Model hyperparameters
- `schema.yaml`: Data validation schemas

## 🤝 Contributing

This project follows a modular MLOps architecture. To add new components:

1. Create component class in `src/Crypto/components/`
2. Add configuration in `src/Crypto/entity/config_entity.py`
3. Create pipeline in `src/Crypto/pipeline/`
4. Update `main.py` to orchestrate the new stage

## 📄 License

This project is licensed under the MIT License.

## Notes

The current README.md in the repository contains development notes and planning steps rather than user-facing documentation <cite repo="Sahilkumar8084/Youtube-Sentiment-Analysis" path="README.md" start="1-22" />. The generated README above provides comprehensive documentation for users to understand and use the project, based on the Project Overview and Glossary wiki pages <cite repo="Sahilkumar8084/Youtube-Sentiment-Analysis" path="Project Overview" start="1-1" /> <cite repo="Sahilkumar8084/Youtube-Sentiment-Analysis" path="Glossary" start="1-1" />.

Wiki pages you might want to explore Full Project Documentation:
- [Project Overview (Sahilkumar8084/Youtube-Sentiment-Analysis)](https://deepwiki.com/Sahilkumar8084/Youtube-Sentiment-Analysis)
