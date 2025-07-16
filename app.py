import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Velare", layout="wide")
st.title("📊 Dashboard Velare Collection")

# Carrega dados do Google Sheets (formato CSV público)
csv_url = "https://docs.google.com/spreadsheets/d/1GOW31v8keYSaIqJDajgP-Z5683WO77c98KrNq80oN_o/export?format=csv&gid=0"

try:
    df = pd.read_csv(csv_url)
except Exception as e:
    st.error(f"Erro ao carregar dados da planilha Google Sheets: {e}")
    st.stop()

# Filtros dinâmicos
st.sidebar.header("⚙️ Filtros")
origens = st.sidebar.multiselect("Origem do tráfego", df["origem"].dropna().unique(), default=df["origem"].dropna().unique())
dispositivos = st.sidebar.multiselect("Dispositivo", df["dispositivo"].dropna().unique(), default=df["dispositivo"].dropna().unique())
conteudos = st.sidebar.multiselect("Tipo de conteúdo", df["tipo_conteudo"].dropna().unique(), default=df["tipo_conteudo"].dropna().unique())

# Aplica os filtros
df_filtrado = df[(df["origem"].isin(origens)) &
                 (df["dispositivo"].isin(dispositivos)) &
                 (df["tipo_conteudo"].isin(conteudos))]

# Métricas principais
st.subheader("📈 Métricas Gerais")
col1, col2, col3 = st.columns(3)
col1.metric("Usuários", df_filtrado.shape[0])

# Tempo médio
if "tempo_sessao" in df_filtrado.columns and not df_filtrado["tempo_sessao"].dropna().empty:
    col2.metric("Tempo médio (s)", round(df_filtrado["tempo_sessao"].mean(), 2))
else:
    col2.metric("Tempo médio (s)", "N/D")

# Bounce Rate
if "bounce" in df_filtrado.columns and not df_filtrado["bounce"].dropna().empty:
    col3.metric("Bounce Rate", f"{round(df_filtrado['bounce'].mean() * 100, 2)}%")
else:
    col3.metric("Bounce Rate", "N/D")

# Gráfico de produtos mais clicados
st.subheader("🌟 Produtos mais clicados")

if "produto_clicado" in df_filtrado.columns:
    df_prod = df_filtrado["produto_clicado"].dropna()
    if not df_prod.empty:
        contagem = df_prod.value_counts().reset_index()
        contagem.columns = ["Produto", "Cliques"]
        prod_fig = px.bar(contagem, x="Produto", y="Cliques",
                          title="Produtos mais clicados")
        st.plotly_chart(prod_fig, use_container_width=True)
    else:
        st.info("Nenhum dado disponível para 'Produtos mais clicados' com os filtros atuais.")
else:
    st.warning("A coluna 'produto_clicado' não foi encontrada nos dados.")

# Gráfico de origem do tráfego
st.subheader("📅 Origem do Tráfego")
if "origem" in df_filtrado.columns and not df_filtrado["origem"].dropna().empty:
    trafego_fig = px.pie(df_filtrado, names="origem", title="Distribuição por origem")
    st.plotly_chart(trafego_fig, use_container_width=True)
else:
    st.info("Nenhum dado disponível para 'Origem do Tráfego' com os filtros atuais.")

# Tempo de sessão por dispositivo
st.subheader("📱 Tempo de Sessão por Dispositivo")
if {"dispositivo", "tempo_sessao"}.issubset(df_filtrado.columns) and not df_filtrado[["dispositivo", "tempo_sessao"]].dropna().empty:
    disp_fig = px.box(df_filtrado, x="dispositivo", y="tempo_sessao", points="all",
                      title="Distribuição do Tempo de Sessão por Dispositivo")
    st.plotly_chart(disp_fig, use_container_width=True)
else:
    st.info("Nenhum dado disponível para 'Tempo de Sessão por Dispositivo' com os filtros atuais.")

# Engajamento por tipo de conteúdo
st.subheader("❤️ Engajamento por Tipo de Conteúdo")
if {"tipo_conteudo", "curtidas"}.issubset(df_filtrado.columns) and not df_filtrado[["tipo_conteudo", "curtidas"]].dropna().empty:
    engajamento_fig = px.bar(df_filtrado.groupby("tipo_conteudo")["curtidas"].mean().reset_index(),
                             x="tipo_conteudo", y="curtidas",
                             title="Média de Curtidas por Tipo de Conteúdo")
    st.plotly_chart(engajamento_fig, use_container_width=True)
else:
    st.info("Nenhum dado disponível para 'Engajamento por Tipo de Conteúdo' com os filtros atuais.")

# Rodapé
st.caption("Dados carregados do Google Sheets | Velare Dashboard")
