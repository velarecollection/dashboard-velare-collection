
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Dashboard Velare", layout="wide")
st.title("📊 Dashboard Velare Collection")

# Conexão com Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# URLs das planilhas
urls = {
    'Tráfego do Site': 'https://docs.google.com/spreadsheets/d/1GOW31v8keYSaIqJDajgP-Z5683WO77c98KrNq80oN_o/edit#gid=0',
    'Produtos Mais Clicados': 'https://docs.google.com/spreadsheets/d/1AfgZZKFYG-fYXI5KxnC9ysGOZavc7ZJNof1sxdUiObE/edit#gid=0',
    'Redes Sociais': 'https://docs.google.com/spreadsheets/d/1P1Zj_z0_0Wc_xq95napA3gFw5o9qckJCeSMdnXxtTSw/edit#gid=0',
    'Conversão Simulada': 'https://docs.google.com/spreadsheets/d/1ddq02T2wq5uq-GnPYPk6awN2EUEQxYbr39UCHK0zyfs/edit#gid=0'
}

# Função auxiliar
def carregar_dados(url):
    return conn.read(spreadsheet=url, worksheet="Página1")

# Tabs do dashboard
aba = st.tabs(["📈 Tráfego", "🔥 Produtos Clicados", "📱 Redes Sociais", "💰 Conversões"])

# ----------- ABA 1 - Tráfego -----------
with aba[0]:
    df_trafego = carregar_dados(urls['Tráfego do Site'])
    st.subheader("Visão Geral do Tráfego")
    st.dataframe(df_trafego)

    if 'Data' in df_trafego.columns:
        df_trafego['Data'] = pd.to_datetime(df_trafego['Data'])
        graf = px.line(df_trafego, x='Data', y='Visitantes', title='Evolução de Visitantes')
        st.plotly_chart(graf, use_container_width=True)

# ----------- ABA 2 - Produtos Clicados -----------
with aba[1]:
    df_produtos = carregar_dados(urls['Produtos Mais Clicados'])
    st.subheader("Produtos Mais Clicados")
    st.dataframe(df_produtos)

    if 'Produto' in df_produtos.columns and 'Cliques' in df_produtos.columns:
        graf = px.bar(df_produtos.sort_values('Cliques', ascending=False),
                      x='Produto', y='Cliques', title='Top Produtos Clicados')
        st.plotly_chart(graf, use_container_width=True)

# ----------- ABA 3 - Redes Sociais -----------
with aba[2]:
    df_redes = carregar_dados(urls['Redes Sociais'])
    st.subheader("Desempenho nas Redes Sociais")
    st.dataframe(df_redes)

    if 'Rede' in df_redes.columns:
        rede = st.selectbox("Escolha a Rede:", df_redes['Rede'].unique())
        df_filtrado = df_redes[df_redes['Rede'] == rede]

        graf = px.bar(df_filtrado, x='Campanha', y='Alcance', color='Campanha',
                      title=f'Alcance por Campanha - {rede}')
        st.plotly_chart(graf, use_container_width=True)

# ----------- ABA 4 - Conversão Simulada -----------
with aba[3]:
    df_conv = carregar_dados(urls['Conversão Simulada'])
    st.subheader("Conversão Simulada")
    st.dataframe(df_conv)

    if 'Origem' in df_conv.columns and 'Conversões' in df_conv.columns:
        graf = px.pie(df_conv, names='Origem', values='Conversões', title='Distribuição de Conversões')
        st.plotly_chart(graf, use_container_width=True)

st.success("✅ Dashboard 100% conectado com Google Sheets e atualizado em tempo real!")
