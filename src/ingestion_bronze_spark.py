from pyspark.sql import SparkSession
from pathlib import Path
from logger import get_logger
from ingest_bronze import tabelas

logger = get_logger(__name__)
RAW_DIR = Path("data/raw")
BRONZE_SPARK_DIR = Path("data/bronze_spark")

def create_session():
    spark = SparkSession.builder.appName("olistBronzeIngestion").getOrCreate()
    return spark

def load_csv_spark(session, path):
    df = session.read.csv(path, header=True, inferSchema=True)
    logger.info(f"Arquivo {path} lido com sucesso por spark!")
    return df

def save_to_bronze_spark(df, table_name):
    caminho = str(BRONZE_SPARK_DIR/ table_name)
    df.write.mode("overwrite").parquet(caminho)
    logger.info(f"Parquet {table_name} criado com sucesso!")

def run_ingestion_spark():
    logger.info("Iniciando ingestão bronze por spark!")
    spark_session = create_session()
    for key, value in tabelas.items():
        caminho_ = str(RAW_DIR / value)
        data_frame = load_csv_spark(spark_session, caminho_)
        save_to_bronze_spark(data_frame, key)
    spark_session.stop()
    logger.info("Ingestão por spark concluída!")

if __name__ == '__main__':
    run_ingestion_spark()