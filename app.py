import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials
import json
import os

st.set_page_config(page_title="Dashboard Velare", layout="wide")
st.title("📊 Dashboard Velare Collection <3")

# Carregar credenciais do Secrets
service_account_info = {
    "type": st.secrets["gcp_service_account"]["type"],
    "project_id": st.secrets["gcp_service_account"]["project_id"],
    "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
    "private_key": st.secrets["gcp_service_account"]["private_key"].replace("\\n", "\n"),
    "client_email": st.secrets["gcp_service_account"]["client_email"],
    "client_id": st.secrets["gcp_service_account"]["client_id"],
    "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
    "token_uri": st.secrets["gcp_service_account"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"],
}

credentials = Credentials.from_service_account_info(service_account_info, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
gc = gspread.authorize(credentials)

# URLs das planilhas (só usar a parte do ID da planilha)
spreadsheet_ids = {
    'Tráfego do Site': '1GOW31v8keYSaIqJDajgP-Z5683WO77c98KrNq80oN_o',
    'Produtos Mais Clicados': '1AfgZZKFYG-fYXI5KxnC9ysGOZavc7ZJNof1sxdUiObE',
    'Redes Sociais': '1P1Zj_z0_0Wc_xq95napA3gFw5o9qckJCeSMdnXxtTSw',
    'Conversão Simulada': '1ddq02T2wq5uq-GnPYPk6awN2EUEQxYbr39UCHK0zyfs'
}

def carregar_dados(spreadsheet_id, worksheet_name="Página1"):
    sh = gc.open_by_key(spreadsheet_id)
    worksheet = sh.worksheet(worksheet_name)
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

# UI Tabs
abas = st.tabs(["📈 Tráfego", "🔥 Produtos Clicados", "📱 Redes Sociais", "💰 Conversões"])

with abas[0]:
    df_trafego = carregar_dados(spreadsheet_ids['Tráfego do Site'])
    st.subheader("Visão Geral do Tráfego")
    st.dataframe(df_trafego)

    if 'Data' in df_trafego.columns:
        df_trafego['Data'] = pd.to_datetime(df_trafego['Data'])
        graf = px.line(df_trafego, x='Data', y='Visitantes', title='Evolução de Visitantes')
        st.plotly_chart(graf, use_container_width=True)

with abas[1]:
    df_produtos = carregar_dados(spreadsheet_ids['Produtos Mais Clicados'])
    st.subheader("Produtos Mais Clicados")
    st.dataframe(df_produtos)

    if 'Produto' in df_produtos.columns and 'Cliques' in df_produtos.columns:
        graf = px.bar(df_produtos.sort_values('Cliques', ascending=False),
                      x='Produto', y='Cliques', title='Top Produtos Clicados')
        st.plotly_chart(graf, use_container_width=True)

with abas[2]:
    df_redes = carregar_dados(spreadsheet_ids['Redes Sociais'])
    st.subheader("Desempenho nas Redes Sociais")
    st.dataframe(df_redes)

    if 'Rede' in df_redes.columns:
        rede = st.selectbox("Escolha a Rede:", df_redes['Rede'].unique())
        df_filtrado = df_redes[df_redes['Rede'] == rede]

        graf = px.bar(df_filtrado, x='Campanha', y='Alcance', color='Campanha',
                      title=f'Alcance por Campanha - {rede}')
        st.plotly_chart(graf, use_container_width=True)

with abas[3]:
    df_conv = carregar_dados(spreadsheet_ids['Conversão Simulada'])
    st.subheader("Conversão Simulada")
    st.dataframe(df_conv)

    if 'Origem' in df_conv.columns and 'Conversões' in df_conv.columns:
        graf = px.pie(df_conv, names='Origem', values='Conversões', title='Distribuição de Conversões')
        st.plotly_chart(graf, use_container_width=True)

st.success("✅ Dashboard 100% conectado com Google Sheets e atualizado em tempo real!")
