# 🚀 SpaceX Falcon 9 First Stage Landing Prediction
### IBM Applied Data Science Capstone Project Report

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML%20Classification-orange.svg)](https://scikit-learn.org/)
[![Plotly Dash](https://img.shields.io/badge/Plotly%20Dash-Interactive%20Dashboard-red.svg)](https://dash.plotly.com/)
[![Folium](https://img.shields.io/badge/Folium-Geospatial%20Analytics-green.svg)](https://python-visualization.github.io/folium/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Executive Summary

SpaceX revolutionised the commercial spaceflight industry by developing reusable **Falcon 9** first-stage rocket boosters. While traditional launch competitors charge upwards of **$62 Million** per launch, SpaceX offers commercial launches at approximately **$20 Million** by landing and re-flying first-stage boosters.

This capstone project applies end-to-end data science methodology to predict whether a Falcon 9 first-stage booster will land successfully (Target `Class = 1`) or fail/unattempted (`Class = 0`). Accurate landing prediction allows commercial launch vendors to bid competitively against SpaceX launch pricing.

---

## 📊 End-to-End Project Methodology

```
┌────────────────────────────────┐    ┌────────────────────────────────┐    ┌────────────────────────────────┐
│ 1. Data Collection             │    │ 2. Data Wrangling              │    │ 3. Exploratory Data Analysis   │
│ • SpaceX REST API              ├───►│ • Mean Imputation              ├───►│ • Seaborn & Matplotlib Charts  │
│ • BeautifulSoup Web Scraping   │    │ • Binary Class Target (1/0)    │    │ • SQLite Queries (SPACEXTBL)   │
└────────────────────────────────┘    │ • One-Hot Encoding (83 features)│    └───────────────┬────────────────┘
                                      └────────────────────────────────┘                    │
                                                                                            ▼
┌────────────────────────────────┐    ┌────────────────────────────────┐    ┌────────────────────────────────┐
│ 5. Machine Learning Models     │◄───│ 4. Interactive Analytics       │◄───┘                                │
│ • Logistic Regression (83.3%)  │    │ • Folium MarkerCluster Maps    │                                     │
│ • Decision Tree (83.3%)        │    │ • Plotly Dash Web Application  │                                     │
│ • SVM (77.8%) | KNN (77.8%)    │    └────────────────────────────────┘                                     │
└────────────────────────────────┘                                                                          │
```

---

## 📂 Repository File Structure

```text
├── 1_SpaceX_Data_Collection_API.ipynb            # SpaceX REST API Ingestion
├── 2_SpaceX_Data_Collection_WebScraping.ipynb     # Wikipedia Web Scraping via BeautifulSoup
├── 3_SpaceX_Data_Wrangling.ipynb                  # Data Wrangling, Imputation & Encoding
├── 4_SpaceX_EDA_Data_Visualization.ipynb         # Seaborn & Matplotlib Visual Analysis
├── 5_SpaceX_EDA_SQL.ipynb                         # SQLite Relational Database Queries
├── 6_SpaceX_Interactive_Folium_Maps.ipynb        # Folium Geospatial Proximity Analysis
├── 7_SpaceX_Interactive_Plotly_Dash.py           # Interactive Plotly Dash Application
├── 8_SpaceX_Machine_Learning_Prediction.ipynb    # Classification ML Modeling & GridSearchCV
├── Data Science Capstone Project Report.pdf       # 🎓 Official 15-Slide Presentation PDF
├── dataset_part_1.csv                             # Raw Ingested API Dataset
├── dataset_part_2.csv                             # Cleaned Dataset with Binary Target Class
├── dataset_part_3.csv                             # One-Hot Encoded ML Matrix (83 Features)
├── spacex_launch_geo.csv                          # Geospatial Coordinates Dataset
├── spacex_sql.csv                                 # SQL SPACEXTBL Source Dataset
└── assets/                                        # Generated Figures, Flowcharts & Graphics
```

---

## 📈 Key Findings & Insights

### 1. Launch Site & Orbital Dynamics
- **CCAFS LC-40** handled the largest volume of early launches but suffered lower initial success rates.
- **KSC LC-39A** achieved the highest overall landing success rate (**>85%**), making it the primary recovery pad.
- Orbits **ES-L1, GEO, HEO, and SSO** achieved a **100% landing success rate**, while high-velocity **GTO** orbits showed higher landing failure risks (~40%).

### 2. Temporal Technological Improvement
- Landing success rates matured from **0% (2010–2013)** to over **90–100% by 2020**, confirming dramatic technological learning curve progression.

---

## 🤖 Machine Learning Model Comparison

All models were evaluated using 10-fold cross-validation with `GridSearchCV` hyperparameter tuning on standard scaled data:

| Algorithm | Train CV Accuracy | Test Accuracy | Status / Verdict |
| :--- | :---: | :---: | :--- |
| **Logistic Regression** | **85.00%** | **83.33%** | 🏆 **Best Model (Recommended for Production)** |
| **Decision Tree Classifier** | **89.11%** | **83.33%** | 🥈 Tied Top Test Accuracy |
| **Support Vector Machine (SVM)** | **85.00%** | **77.78%** | 🥉 Solid Baseline |
| **K-Nearest Neighbors (KNN)** | **89.11%** | **77.78%** | 4th Place |

---

## 💻 How to Run & Reproduce

### 1. Prerequisites & Environment Setup
```bash
pip install pandas numpy matplotlib seaborn scikit-learn folium dash reportlab pymupdf
```

### 2. Run Data Pipeline & Generate Assets
```bash
python generate_capstone_assets.py
python generate_diagrams.py
```

### 3. Generate Presentation PDF Report
```bash
python generate_capstone_pdf.py
```

### 4. Launch Interactive Plotly Dash Application
```bash
python 7_SpaceX_Interactive_Plotly_Dash.py
```

---

## 📜 License & Acknowledgments
This project was developed as part of the **IBM Applied Data Science Professional Certificate** on Coursera / edX.
