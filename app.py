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

# Funções de Extração Automática
def extrair_centena(m):
    return str(m)[-3:] if len(str(m)) >= 3 else ""

def identificar_grupo(m):
    try:
        dezena = int(str(m)[-2:])
        if dezena == 0: return "25"
        return str(min((dezena - 1) // 4 + 1, 25)).zfill(2)
    except: return "01"

CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = [
        {"Horário": "08:00", "Prêmio": "1º", "Milhar": "1224", "Centena": "224", "Grupo": "06", "Bicho": "🐐 Cabra", "Loteria": "NACIONAL"}
    ]

# --- 1. CENTRAL DE LANÇAMENTO (FOCO NA MILHAR) ---
st.title("🏆 Central de Lançamento Inteligente")
with st.expander("📥 Digite apenas os Milhares (Centena e Grupo automáticos)", expanded=True):
    with st.form("form_auto_calculo"):
        loto_atual = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
        
        for h_idx in range(1, 9):
            st.markdown(f"#### ⏰ Horário {h_idx}")
            col_h, col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns([1, 1, 1, 1, 1, 1])
            
            hora = col_h.text_input(f"Hora", key=f"h_{h_idx}", placeholder="00:00")
            m1 = col_m1.text_input("1º Milhar", key=f"m1_{h_idx}")
            m2 = col_m2.text_input("2º Milhar", key=f"m2_{h_idx}")
            m3 = col_m3.text_input("3º Milhar", key=f"m3_{h_idx}")
            m4 = col_m4.text_input("4º Milhar", key=f"m4_{h_idx}")
            m5 = col_m5.text_input("5º Milhar", key=f"m5_{h_idx}")
            st.markdown("---")
            
        if st.form_submit_button("🚀 Gravar e Calcular Tudo"):
            novos_dados = []
            for h_idx in range(1, 9):
                hora_v = st.session_state.get(f"h_{h_idx}")
                if hora_v:
                    for p_idx in range(1, 6):
                        milhar_v = st.session_state.get(f"m{p_idx}_{h_idx}")
                        if milhar_v:
                            centena_v = extrair_centena(milhar_v)
                            grupo_v = identificar_grupo(milhar_v)
                            novos_dados.append({
                                "Horário": hora_v, "Prêmio": f"{p_idx}º",
                                "Milhar": milhar_v, "Centena": centena_v,
                                "Grupo": grupo_v, "Bicho": BICHO_MAP.get(grupo_v, "Sorte"),
                                "Loteria": loto_atual
                            })
            if novos_dados:
                st.session_state.vagas_resultados = novos_dados
                st.success("✅ Sucesso! Centenas e Grupos calculados automaticamente.")
                st.rerun()

st.divider()

# --- 2. INTERFACE DE ANÁLISE ---
df = pd.DataFrame(st.session_state.vagas_resultados)
loto_ativa = df['Loteria'].iloc[0] if not df.empty else "NACIONAL"
cor = CORES.get(loto_ativa, "#333")

st.markdown(f"<h1 style='color: {cor}; text-align: center;'>📍 Monitor: {loto_ativa}</h1>", unsafe_allow_html=True)

# Cards (1º Prêmio)
df_1 = df[df['Prêmio'] == "1º"].sort_values(by="Horário", ascending=False)
if not df_1.empty:
    cols = st.columns(min(len(df_1), 4))
    for i, (idx, row) in enumerate(df_1.head(4).iterrows()):
        with cols[i]:
            st.metric(label=f"1º - {row['Horário']}", value=row['Milhar'], delta=row['Bicho'])

# Tabela e Palpites
c1, c2 = st.columns([1.8, 1])
with c1:
    st.subheader("🕒 Histórico com Cálculos Automáticos")
    st.dataframe(df.sort_values(by=["Horário", "Prêmio"]), use_container_width=True)

with c2:
    st.subheader("🎯 Palpite VIP")
    g_ja_saiu = df[df['Prêmio'] == "1º"]['Grupo'].tolist()
    g_vivos = [g for g in BICHO_MAP.keys() if g not in g_ja_saiu]
    if g_vivos:
        sug = random.choice(g_vivos)
        st.markdown(f"<div style='background-color:{cor}; padding:25px; border-radius:15px; color:white; text-align:center;'><b>FORTE PARA O PRÓXIMO</b><br><span style='font-size: 32px; font-weight: bold;'>{BICHO_MAP[sug]}</span></div>", unsafe_allow_html=True)

# Termômetro
st.divider()
st.subheader("🔥 Termômetro de Frequência (1º ao 5º)")
if not df.empty:
    freq = df['Bicho'].value_counts().reset_index()
    freq.columns = ['Bicho', 'Qtd']
    fig = px.bar(freq, x='Bicho', y='Qtd', color='Bicho', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
