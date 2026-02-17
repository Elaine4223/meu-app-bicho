import streamlit as st
import pandas as pd
import plotly.express as px
import random

# CONFIGURAÇÃO DE PÁGINA (Layout Profissional)
st.set_page_config(page_title="Monitor Vip Pro - Elaine", layout="wide")

# --- BANCO DE DADOS DE BICHOS OFICIAL ---
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

# CORES POR LOTERIA
CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

# --- INICIALIZAÇÃO DOS DADOS REAIS ---
if 'historico_vips' not in st.session_state:
    st.session_state.historico_vips = [
        {"Loteria": "NACIONAL", "Horário": "12:00", "Prêmio": "1º", "Milhar": "7261", "Grupo": "16", "Bicho": "🦁 Leão"},
        {"Loteria": "NACIONAL", "Horário": "08:00", "Prêmio": "1º", "Milhar": "0651", "Grupo": "13", "Bicho": "🐓 Galo"},
        {"Loteria": "NACIONAL", "Horário": "02:00", "Prêmio": "1º", "Milhar": "6028", "Grupo": "07", "Bicho": "🐑 Carneiro"},
        {"Loteria": "PT-RIO", "Horário": "14:30", "Prêmio": "1º", "Milhar": "6168", "Grupo": "17", "Bicho": "🐒 Macaco"},
        {"Loteria": "PT-RIO", "Horário": "11:30", "Prêmio": "1º", "Milhar": "6378", "Grupo": "20", "Bicho": "🦃 Peru"},
        {"Loteria": "PT-RIO", "Horário": "09:30", "Prêmio": "1º", "Milhar": "8576", "Grupo": "19", "Bicho": "🦚 Pavão"}
    ]

# --- PAINEL DE LANÇAMENTO (DISCRETO NO TOPO) ---
with st.expander("📥 Central de Lançamento de Resultados", expanded=False):
    with st.form("form_venda", clear_on_submit=True):
        c1, c2 = st.columns(2)
        l_in = c1.selectbox("Loteria:", list(CORES.keys()))
        h_in = c2.text_input("Horário (Ex: 15:00):")
        m1, m2, m3, m4, m5 = st.columns(5)
        res_m = [m1.text_input("1º"), m2.text_input("2º"), m3.text_input("3º"), m4.text_input("4º"), m5.text_input("5º")]
        if st.form_submit_button("🚀 Atualizar Monitor"):
            for m, p in zip(res_m, ["1º", "2º", "3º", "4º", "5º"]):
                if m:
                    g = identificar_grupo(m)
                    st.session_state.historico_vips.append({"Loteria": l_in, "Horário": h_in, "Prêmio": p, "Milhar": m, "Grupo": g, "Bicho": BICHO_MAP[g]})
            st.rerun()

# --- INTERFACE VISUAL RESTAURADA ---
df = pd.DataFrame(st.session_state.historico_vips)
escolha = st.selectbox("Selecione a Loteria para Análise:", list(CORES.keys()))
cor = CORES.get(escolha)

st.markdown(f"<h1 style='color: {cor}; text-align: center;'>📍 Resultados de Hoje: {escolha}</h1>", unsafe_allow_html=True)

df_f = df[df['Loteria'] == escolha].sort_values(by="Horário", ascending=False)
df_c = df_f[df_f['Prêmio'] == "1º"]

# 1. CARDS COLORIDOS
if not df_c.empty:
    cols = st.columns(len(df_c.head(4)))
    for i, (idx, row) in enumerate(df_c.head(4).iterrows()):
        with cols[i]:
            st.metric(label=f"Hora: {row['Horário']}", value=row['Milhar'], delta=row['Bicho'])

st.divider()

# 2. HISTÓRICO E PALPITES VIP
col_tab, col_palp = st.columns([1.5, 1])

with col_tab:
    st.subheader("🕒 Histórico do Dia")
    st.table(df_f[['Horário', 'Prêmio', 'Milhar', 'Bicho']].head(10))

with col_palp:
    st.subheader("🎯 Palpites VIP")
    g_fora = [g for g in BICHO_MAP.keys() if g not in df_c['Grupo'].tolist()]
    if g_fora:
        sug = random.choice(g_fora)
        st.markdown(f"<div style='background-color:{cor}; padding:20px; border-radius:15px; color:white; text-align:center;'><b>PRÓXIMO GRUPO PROVÁVEL</b><br><span style='font-size: 32px; font-weight: bold;'>{BICHO_MAP[sug]}</span></div>", unsafe_allow_html=True)
        
        g_i = int(sug)
        d_f = str(g_i * 4).replace('100','00').zfill(2)
        st.write(f"💡 **Milhares Sugeridos:** {random.randint(10,99)}{d_f} | {random.randint(10,99)}{str(g_i*4-1).zfill(2)}")

# 3. TERMÔMETRO DE FREQUÊNCIA
st.divider()
st.subheader("🔥 Termômetro de Bichos (Frequência do Dia)")
if not df_c.empty:
    freq = df_c['Bicho'].value_counts().reset_index()
    fig = px.bar(freq, x='index', y='Bicho', color='Bicho', text_auto=True, color_continuous_scale=[[0, '#eee'], [1, cor]])
    st.plotly_chart(fig, use_container_width=True)

# 4. SIMULADOR NA LATERAL
st.sidebar.header(f"🎰 Simulador ({escolha})")
meu_p = st.sidebar.text_input("Seu Palpite (Milhar ou Grupo):")
valor = st.sidebar.number_input("Valor da Aposta (R$):", 1.0, 100.0, 1.0)
if meu_p:
    ganhou = df_f[df_f['Milhar'].str.contains(meu_p) | (df_f['Grupo'] == meu_p)]
    if not ganhou.empty:
        st.sidebar.balloons()
        st.sidebar.success(f"✅ GANHOU! Prêmio: R$ {valor * 15:.2f}")
    else:
        st.sidebar.error("❌ Não saiu ainda.")
