import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Dashboard Velare", layout="wide")
st.title("📊 Dashboard Velare Collection <3")

# Autenticação com escopos definidos
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
service_account_info = dict(st.secrets["gcp_service_account"])
credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)
gc = gspread.authorize(credentials)

# Abertura da planilha
#sheet = gc.open_by_key("1GOW31v8keYSaIqJDajgP-Z5683WO77c98KrNq80oN_o").sheet1
sheet = gc.open_by_key("1vp5nkA44k-9phsKwLe_Qj5R_gur8QxGg").sheet1
data = pd.DataFrame(sheet.get_all_records())

st.dataframe(data)


