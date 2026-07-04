from pathlib import Path
import pandas as pd
import sqlalchemy
from logger import get_logger
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib


logger = get_logger(__name__)
FACT_PATH = Path('data/gold/olist_gold.db')

def get_engine():
    con = sqlalchemy.create_engine(f'sqlite:///{FACT_PATH}')
    return con

def get_df(connection):
    df = pd.read_sql("SELECT * FROM fact_orders", connection)
    return df

def create_target(data_frame):
    conditions = [
        data_frame['avg_review_score'] <= 3
    ]
    choices = [1]

    data_frame['target'] = np.select(conditions, choices)
    return data_frame

def prepare_features(df):
    df = pd.get_dummies(df, columns=['seller_state', 'customer_state', 'order_status'])

    df = df.dropna()

    x = df.drop(columns=['target', 'id', 'avg_review_score'])
    y = df['target']

    return x, y

def train_model(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y ,test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(x_train, y_train)

    return model, x_test, y_test

def evaluate_model(modelo, x_teste, y_teste):

    y_pred = modelo.predict(x_teste)
    print(classification_report(y_teste, y_pred))

    importances = pd.Series(modelo.feature_importances_, index=x_teste.columns)
    importances = importances.sort_values(ascending=False)
    print(importances.head(10))

def run_model():
    logger.info('Inicializando Modelo!')
    con = get_engine()
    df = get_df(con)
    df_with_target = create_target(df)

    x, y = prepare_features(df_with_target)
    model, x_test, y_test = train_model(x, y)
    evaluate_model(model, x_test, y_test)
    logger.info('Modelo inicializado com sucesso!')
    joblib.dump(model, 'model/random_forest.pkl')
    logger.info('Modelo salvo em model/random_forest.pkl')

if __name__ == '__main__':
    run_model()