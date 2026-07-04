import streamlit as st
import pandas as pd
import joblib
from sqlalchemy import create_engine
from pathlib import Path
import plotly.express as px

GOLD_DB_PATH = Path('data/gold/olist_gold.db')
MODEL_PATH = Path('model/random_forest.pkl')



# Funções de dados

def get_engine():
    return create_engine(f"sqlite:///{GOLD_DB_PATH}")


def load_data(engine):
    return pd.read_sql("SELECT * FROM fact_orders", engine)


def calc_metrics(df):
    total_pedidos = len(df)
    avaliacoes_ruins = len(df[df["avg_review_score"] <= 3])
    percentagem_ruins = (avaliacoes_ruins / total_pedidos) * 100
    frete_medio = df['sum_freight'].mean()
    late_bool = df['late'].astype(bool)
    pedidos_atrasados = int(late_bool.sum())
    percentagem_atrasados = (pedidos_atrasados / total_pedidos) * 100
    tempo_medio_entrega = df['deliver_time_days'].mean()
    return total_pedidos, percentagem_ruins, frete_medio, percentagem_atrasados, tempo_medio_entrega



# Funções de visualização

def show_metricas(total, pct_ruins, frete_medio, pct_atrasados, tempo_entrega):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Pedidos", f"{total:,}".replace(",", "."))
    with col2:
        st.metric("Avaliações Ruins", f"{pct_ruins:.1f}%")
    with col3:
        st.metric("Pedidos com Atraso", f"{pct_atrasados:.1f}%")

    col4, col5 = st.columns(2)
    with col4:
        st.metric("Frete Médio", f"R$ {frete_medio:.2f}")
    with col5:
        st.metric("Tempo Médio de Entrega", f"{tempo_entrega:.1f} dias")


def plot_distribuicao_avaliacoes(df):
    contagem = df['avg_review_score'].dropna().round().astype(int).value_counts().sort_index()
    fig = px.bar(
        x=contagem.index.astype(str),
        y=contagem.values,
        title="Distribuição de Avaliações",
        labels={'x': 'Nota', 'y': 'Número de Pedidos'},
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_atraso_vs_avaliacao(df):
    dados = df.dropna(subset=['late', 'avg_review_score']).copy()
    dados['status_entrega'] = dados['late'].astype(bool).map({True: 'Atrasado', False: 'No Prazo'})
    media_por_atraso = dados.groupby('status_entrega')['avg_review_score'].mean().reset_index()
    fig = px.bar(
        media_por_atraso,
        x='status_entrega',
        y='avg_review_score',
        title="Avaliação Média: Atraso vs No Prazo",
        labels={'status_entrega': '', 'avg_review_score': 'Avaliação Média'},
        color='status_entrega',
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_frete_por_avaliacao(df):
    media_frete = df.groupby('avg_review_score')['sum_freight'].mean().reset_index()
    fig = px.line(
        media_frete,
        x='avg_review_score',
        y='sum_freight',
        title="Frete Médio por Nota de Avaliação",
        labels={'avg_review_score': 'Nota', 'sum_freight': 'Frete Médio (R$)'},
        markers=True,
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_tempo_entrega_por_estado(df):
    media_estado = (
        df.groupby('customer_state')['deliver_time_days']
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig = px.bar(
        media_estado,
        x='customer_state',
        y='deliver_time_days',
        title="Tempo Médio de Entrega por Estado do Cliente",
        labels={'customer_state': 'Estado', 'deliver_time_days': 'Dias'},
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_feature_importance():
    if not MODEL_PATH.exists():
        st.info("Modelo não encontrado. Rode o script de treino para gerar o gráfico de importância.")
        return
    model = joblib.load(MODEL_PATH)
    importances = pd.Series(model.feature_importances_, index=model.feature_names_in_)
    importances = importances.sort_values(ascending=True).tail(4)

    nomes = {
        'sum_freight': 'Frete Total',
        'deliver_time_days': 'Tempo de Entrega',
        'late': 'Entrega Atrasada',
        'aprov_time_days': 'Tempo de Aprovação',
    }
    importances.index = [nomes.get(i, i) for i in importances.index]

    fig = px.bar(
        x=importances.values,
        y=importances.index,
        orientation='h',
        title="O Que Mais Influencia uma Avaliação Ruim",
        labels={'x': 'Importância', 'y': 'Fator'},
    )
    st.plotly_chart(fig, use_container_width=True)



# Página

st.set_page_config(page_title="Experiência do Cliente — Olist", layout="wide")
st.title('Experiência do Cliente no E-commerce Brasileiro')
st.caption('O que faz um cliente brasileiro ter uma experiência ruim — e dá pra prever isso?')

engine = get_engine()
df = load_data(engine)

total, pct_ruins, frete_medio, pct_atrasados, tempo_entrega = calc_metrics(df)
show_metricas(total, pct_ruins, frete_medio, pct_atrasados, tempo_entrega)

st.divider()

col_a, col_b = st.columns(2)
with col_a:
    plot_distribuicao_avaliacoes(df)
with col_b:
    plot_atraso_vs_avaliacao(df)

col_c, col_d = st.columns(2)
with col_c:
    plot_frete_por_avaliacao(df)
with col_d:
    plot_tempo_entrega_por_estado(df)

st.divider()

plot_feature_importance()