import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Dashboard Velare", layout="wide")
st.title("📊 Dashboard Velare Collection <3")

# Conexão com Google Sheets via st.secrets
service_account_info = dict(st.secrets["gcp_service_account"])  # conversão para dict
credentials = Credentials.from_service_account_info(service_account_info)
gc = gspread.authorize(credentials)

# Abrir a planilha pelo ID
sheet = gc.open_by_key("1GOW31v8keYSaIqJDajgP-Z5683WO77c98KrNq80oN_o").sheet1

# Carregar dados da aba 1 como DataFrame
data = pd.DataFrame(sheet.get_all_records())

# Exibir no Streamlit
st.dataframe(data)
