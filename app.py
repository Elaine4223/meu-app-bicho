import streamlit as st
import pandas as pd
import plotly.express as px
import random

# 1. IDENTIDADE DO APP
st.set_page_config(
    page_title="API JB", 
    page_icon="🎯", 
    layout="wide"
)

# 2. BLOQUEIO VISUAL (Esconde o gatinho do GitHub e menus)
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QS13 {display: none !important;}
    .stAppDeployButton {display: none !important;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# --- DICIONÁRIO OFICIAL ---
BICHO_MAP = {
    "01": "🦩 Avestruz", "02": "🦅 Águia", "03": "🦙 Burro", "04": "🦋 Borboleta", 
    "05": "🐕 Cachorro", "06": "🐐 Cabra", "07": "🐑 Carneiro", "08": "🐪 Camelo", 
    "09": "🐍 Cobra", "10": "🐇 Coelho", "11": "🐎 Cavalo", "12": "🐘 Elefante", 
    "13": "🐓 Galo", "14": "🐈 Gato", "15": "🐊 Jacaré", "16": "🦁 Leão", 
    "17": "🐒 Macaco", "18": "🐖 Porco", "19": "🦚 Pavão", "20": "🦃 Peru", 
    "21": "🐂 Touro", "22": "🐅 Tigre", "23": "🐻 Urso", "24": "🦌 Veado", "25": "🐄 Vaca"
}

def obter_bicho(grupo):
    return BICHO_MAP.get(str(grupo).zfill(2), "Sorte")

CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = []

# --- INTERFACE DE LANÇAMENTO ---
st.title("🏆 API JB - Central VIP")
with st.expander("📥 Lançar Resultados (1º ao 5º Prêmio)", expanded=True):
    loto_atual = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
    
    for h_idx in range(1, 9):
        st.markdown(f"### ⏰ Horário {h_idx}")
        hf = st.text_input(f"Hora", key=f"h_{h_idx}", placeholder="Ex: 10:00")
        
        for p_idx in range(1, 6):
            st.write(f"**{p_idx}º Prêmio**")
            c_m, c_c, c_g = st.columns(3)
            c_m.text_input("Milhar", key=f"m_{h_idx}_{p_idx}")
            c_c.text_input("Centena", key=f"c_{h_idx}_{p_idx}")
            c_g.text_input("Grupo", key=f"g_{h_idx}_{p_idx}")
        st.markdown("---")
            
    if st.button("🚀 Gerar Análise Vencedora"):
        temp = []
        for h_idx in range(1, 9):
            hora_val = st.session_state.get(f"h_{h_idx}")
            if hora_val:
                for p_idx in range(1, 6):
                    milhar = st.session_state.get(f"m_{h_idx}_{p_idx}")
                    grupo = st.session_state.get(f"g_{h_idx}_{p_idx}")
                    centena = st.session_state.get(f"c_{h_idx}_{p_idx}")
                    if milhar and grupo:
                        temp.append({
                            "Loteria": loto_atual, "Horário": hora_val, "Prêmio": f"{p_idx}º", 
                            "Milhar": milhar, "Centena": centena, "Grupo": grupo, 
                            "Bicho": obter_bicho(grupo)
                        })
        if temp:
            st.session_state.vagas_resultados = temp
            st.rerun()

st.divider()

# --- INTERFACE DE ANÁLISE ---
if st.session_state.vagas_resultados:
    df = pd.DataFrame(st.session_state.vagas_resultados)
    loto_ativa = df['Loteria'].iloc[0]
    cor = CORES.get(loto_ativa, "#333")
    
    st.markdown(f"<h2 style='color: {cor}; text-align: center;'>📍 Análise: {loto_ativa}</h2>", unsafe_allow_html=True)
    
    # Palpites
    st.subheader("🎯 Palpites da Rodada")
    g_ja_foi = df[df['Prêmio'] == "1º"]['Grupo'].tolist()
    g_vivos = [g for g in BICHO_MAP.keys() if g not in g_ja_foi]
    if g_vivos:
        sug = random.choice(g_vivos)
        st.success(f"**PRÓXIMO GRUPO PROVÁVEL: {BICHO_MAP[sug]}**")
        for i in range(5):
            dezena_base = str(int(sug)*4).zfill(2)
            m_sug = f"{random.randint(1,9)}{random.randint(0,9)}{dezena_base}"
            st.code(f"M: {m_sug} | C: {m_sug[-3:]}")

    # Termômetro
    st.subheader("🔥 Termômetro de Frequência")
    freq = df['Bicho'].value_counts().reset_index()
    freq.columns = ['Bicho', 'Qtd']
    fig = px.bar(freq, x='Bicho', y='Qtd', color='Bicho', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🕒 Histórico")
    st.dataframe(df[['Horário', 'Prêmio', 'Milhar', 'Centena', 'Grupo', 'Bicho']], use_container_width=True)
else:
    st.info("Aguardando lançamentos para gerar os palpites...")
