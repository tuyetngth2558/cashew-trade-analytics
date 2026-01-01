# 🥜 Cashew Trade Analytics

## 📖 Project Overview
A data analytics platform for analyzing cashew trade contracts, forecasting revenue, and customer segmentation.

## 🚀 Features
- Data cleaning and processing pipeline
- SQLite database management
- Feature engineering for ML models
- Revenue forecasting
- Customer segmentation (RFM Analysis)
- Interactive Streamlit dashboard

## 🛠️ Tech Stack
- **Language:** Python 3.9+
- **Data Processing:** Pandas, NumPy
- **Database:** SQLite, SQLAlchemy
- **Machine Learning:** Scikit-learn
- **Visualization:** Plotly, Matplotlib, Seaborn
- **Dashboard:** Streamlit
- **Version Control:** Git, GitHub

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- Git

### Setup

1. Clone the repository:
```bash
git clone https://github.com/tuyetngth2558/cashew-trade-analytics.git
cd cashew-trade-analytics
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### 1. Prepare Data
Place your data file in `data/raw/Data.txt`

### 2. Run Data Pipeline
```bash
# Clean data
python src/data_processing.py

# Create database
python src/database.py

# Generate features
python src/features.py
```

### 3. Train Models
```bash
python src/models.py
```

### 4. Launch Dashboard
```bash
streamlit run dashboard/app.py
```

## 📊 Project Structure
```
cashew-trade-analytics/
├── data/              # Data files
├── src/               # Python modules
├── dashboard/         # Streamlit app
├── notebooks/         # Jupyter notebooks
├── models/            # Trained models
└── tests/             # Unit tests
```

## 🎯 Next Steps

- [ ] Add machine learning models
- [ ] Implement customer segmentation
- [ ] Add revenue forecasting
- [ ] Deploy to Streamlit Cloud
- [ ] Add authentication
- [ ] Create API endpoints

## 📝 Development Log

### Version 0.1.0 (Current)
- ✅ Data cleaning pipeline
- ✅ SQLite database
- ✅ Basic Streamlit dashboard

### Planned Features
- Machine learning models
- Advanced analytics
- Real-time updates
## 📄 License
MIT License
