import streamlit as st
import pandas as pd
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

def identificar_grupo(milhar):
    try:
        dezena = int(str(milhar)[-2:])
        if dezena == 0: return "25"
        grupo = (dezena - 1) // 4 + 1
        return str(min(grupo, 25)).zfill(2)
    except: return "01"

CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

# --- INICIALIZAÇÃO COM DADOS PARA AS INTERFACES APARECEREM ---
if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = [
        {"Loteria": "NACIONAL", "Horário": "08:00", "Prêmio": "1º", "Milhar": "1224", "Grupo": "06", "Bicho": "🐐 Cabra"},
        {"Loteria": "NACIONAL", "Horário": "10:00", "Prêmio": "1º", "Milhar": "9363", "Grupo": "16", "Bicho": "🦁 Leão"}
    ]

# --- 1. CENTRAL DE LANÇAMENTO (8 SLOTS) ---
st.title("🏆 Central de Lançamento VIP")
with st.expander("📥 Lançar Resultados do Dia (Até 8 Horários)", expanded=False):
    with st.form("form_8_horarios"):
        loto_atual = st.selectbox("Selecione a Loteria para preencher:", list(CORES.keys()))
        st.write("---")
        for i in range(1, 9):
            col_h, col_m = st.columns([1, 4])
            h = col_h.text_input(f"Horário {i}", key=f"h{i}", placeholder="00:00")
            m = col_m.text_input(f"Milhar 1º Prêmio (Slot {i})", key=f"m{i}")
            
        if st.form_submit_button("🚀 Atualizar Banco de Dados do Dia"):
            temp_dados = [] 
            for i in range(1, 9):
                horario = st.session_state[f"h{i}"]
                milhar = st.session_state[f"m{i}"]
                if horario and milhar:
                    g = identificar_grupo(milhar)
                    temp_dados.append({
                        "Loteria": loto_atual, "Horário": horario, 
                        "Prêmio": "1º", "Milhar": milhar, 
                        "Grupo": g, "Bicho": BICHO_MAP[g]
                    })
            if temp_dados:
                st.session_state.vagas_resultados = temp_dados
                st.success("Painel de Análise Atualizado!")
                st.rerun()

st.divider()

# --- 2. INTERFACE DE ANÁLISE (RESTAURADA) ---
if st.session_state.vagas_resultados:
    df = pd.DataFrame(st.session_state.vagas_resultados)
    # Pega a loteria do último lançamento ou a primeira da lista
    loto_ativa = df['Loteria'].iloc[0] if not df.empty else "NACIONAL"
    cor = CORES.get(loto_ativa, "#333")
    
    st.markdown(f"<h1 style='color: {cor}; text-align: center;'>📍 Monitor de Tendências: {loto_ativa}</h1>", unsafe_allow_html=True)

    # Cards (Atrativos como em image_323f59)
    df_c = df.sort_values(by="Horário", ascending=False)
    cols = st.columns(len(df_c.head(4)))
    for i, (idx, row) in enumerate(df_c.head(4).iterrows()):
        with cols[i]:
            st.metric(label=f"Hora: {row['Horário']}", value=row['Milhar'], delta=row['Bicho'])

    st.divider()

    # Histórico e Palpites Lado a Lado (Como em image_3298f6)
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.subheader("🕒 Histórico do Dia")
        st.table(df_c[['Horário', 'Milhar', 'Bicho']])

    with c2:
        st.subheader("🎯 Palpites VIP")
        g_vivos = [g for g in BICHO_MAP.keys() if g not in df['Grupo'].tolist()]
        if g_vivos:
            sug = random.choice(g_vivos)
            st.markdown(f"<div style='background-color:{cor}; padding:20px; border-radius:15px; color:white; text-align:center;'><b>PRÓXIMO GRUPO PROVÁVEL</b><br><span style='font-size: 32px; font-weight: bold;'>{BICHO_MAP[sug]}</span></div>", unsafe_allow_html=True)

    # Termômetro (Como em image_3e8926)
    st.divider()
    st.subheader("🔥 Termômetro de Bichos (Frequência do Dia)")
    freq = df['Bicho'].value_counts().reset_index()
    freq.columns = ['Bicho', 'Qtd']
    fig = px.bar(freq, x='Bicho', y='Qtd', color='Bicho', text_auto=True, color_continuous_scale=[[0, '#eee'], [1, cor]])
    st.plotly_chart(fig, use_container_width=True)
