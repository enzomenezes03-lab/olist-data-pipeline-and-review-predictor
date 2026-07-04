# Data Pipeline & Predictive Model — Brazilian E-commerce Customer Experience

[🇧🇷 Versão em Português](README.pt-BR.md)

End-to-end data pipeline built on the public Olist dataset (99k orders), applying Medallion Architecture (Bronze → Silver → Gold), a Random Forest predictive model, and an interactive dashboard to answer: **"What makes a Brazilian customer have a bad experience with an online order — and can it be predicted before it happens?"**

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Scikit Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

---

## Architecture

The pipeline was implemented in two versions:

**Local (pandas + SQLite)**
The 9 Olist CSVs are ingested via pandas and SQLAlchemy into a SQLite database (Bronze layer). Data quality rules are then applied and the result is persisted into a second SQLite database (Silver layer). Finally, a SQL query with CTEs and aggregations models the `fact_orders` table in the Gold layer, ready for consumption by the model and dashboard.

**Cloud (PySpark + Databricks)**
The same CSVs are loaded into a Unity Catalog Volume on Databricks and ingested as Delta Lake tables (Bronze). Silver and Gold transformations are executed in PySpark notebooks using Spark SQL, leveraging the platform's serverless environment.

The Gold table feeds a Random Forest classification model trained with scikit-learn, which predicts whether an order will result in a bad review based on features such as freight cost, delivery time, and delay. Results are exposed through an interactive dashboard published on Streamlit Community Cloud.

---

## Results

Analysis of **99,441 orders** revealed that **22.7% of customers had a bad experience** (rating ≤ 3), with only **7.9% of orders arriving late**.

States in the North and Northeast regions (RR, AP, AM) have the longest average delivery times — over 25 days — while SP has the fastest deliveries, averaging 8 days.

### Predictive Model

The Random Forest model was trained on **19,164 orders** — a subset of the complete data after removing records with null values in essential features such as delivery time and review score.

Key factors identified by the model:

- **Freight cost (58%)** — the most decisive factor for bad reviews
- **Delivery time (24%)** — second most relevant factor
- **Late delivery (6%)** — late orders average a 2.6 rating vs 4.2 for on-time orders
- **Approval time (4%)** — smaller but present impact

> **Conclusion:** Bad customer experience in Brazilian e-commerce is primarily a logistics problem — high freight costs and long delivery times account for over 80% of negative reviews.

---

## Model Performance

**Overall accuracy: 70%**

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| Good (0) | 0.83 | 0.77 | 0.80 | 15,116 |
| Bad (1) | 0.33 | 0.42 | 0.37 | 4,048 |

The priority metric is **Recall for the Bad class (42%)** — the model identifies 42% of orders that will result in a negative review before it happens.

The main limitation is class imbalance — 79% of orders have good ratings, making it harder for the model to learn the minority class. Additionally, the Olist dataset does not include information about product quality or seller reputation — factors that likely influence customer experience but are unavailable to the model.

![Confusion Matrix](model/confusion_matrix.png)

---

## Dashboard

Access the interactive dashboard in production:

🔗 **[olist-customer-experience.streamlit.app](https://olist-customer-experience.streamlit.app)**

---

## How to Run

### Prerequisites
- Python 3.10+
- Git

### Step by step

**1 — Clone the repository**
```bash
git clone https://github.com/enzomenezes03-lab/olist-data-pipeline-and-review-predictor.git
cd olist-data-pipeline-and-review-predictor
```

**2 — Create and activate virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

**3 — Install dependencies**
```bash
pip install -r requirements.txt
pip install pandas sqlalchemy scikit-learn streamlit plotly joblib matplotlib
```

**4 — Download the dataset**

Go to [this Kaggle link](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), download the dataset and extract the 9 CSV files into the `data/raw/` folder.

**5 — Run the pipeline**
```bash
python src/ingest_bronze.py
python src/transform_silver.py
python src/modeling_gold.py
```

**6 — Train the model**
```bash
python src/predict_bad_review.py
```

**7 — Run the dashboard locally**
```bash
streamlit run dashboard/app.py
```