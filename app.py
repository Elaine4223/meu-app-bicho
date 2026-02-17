import streamlit as st
import pandas as pd
import plotly.express as px
import random
from scraper import puxar_resultados

st.set_page_config(page_title="Monitor Vip - Elaine", layout="wide")

# Dicionário de Bichos para sumir com o "Carregando..."
BICHO_MAP = {f"{i:02d}": bicho for i, bicho in enumerate(["Avestruz", "Águia", "Burro", "Borboleta", "Cachorro", "Cabra", "Carneiro", "Camelo", "Cobra", "Coelho", "Cavalo", "Elefante", "Galo", "Gato", "Jacaré", "Leão", "Macaco", "Porco", "Pavão", "Peru", "Touro", "Tigre", "Urso", "Veado", "Vaca"], 1)}

# Cores de Luxo para cada Loteria
CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

st.title("📊 Monitor de Loterias Filtrado")

if st.button("🔄 Atualizar Dados agora"):
    st.session_state.dados = puxar_resultados()

if 'dados' in st.session_state:
    df = st.session_state.dados.copy()
    df['Bicho'] = df['Grupo'].map(BICHO_MAP)
    
    escolha = st.selectbox("Selecione a Loteria para Análise:", list(CORES.keys()))
    cor_viva = CORES.get(escolha)
    
    # Título Colorido Dinâmico
    st.markdown(f"<h2 style='color: {cor_viva};'>📍 Resultados: {escolha}</h2>", unsafe_allow_html=True)
    
    df_filtrado = df[df['Loteria'] == escolha].sort_values(by="Horário", ascending=False)

    # Exibição da Tabela principal
    st.dataframe(df_filtrado[['Horário', 'Milhar', 'Grupo', 'Bicho']], use_container_width=True)

    # --- SIMULADOR NA BARRA LATERAL (Conforme image_314f1d.png) ---
    st.sidebar.header("🎰 Simulador de Apostas")
    meu_palpite = st.sidebar.text_input("Seu Palpite (Ex: 1234 ou 01):")
    valor = st.sidebar.number_input("Valor da Aposta (R$):", min_value=1.0, value=1.0)
    
    if meu_palpite:
        ganhou = df_filtrado[df_filtrado['Milhar'].str.contains(meu_palpite) | (df_filtrado['Grupo'] == meu_palpite)]
        if not ganhou.empty:
            st.sidebar.balloons()
            st.sidebar.success(f"✅ GANHOU NA {escolha}!")
        else:
            st.sidebar.error("❌ Ainda não saiu.")
else:
    st.info("Clique no botão azul para carregar a interface.")
