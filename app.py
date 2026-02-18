import streamlit as st
import pandas as pd  # CORRIGIDO: Agora o sistema reconhece a biblioteca corretamente
import plotly.express as px
import random

# CONFIGURAÇÃO DO NOME E ÍCONE OFICIAL
st.set_page_config(
    page_title="API JB", 
    page_icon="🎯", 
    layout="wide"
)

# --- DICIONÁRIO OFICIAL ---
BICHO_MAP = {
    "01": "🦩 Avestruz", "02": "🦅 Águia", "03": "🦙 Burro", "04": "🦋 Borboleta", 
    "05": "🐕 Cachorro", "06": "🐐 Cabra", "07": "🐑 Carneiro", "08": "🐪 Camelo", 
    "09": "🐍 Cobra", "10": "🐇 Coelho", "11": "🐎 Cavalo", "12": "🐘 Elefante", 
    "13": "🐓 Galo", "14": "🐈 Gato", "15": "🐊 Jacaré", "16": "🦁 Leão", 
    "17": "🐒 Macaco", "18": "🐖 Porco", "19": "🦚 Pavão", "20": "🦃 Peru", 
    "21": "🐂 Touro", "22": "🐅 Tigre", "23": "🐻 Urso", "24": "🦌 Veado", "25": "🐄 Vaca"
}

# Funções de Cálculo Automático
def calcular_dados(m):
    if not m or len(str(m)) < 2: return "", ""
    centena = str(m)[-3:] if len(str(m)) >= 3 else ""
    try:
        dezena = int(str(m)[-2:])
        g = "25" if dezena == 0 else str(min((dezena - 1) // 4 + 1, 25)).zfill(2)
    except: g = ""
    return centena, g

def obter_bicho(grupo):
    return BICHO_MAP.get(str(grupo).zfill(2), "Sorte")

CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

# Dados iniciais para a interface nunca abrir vazia
if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = [
        {"Loteria": "NACIONAL", "Horário": "08:00", "Prêmio": "1º", "Milhar": "1224", "Centena": "224", "Grupo": "06", "Bicho": "🐐 Cabra"}
    ]

# --- 1. CENTRAL DE LANÇAMENTO VERTICAL (COM AUTO-PREENCHIMENTO) ---
st.title("🏆 Central de Lançamento VIP")
with st.expander("📥 Painel de Entrada - API JB (Auto-Cálculo)", expanded=False):
    loto_atual = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
    
    for h_idx in range(1, 9):
        st.markdown(f"### ⏰ Horário {h_idx}")
        col_h, _ = st.columns([1, 4])
        hora = col_h.text_input(f"Horário", key=f"h_{h_idx}", placeholder="Ex: 08:00")
        
        c_header = st.columns([0.5,
