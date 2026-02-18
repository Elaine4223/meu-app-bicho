import streamlit as st
import pd
import plotly.express as px
import random

st.set_page_config(page_title="Monitor Vip Pro - Elaine", layout="wide")

# --- DICIONÁRIO OFICIAL ---
BICHO_MAP = {
    "01": "🦩 Avestruz", "02": "🦅 Águia", "03": "🦙 Burro", "04": "🦋 Borboleta", 
    "05": "🐕 Cachorro", "06": "🐐 Cabra", "07": "🐑 Carneiro", "08": "🐪 Camelo", 
    "09": "🐍 Cobra", "10": "🐇 Coelho", "11": "🐎 Cavalo", "12": "🐘 Elefante", 
    "13": "🐓 Galo", "14": "🐈 Gato", "15": "🐊 Jacaré", "16": "🦁 Leão", 
    "17": "🐒 Macaco", "18": "🐖 Porco", "19": "🦚 Pavão", "20": "🦃 Peru", 
    "21": "🐂 Touro", "22": "🐅 Tigre", "23": "🐻 Urso", "24": "🦌 Veado", "25": "🐄 Vaca"
}

def calcular_dados(m):
    if not m or len(str(m)) < 2: return "", ""
    centena = str(m)[-3:] if len(str(m)) >= 3 else ""
    try:
        dezena = int(str(m)[-2:])
        g = "25" if dezena == 0 else str(min((dezena - 1) // 4 + 1, 25)).zfill(2)
    except: g = ""
    return centena, g

CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = []

# --- 1. CENTRAL DE LANÇAMENTO (COM AUTO-SOMA) ---
st.title("🏆 Central de Lançamento Profissional PRO")
with st.expander("📥 Painel de Lançamento (Auto-Preenchimento)", expanded=True):
    loto_atual = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
    
    for h_idx in range(1, 9):
        st.markdown(f"### ⏰ Horário {h_idx}")
        col_h, _ = st.columns([1, 4])
        hora = col_h.text_input(f"Horário", key=f"h_{h_idx}", placeholder="Ex: 08:00")
        
        c_header = st.columns([0.5, 1, 1, 1])
        c_header[1].write("**Milhar**")
        c_header[2].write("**Centena**")
        c_header[3].write("**Grupo**")
        
        for p_idx in range(1, 6):
            cp, cm, cc, cg = st.columns([0.5, 1, 1, 1])
            cp.write(f"**{p_idx}º**")
            
            # Milhar - O gatilho para o resto
            m_input = cm.text_input(f"M", key=f"m_{h_idx}_{p_idx}", label_visibility="collapsed")
            
            # Cálculo automático em tempo real
            c_auto, g_auto = calcular_dados(m_input)
            
            # Centena e Grupo aparecem preenchidos
            cc.text_
