import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Dashboard Velare", layout="wide")
st.title("📊 Dashboard Velare Collection <3")

# Conexão com Google Sheets via st.secrets
service_account_info = dict(st.secrets["gcp_service_account"])  # <-- conversão correta
credentials = Credentials.from_service_account_info(service_account_info)
gc = gspread.authorize(credentials)

# Substitua pelo ID real da planilha
sheet = gc.open_by_key("SUA_PLANILHA_ID").sheet1
data = pd.DataFrame(sheet.get_all_records())

st.dataframe(data)
