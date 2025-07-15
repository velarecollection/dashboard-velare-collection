
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Dashboard Velare", layout="wide")
st.title("📊 Dashboard Velare Collection")

conn = st.connection("gsheets", type=GSheetsConnection)

# URLs das planilhas
urls = {
    'Tráfego do Site': 'https://docs.google.com/spreadsheets/d/1GOW31v8keYSaIqJDajgP-Z5683WO77c98KrNq80oN_o/edit#gid=0',
    'Produtos Mais Clicados': 'https://docs.google.com/spreadsheets/d/1AfgZZKFYG-fYXI5KxnC9ysGOZavc7ZJNof1sxdUiObE/edit#gid=0',
    'Redes Sociais': 'https://docs.google.com/spreadsheets/d/1P1Zj_z0_0Wc_xq95napA3gFw5o9qckJCeSMdnXxtTSw/edit#gid=0',
    'Conversão Simulada': 'https://docs.google.com/spreadsheets/d/1ddq02T2wq5uq-GnPYPk6awN2EUEQxYbr39UCHK0zyfs/edit#gid=0'
}

def carregar_dados(url):
    return conn.read(spreadsheet=url, worksheet="Página1")

aba = st.tabs(["📈 Tráfego", "🔥 Produtos Clicados", "📱 Redes Sociais", "💰 Conversões"])

with aba[0]:
    df = carregar_dados(urls['Tráfego do Site'])
    st.subheader("Visão Geral do Tráfego")
    st.dataframe(df)
    if 'Data' in df.columns:
        df['Data'] = pd.to_datetime(df['Data'])
        graf = px.line(df, x='Data', y='Visitantes', title='Evolução de Visitantes')
        st.plotly_chart(graf, use_container_width=True)

with aba[1]:
    df = carregar_dados(urls['Produtos Mais Clicados'])
    st.subheader("Produtos Mais Clicados")
    st.dataframe(df)
    if 'Produto' in df.columns and 'Cliques' in df.columns:
        graf = px.bar(df.sort_values('Cliques', ascending=False), x='Produto', y='Cliques')
        st.plotly_chart(graf, use_container_width=True)

with aba[2]:
    df = carregar_dados(urls['Redes Sociais'])
    st.subheader("Desempenho nas Redes Sociais")
    st.dataframe(df)
    if 'Rede' in df.columns:
        rede = st.selectbox("Escolha a Rede:", df['Rede'].unique())
        filtrado = df[df['Rede'] == rede]
        graf = px.bar(filtrado, x='Campanha', y='Alcance', color='Campanha')
        st.plotly_chart(graf, use_container_width=True)

with aba[3]:
    df = carregar_dados(urls['Conversão Simulada'])
    st.subheader("Conversão Simulada")
    st.dataframe(df)
    if 'Origem' in df.columns and 'Conversões' in df.columns:
        graf = px.pie(df, names='Origem', values='Conversões')
        st.plotly_chart(graf, use_container_width=True)
