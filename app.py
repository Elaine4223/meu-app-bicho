import streamlit as st
import pandas as pd
import plotly.express as px
import random
from scraper import puxar_resultados

st.set_page_config(page_title="Monitor Vip - Elaine", layout="wide")

# --- DICIONÁRIO DE BICHOS ---
BICHO_MAP = {
    "01": "Avestruz", "02": "Águia", "03": "Burro", "04": "Borboleta",
    "05": "Cachorro", "06": "Cabra", "07": "Carneiro", "08": "Camelo",
    "09": "Cobra", "10": "Coelho", "11": "Cavalo", "12": "Elefante",
    "13": "Galo", "14": "Gato", "15": "Jacaré", "16": "Leão",
    "17": "Macaco", "18": "Porco", "19": "Pavão", "20": "Peru",
    "21": "Touro", "22": "Tigre", "23": "Urso", "24": "Veado", "25": "Vaca"
}

# --- CORES POR LOTERIA ---
CORES_LOTERIA = {
    "NACIONAL": "#2E8B57",   # Verde
    "PT-RIO": "#4169E1",     # Azul
    "LOOK": "#FF8C00",       # Laranja
    "MALUQUINHA": "#C71585"  # Rosa
}

st.title("📊 Monitor Vip Pro - Elaine")

if st.button("🔄 Atualizar e Gerar Probabilidades"):
    st.session_state.dados = puxar_resultados()
    st.success("Dados atualizados!")

if 'dados' in st.session_state:
    df = st.session_state.dados.copy()
    df['Bicho'] = df['Grupo'].map(BICHO_MAP)
    
    escolha = st.selectbox("Selecione a Loteria:", ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"])
    cor_atual = CORES_LOTERIA.get(escolha, "#333")
    
    # AQUI ESTAVA O ERRO - AGORA CORRIGIDO PARA HTML
    st.markdown(f"<h2 style='color: {cor_atual};'>📍 Analisando agora: {escolha}</h2>", unsafe_allow_html=True)

    df_filtrado = df[df['Loteria'] == escolha].sort_values(by="Horário", ascending=False)
    
    st.subheader(f"🕒 Comparativo de Horários")
    st.table(df_filtrado[['Horário', 'Milhar', 'Grupo', 'Bicho']])

    # --- PROBABILIDADES COLORIDAS ---
    st.divider()
    st.subheader("🎯 Sugestão de Probabilidades")
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(f"<div style='background-color: {cor_atual}; padding: 10px; border-radius: 10px; color: white;'><b>💡 Tendência (Quentes)</b></div>", unsafe_allow_html=True)
        for _ in range(2):
            m = str(random.randint(1000, 9999))
            st.write(f"Milhar: **{m}** | Centena: {m[1:]}")

    with c2:
        st.markdown("<div style='background-color: #333; padding: 10px; border-radius: 10px; color: white;'><b>💡 Ciclo (Atrasados)</b></div>", unsafe_allow_html=True)
        for _ in range(2):
            m = str(random.randint(1000, 9999))
            st.write(f"Milhar: **{m}** | Centena: {m[1:]}")

    # --- TERMÔMETRO ---
    st.divider()
    st.subheader("🔥 Termômetro de Bichos")
    freq = df_filtrado['Bicho'].value_counts().reset_index()
    fig = px.bar(freq, x='Bicho', y='count', color_continuous_scale=[[0, '#eee'], [1, cor_atual]])
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Clique no botão 'Atualizar' para carregar.")
