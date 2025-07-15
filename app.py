
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Dashboard Loja de Camisas")

st.title("👕 Dashboard - Loja Online de Camisas (Pré-vendas)")

# Carregar dados
trafego = pd.read_csv("trafego_site.csv")
produtos = pd.read_csv("produtos_mais_clicados.csv")
redes = pd.read_csv("redes_sociais.csv")
conversao = pd.read_csv("conversao_simulada.csv")

# Coluna 1 - Tráfego
st.header("🌐 Tráfego do Site")
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Visitantes por Fonte")
    st.bar_chart(trafego.set_index("Fonte")["Visitantes"])

with col2:
    st.subheader("Taxa de Rejeição (%)")
    st.bar_chart(trafego.set_index("Fonte")["Bounce Rate (%)"])

# Tempo médio por sessão
st.subheader("⏱️ Tempo Médio por Sessão (em segundos)")
st.line_chart(trafego.set_index("Fonte")["Tempo Médio (segundos)"])

# Coluna 2 - Produtos
st.header("👕 Produtos Mais Clicados")
fig1, ax1 = plt.subplots()
ax1.pie(produtos["Cliques"], labels=produtos["Produto"], autopct="%1.1f%%", startangle=90)
ax1.axis("equal")
st.pyplot(fig1)

# Coluna 3 - Redes Sociais
st.header("📱 Engajamento nas Redes Sociais")
st.dataframe(redes.set_index("Rede Social"))

# Coluna 4 - Conversão
st.header("🛒 Conversão Simulada no Funil")

total = conversao["Quantidade"].iloc[0]
for idx, row in conversao.iterrows():
    taxa = row["Quantidade"] / total * 100
    st.write(f"**{row['Etapa']}** – {row['Quantidade']} ({taxa:.1f}%)")

st.success("Dashboard finalizado! Alimente os dados regularmente para acompanhar sua evolução 🚀")
