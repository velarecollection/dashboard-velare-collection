import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Velare", layout="wide")
st.title("📊 Dashboard Velare Collection - Gráficos Interativos")

csv_url = "https://docs.google.com/spreadsheets/d/1GOW31v8keYSaIqJDajgP-Z5683WO77c98KrNq80oN_o/export?format=csv&gid=0"

try:
    df = pd.read_csv(csv_url)
except Exception as e:
    st.error(f"Erro ao carregar dados da planilha Google Sheets: {e}")
    st.stop()

# Filtros dinâmicos
st.sidebar.header("⚙️ Filtros")
origens = st.sidebar.multiselect("Origem do tráfego", df["origem"].unique(), default=df["origem"].unique())
dispositivos = st.sidebar.multiselect("Dispositivo", df["dispositivo"].unique(), default=df["dispositivo"].unique())
conteudos = st.sidebar.multiselect("Tipo de conteúdo", df["tipo_conteudo"].unique(), default=df["tipo_conteudo"].unique())

# Aplica os filtros
df_filtrado = df[(df["origem"].isin(origens)) &
                 (df["dispositivo"].isin(dispositivos)) &
                 (df["tipo_conteudo"].isin(conteudos))]

# Métricas principais
st.subheader("📈 Métricas Gerais")
col1, col2, col3 = st.columns(3)
col1.metric("Usuários", df_filtrado.shape[0])
col2.metric("Tempo médio (s)", round(df_filtrado["tempo_sessao"].mean(), 2))
col3.metric("Bounce Rate", f"{round(df_filtrado['bounce'].mean() * 100, 2)}%")

# Gráfico de produtos mais clicados
st.subheader("🌟 Produtos mais clicados")
prod_fig = px.bar(df_filtrado["produto_clicado"].value_counts().reset_index(),
                  x="index", y="produto_clicado",
                  labels={"index": "Produto", "produto_clicado": "Cliques"},
                  title="Produtos mais clicados")
st.plotly_chart(prod_fig, use_container_width=True)

# Gráfico de origem do tráfego
st.subheader("📅 Origem do Tráfego")
trafego_fig = px.pie(df_filtrado, names="origem", title="Distribuição por origem")
st.plotly_chart(trafego_fig, use_container_width=True)

# Tempo de sessão por dispositivo
st.subheader("📱 Tempo de Sessão por Dispositivo")
disp_fig = px.box(df_filtrado, x="dispositivo", y="tempo_sessao", points="all",
                  title="Distribuição do Tempo de Sessão por Dispositivo")
st.plotly_chart(disp_fig, use_container_width=True)

# Engajamento por tipo de conteúdo
st.subheader("❤️ Engajamento por Tipo de Conteúdo")
engajamento_fig = px.bar(df_filtrado.groupby("tipo_conteudo")["curtidas"].mean().reset_index(),
                         x="tipo_conteudo", y="curtidas",
                         title="Média de Curtidas por Tipo de Conteúdo")
st.plotly_chart(engajamento_fig, use_container_width=True)

# Rodapé
st.caption("Dados carregados do Google Sheets | Velare Dashboard")

