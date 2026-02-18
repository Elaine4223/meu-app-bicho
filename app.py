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

def obter_bicho(grupo):
    return BICHO_MAP.get(str(grupo).zfill(2), "Sorte")

CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = []

# --- 1. CENTRAL DE LANÇAMENTO VERTICAL (MANUAL) ---
st.title("🏆 Central de Lançamento VIP")
with st.expander("📥 Painel Manual (1º ao 5º Prêmio)", expanded=True):
    loto_atual = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
    
    for h_idx in range(1, 9):
        st.markdown(f"### ⏰ Horário {h_idx}")
        col_h, _ = st.columns([1, 4])
        hora = col_h.text_input(f"Horário {h_idx}", key=f"h_{h_idx}", placeholder="Ex: 10:00")
        
        c_header = st.columns([0.5, 1, 1, 1])
        c_header[0].write("**Prêmio**")
        c_header[1].write("**Milhar**")
        c_header[2].write("**Centena**")
        c_header[3].write("**Grupo**")
        
        for p_idx in range(1, 6):
            cp, cm, cc, cg = st.columns([0.5, 1, 1, 1])
            cp.write(f"**{p_idx}º**")
            m_v = cm.text_input(f"M", key=f"m_{h_idx}_{p_idx}", label_visibility="collapsed")
            c_v = cc.text_input(f"C", key=f"c_{h_idx}_{p_idx}", label_visibility="collapsed")
            g_v = cg.text_input(f"G", key=f"g_{h_idx}_{p_idx}", label_visibility="collapsed")
        st.markdown("---")
            
    if st.button("🚀 Atualizar Monitor"):
        temp = []
        for h_idx in range(1, 9):
            hf = st.session_state.get(f"h_{h_idx}")
            if hf:
                for p_idx in range(1, 6):
                    milhar = st.session_state.get(f"m_{h_idx}_{p_idx}")
                    grupo = st.session_state.get(f"g_{h_idx}_{p_idx}")
                    centena = st.session_state.get(f"c_{h_idx}_{p_idx}")
                    if milhar and grupo:
                        temp.append({
                            "Loteria": loto_atual, "Horário": hf, "Prêmio": f"{p_idx}º", 
                            "Milhar": milhar, "Centena": centena, "Grupo": grupo, 
                            "Bicho": obter_bicho(grupo)
                        })
        if temp:
            st.session_state.vagas_resultados = temp
            st.rerun()

st.divider()

# --- 2. INTERFACE DE ANÁLISE ---
if st.session_state.vagas_resultados:
    df = pd.DataFrame(st.session_state.vagas_resultados)
    loto_ativa = df['Loteria'].iloc[0]
    cor = CORES.get(loto_ativa, "#333")
    
    st.markdown(f"<h1 style='color: {cor}; text-align: center;'>📍 API JB: {loto_ativa}</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.subheader("🕒 Histórico Detalhado (1º ao 5º)")
        st.table(df[['Horário', 'Prêmio', 'Milhar', 'Centena', 'Grupo', 'Bicho']].sort_values(by=["Horário", "Prêmio"]))

    with c2:
        st.subheader("🎯 Palpites VIP")
        g_1_saiu = df[df['Prêmio'] == "1º"]['Grupo'].tolist()
        g_vivos = [g for g in BICHO_MAP.keys() if g not in g_1_saiu]
        if g_vivos:
            sug = random.choice(g_vivos)
            st.markdown(f"<div style='background-color:{cor}; padding:15px; border-radius:10px; color:white; text-align:center;'><b>PRÓXIMO GRUPO PROVÁVEL</b><br><span style='font-size: 28px;'>{BICHO_MAP[sug]}</span></div>", unsafe_allow_html=True)
            
            st.markdown("#### 🎰 5 Milhares Sugeridos")
            for i in range(5):
                dezena_base = str(int(sug)*4).zfill(2)
                m_sug = f"{random.randint(1,9)}{random.randint(0,9)}{dezena_base}"
                st.write(f"🔥 **{m_sug}** | C: **{m_sug[-3:]}**")

    st.divider()
    st.subheader("🔥 Termômetro de Frequência")
    freq = df['Bicho'].value_counts().reset_index()
    freq.columns = ['Bicho', 'Qtd']
    fig = px.bar(freq, x='Bicho', y='Qtd', color='Bicho', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Preencha os resultados acima para gerar as análises vencedoras!")
