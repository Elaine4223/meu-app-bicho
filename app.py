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

# Funções de Cálculo Automático
def extrair_centena(milhar):
    if len(str(milhar)) >= 3:
        return str(milhar)[-3:]
    return ""

def identificar_grupo(milhar):
    try:
        dezena = int(str(milhar)[-2:])
        if dezena == 0: return "25"
        grupo = (dezena - 1) // 4 + 1
        return str(min(grupo, 25)).zfill(2)
    except: return ""

CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = [
        {"Loteria": "NACIONAL", "Horário": "08:00", "Prêmio": "1º", "Milhar": "1224", "Grupo": "06", "Bicho": "🐐 Cabra"}
    ]

# --- 1. CENTRAL DE LANÇAMENTO COM AUTO-PREENCHIMENTO ---
st.title("🏆 Central de Lançamento Profissional PRO")
with st.expander("📥 Painel de Lançamento Inteligente (1º ao 5º Prêmio)", expanded=True):
    loto_atual = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
    
    # Lista temporária para processar os dados
    dados_dia = []

    for h_idx in range(1, 9):
        st.markdown(f"### ⏰ Horário {h_idx}")
        col_h, _ = st.columns([1, 4])
        hora_key = f"hora_{h_idx}"
        hora = col_h.text_input(f"Horário", key=hora_key, placeholder="Ex: 08:00")
        
        c_header = st.columns([0.5, 1, 1, 1])
        c_header[0].write("**Prêmio**")
        c_header[1].write("**Milhar**")
        c_header[2].write("**Centena**")
        c_header[3].write("**Grupo**")
        
        for p_idx in range(1, 6):
            cp, cm, cc, cg = st.columns([0.5, 1, 1, 1])
            cp.write(f"**{p_idx}º**")
            
            # Chaves únicas para cada campo
            m_key = f"m_{h_idx}_{p_idx}"
            c_key = f"c_{h_idx}_{p_idx}"
            g_key = f"g_{h_idx}_{p_idx}"
            
            # Input da Milhar
            milhar = cm.text_input("M", key=m_key, label_visibility="collapsed")
            
            # Lógica de Automatismo: Se a milhar for preenchida, calcula os outros
            centena_auto = extrair_centena(milhar) if milhar else ""
            grupo_auto = identificar_grupo(milhar) if milhar else ""
            
            centena = cc.text_input("C", value=centena_auto, key=c_key, label_visibility="collapsed")
            grupo = cg.text_input("G", value=grupo_auto, key=g_key, label_visibility="collapsed")
            
            if hora and milhar:
                dados_dia.append({
                    "Loteria": loto_atual, "Horário": hora, "Prêmio": f"{p_idx}º",
                    "Milhar": milhar, "Grupo": grupo if grupo else grupo_auto,
                    "Bicho": BICHO_MAP.get(grupo if grupo else grupo_auto, "Sorte")
                })
        st.markdown("---")
            
    if st.button("🚀 Gravar e Sincronizar Monitor"):
        if dados_dia:
            st.session_state.vagas_resultados = dados_dia
            st.success("Tudo pronto! Painel atualizado.")
            st.rerun()

st.divider()

# --- 2. INTERFACE DE ANÁLISE ---
df = pd.DataFrame(st.session_state.vagas_resultados)
loto_ativa = df['Loteria'].iloc[0] if not df.empty else "NACIONAL"
cor = CORES.get(loto_ativa, "#333")

st.markdown(f"<h1 style='color: {cor}; text-align: center;'>📍 Monitor: {loto_ativa}</h1>", unsafe_allow_html=True)

df_1 = df[df['Prêmio'] == "1º"].sort_values(by="Horário", ascending=False)
if not df_1.empty:
    cols = st.columns(min(len(df_1), 4))
    for i, (idx, row) in enumerate(df_1.head(4).iterrows()):
        with cols[i]:
            st.metric(label=f"1º - {row['Horário']}", value=row['Milhar'], delta=row['Bicho'])

st.divider()

c1, c2 = st.columns([1.5, 1])
with c1:
    st.subheader("🕒 Histórico Detalhado")
    st.dataframe(df.sort_values(by=["Horário", "Prêmio"]), use_container_width=True)

with c2:
    st.subheader("🎯 Palpite VIP")
    g_ja_foi = df[df['Prêmio'] == "1º"]['Grupo'].tolist()
    g_vivos = [g for g in BICHO_MAP.keys() if g not in g_ja_foi]
    if g_vivos:
        sug = random.choice(g_vivos)
        st.markdown(f"<div style='background-color:{cor}; padding:25px; border-radius:15px; color:white; text-align:center;'><b>FORTE PARA O PRÓXIMO</b><br><span style='font-size: 32px; font-weight: bold;'>{BICHO_MAP[sug]}</span></div>", unsafe_allow_html=True)

st.divider()
st.subheader("🔥 Termômetro Geral (1º ao 5º)")
if not df.empty:
    freq = df['Bicho'].value_counts().reset_index()
    freq.columns = ['Bicho', 'Qtd']
    fig = px.bar(freq, x='Bicho', y='Qtd', color='Bicho', text_auto=True, color_continuous_scale=[[0, '#eee'], [1, cor]])
    st.plotly_chart(fig, use_container_width=True)
