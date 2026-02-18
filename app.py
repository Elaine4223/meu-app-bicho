import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="Monitor Ouro da Sorte - Elaine", layout="wide")

# --- DICIONÁRIO OFICIAL ---
BICHO_MAP = {
    "01": "🦩 Avestruz", "02": "🦅 Águia", "03": "🦙 Burro", "04": "🦋 Borboleta", 
    "05": "🐕 Cachorro", "06": "🐐 Cabra", "07": "🐑 Carneiro", "08": "🐪 Camelo", 
    "09": "🐍 Cobra", "10": "🐇 Coelho", "11": "🐎 Cavalo", "12": "🐘 Elefante", 
    "13": "🐓 Galo", "14": "🐈 Gato", "15": "🐊 Jacaré", "16": "🦁 Leão", 
    "17": "🐒 Macaco", "18": "🐖 Porco", "19": "🦚 Pavão", "20": "🦃 Peru", 
    "21": "🐂 Touro", "22": "🐅 Tigre", "23": "🐻 Urso", "24": "🦌 Veado", "25": "🐄 Vaca"
}

def identificar_grupo(valor):
    try:
        dezena = int(str(valor)[-2:])
        if dezena == 0: return "25"
        grupo = (dezena - 1) // 4 + 1
        return str(min(grupo, 25)).zfill(2)
    except: return "01"

CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

# --- FORÇAR EXIBIÇÃO DAS INTERFACES (DADOS INICIAIS) ---
if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = [
        {"Loteria": "NACIONAL", "Horário": "08:00", "Milhar": "1224", "Grupo": "06", "Bicho": "🐐 Cabra"},
        {"Loteria": "NACIONAL", "Horário": "10:00", "Milhar": "9363", "Grupo": "16", "Bicho": "🦁 Leão"}
    ]

# --- 1. CENTRAL DE LANÇAMENTO (EM COLUNAS PROFISSIONAIS) ---
st.title("🏆 Central de Lançamento VIP")
with st.expander("📥 Painel de Entrada - 8 Horários (Clique para abrir)", expanded=False):
    with st.form("form_8_horarios_final"):
        loto_atual = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
        
        # Cabeçalho organizado
        h_cols = st.columns([1, 1, 1, 1])
        h_cols[0].write("**Horário**")
        h_cols[1].write("**Milhar**")
        h_cols[2].write("**Centena**")
        h
