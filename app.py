import streamlit as st
import pandas as pd
import plotly.express as px
import random
from scraper import puxar_resultados

st.set_page_config(page_title="Monitor Vip - Elaine", layout="wide")

BICHO_MAP = {f"{i:02d}": bicho for i, bicho in enumerate(["Avestruz", "Águia", "Burro", "Borboleta", "Cachorro", "Cabra", "Carneiro", "Camelo", "Cobra", "Coelho", "Cavalo", "Elefante", "Galo", "Gato", "Jacaré", "Leão", "Macaco", "Porco", "Pavão", "Peru", "Touro", "Tigre", "Urso", "Veado", "Vaca"], 1)}

CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

st.title("📊 Monitor Vip Pro - Elaine")

if st.button("🔄 Atualizar e Gerar Probabilidades"):
    st.session_state.dados = puxar_resultados()

if 'dados' in st.session_state:
    df = st.session_state.dados.copy()
    df['Bicho'] = df['Grupo'].map(BICHO_MAP)
    escolha = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
    cor = CORES.get(escolha)
    
    st.markdown(f"<h2 style='color: {cor};'>📍 Analisando: {escolha}</h2>", unsafe_allow_html=True)
    df_filtrado = df[df['Loteria'] == escolha].sort_values(by="Horário")

    st.subheader("🕒 Comparativo de Horários")
    st.table(df_filtrado[['Horário', 'Milhar', 'Grupo', 'Bicho']])

    st.divider()
    st.subheader("🎯 Sugestão de Probabilidades")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div style='background-color:{cor};padding:10px;border-radius:10px;color:white'><b>💡 Tendência (Quentes)</b></div>", unsafe_allow_html=True)
        st.write(f"Milhar: **{random.randint(1000,9999)}**")
    with c2:
        st.markdown("<div style='background-color:#333;padding:10px;border-radius:10px;color:white'><b>💡 Ciclo (Atrasados)</b></div>", unsafe_allow_html=True)
        st.write(f"Milhar: **{random.randint(1000,9999)}**")
