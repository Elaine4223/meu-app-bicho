import streamlit as st
import pandas as pd
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
        hora = col_h.text_input(f"Horário {h_idx}", key=f"h_{h_idx}", placeholder="Ex: 08:00")
        
        c_header = st.columns([0.5, 1, 1, 1])
        c_header[1].write("**Milhar**")
        c_header[2].write("**Centena**")
        c_header[3].write("**Grupo**")
        
        for p_idx in range(1, 6):
            cp, cm, cc, cg = st.columns([0.5, 1, 1, 1])
            cp.write(f"**{p_idx}º**")
            
            # Input Milhar
            m_input = cm.text_input(f"M", key=f"m_{h_idx}_{p_idx}", label_visibility="collapsed")
            
            # Cálculo Automático
            c_auto, g_auto = calcular_dados(m_input)
            
            # Exibição Automática (Campos Centena e Grupo preenchem sozinhos)
            cc.text_input(f"C", value=c_auto, key=f"c_{h_idx}_{p_idx}", label_visibility="collapsed", disabled=True)
            cg.text_input(f"G", value=g_auto, key=f"g_{h_idx}_{p_idx}", label_visibility="collapsed", disabled=True)
        st.markdown("---")
            
    if st.button("🚀 Atualizar Monitor"):
        temp = []
        for h_idx in range(1, 9):
            hf = st.session_state.get(f"h_{h_idx}")
            if hf:
                for p_idx in range(1, 6):
                    milhar = st.session_state.get(f"m_{h_idx}_{p_idx}")
                    if milhar:
                        c_val, g_val = calcular_dados(milhar)
                        temp.append({
                            "Loteria": loto_atual, "Horário": hf, "Prêmio": f"{p_idx}º", 
                            "Milhar": milhar, "Centena": c_val, "Grupo": g_val, 
                            "Bicho": obter_bicho(g_val)
                        })
        if temp:
            st.session_state.vagas_resultados = temp
            st.rerun()

st.divider()

# --- 2. INTERFACE DE ANÁLISE ---
df = pd.DataFrame(st.session_state.vagas_resultados)
loto_ativa = df['Loteria'].iloc[0] if not df.empty else "NACIONAL"
cor = CORES.get(loto_ativa, "#333")
st.markdown(f"<h1 style='color: {cor}; text-align: center;'>📍 API JB: {loto_ativa}</h1>", unsafe_allow_html=True)

# Cards 1º Prêmio
df_1 = df[df['Prêmio'] == "1º"].sort_values(by="Horário", ascending=False)
if not df_1.empty:
    cols_cards = st.columns(len(df_1.head(4)))
    for i, (idx, row) in enumerate(df_1.head(4).iterrows()):
        with cols_cards[i]:
            st.metric(label=f"1º - {row['Horário']}", value=row['Milhar'], delta=row['Bicho'])

st.divider()

c1, c2 = st.columns([1.5, 1])
with c1:
    st.subheader("🕒 Histórico Detalhado (1º ao 5º)")
    st.table(df[['Horário', 'Prêmio', 'Milhar', 'Centena', 'Grupo', 'Bicho']].sort_values(by=["Horário", "Prêmio"]))

with c2:
    st.subheader("🎯 Palpites VIP")
    g_1_saiu = df[df['Prêmio'] == "1º"]['Grupo'].tolist()
    g_vivos = [g for g in BICHO_MAP.keys() if g not in g_1_saiu]
    if g_
