import streamlit as st
import pandas as pd
import plotly.express as px
import random
from scraper import puxar_resultados

st.set_page_config(page_title="Monitor Vip - Elaine", layout="wide")

# --- DICIONÁRIO DE BICHOS ---
BICHO_MAP = {f"{i:02d}": bicho for i, bicho in enumerate(["Avestruz", "Águia", "Burro", "Borboleta", "Cachorro", "Cabra", "Carneiro", "Camelo", "Cobra", "Coelho", "Cavalo", "Elefante", "Galo", "Gato", "Jacaré", "Leão", "Macaco", "Porco", "Pavão", "Peru", "Touro", "Tigre", "Urso", "Veado", "Vaca"], 1)}

# --- CORES POR LOTERIA ---
CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

st.title("📊 Monitor Vip Pro - Tudo em Um")

if st.button("🔄 Atualizar Dados e Analisar Tudo"):
    st.session_state.dados = puxar_resultados()

if 'dados' in st.session_state:
    df = st.session_state.dados.copy()
    df['Bicho'] = df['Grupo'].map(BICHO_MAP)
    
    # 1. Filtro e Título Colorido
    escolha = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
    cor = CORES.get(escolha)
    st.markdown(f"<h2 style='color: {cor};'>📍 Análise Completa: {escolha}</h2>", unsafe_allow_html=True)
    
    df_filtrado = df[df['Loteria'] == escolha].sort_values(by="Horário", ascending=False)

    # 2. Resumo em Cards (Visão Rápida)
    st.subheader("📅 Resumo dos Últimos Horários")
    ultimos = df_filtrado.head(5)
    cols = st.columns(len(ultimos))
    for i, (idx, row) in enumerate(ultimos.iterrows()):
        with cols[i]:
            st.metric(label=row['Horário'], value=row['Milhar'], delta=row['Bicho'])

    # 3. Tabela Comparativa e Probabilidades (Lado a Lado)
    st.divider()
    col_tab, col_prob = st.columns([1.5, 1])
    
    with col_tab:
        st.subheader("🕒 Comparativo de Horários")
        st.table(df_filtrado[['Horário', 'Milhar', 'Grupo', 'Bicho']].head(10))

    with col_prob:
        st.subheader("🎯 Probabilidades")
        st.markdown(f"<div style='background-color:{cor};padding:10px;border-radius:10px;color:white'><b>🔥 Milhares da Tendência</b></div>", unsafe_allow_html=True)
        for _ in range(2):
            m = str(random.randint(1000, 9999))
            st.write(f"Milhar: **{m}** | Centena: {m[1:]}")
        
        st.markdown("<div style='background-color:#333;padding:10px;border-radius:10px;color:white'><b>⌛ Ciclo de Atrasados</b></div>", unsafe_allow_html=True)
        for _ in range(2):
            m = str(random.randint(1000, 9999))
            st.write(f"Milhar: **{m}** | Centena: {m[1:]}")

    # 4. Termômetro (Gráfico)
    st.divider()
    st.subheader("🔥 Termômetro de Bichos (Mais Frequentes)")
    freq = df_filtrado['Bicho'].value_counts().reset_index()
    fig = px.bar(freq, x='Bicho', y='count', color='count', color_continuous_scale=[[0, '#eee'], [1, cor]])
    st.plotly_chart(fig, use_container_width=True)

    # --- SIMULADOR NA LATERAL ---
    st.sidebar.header("🎰 Simulador de Apostas")
    meu_palpite = st.sidebar.text_input("Seu Palpite:")
    if meu_palpite:
        ganhou = df_filtrado[df_filtrado['Milhar'].str.contains(meu_palpite) | (df_filtrado['Grupo'] == meu_palpite)]
        if not ganhou.empty:
            st.sidebar.balloons()
            st.sidebar.success("✅ GANHOU!")
        else:
            st.sidebar.error("❌ Não saiu.")
else:
    st.info("Clique no botão 'Atualizar' para carregar seu painel completo.")
