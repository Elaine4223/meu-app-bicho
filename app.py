import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="Monitor Ouro da Sorte - Elaine VIP", layout="wide")

# --- DICIONÁRIO OFICIAL ---
BICHO_MAP = {
    "01": "🦩 Avestruz", "02": "🦅 Águia", "03": "🦙 Burro", "04": "🦋 Borboleta", 
    "05": "🐕 Cachorro", "06": "🐐 Cabra", "07": "🐑 Carneiro", "08": "🐪 Camelo", 
    "09": "🐍 Cobra", "10": "🐇 Coelho", "11": "🐎 Cavalo", "12": "🐘 Elefante", 
    "13": "🐓 Galo", "14": "🐈 Gato", "15": "🐊 Jacaré", "16": "🦁 Leão", 
    "17": "🐒 Macaco", "18": "🐖 Porco", "19": "🦚 Pavão", "20": "🦃 Peru", 
    "21": "🐂 Touro", "22": "🐅 Tigre", "23": "🐻 Urso", "24": "🦌 Veado", "25": "🐄 Vaca"
}

# Funções Inteligentes de Extração
def extrair_centena(m):
    return str(m)[-3:] if len(str(m)) >= 3 else ""

def identificar_grupo(m):
    try:
        dezena = int(str(m)[-2:])
        if dezena == 0: return "25"
        grupo = (dezena - 1) // 4 + 1
        return str(min(grupo, 25)).zfill(2)
    except: return "01"

CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = [
        {"Horário": "2:00", "Prêmio": "1º", "Milhar": "0579", "Centena": "579", "Grupo": "20", "Bicho": "🦃 Peru", "Loteria": "NACIONAL"}
    ]

# --- 1. CENTRAL DE LANÇAMENTO (FOCO TOTAL NA MILHAR) ---
st.title("🏆 Central de Lançamento Inteligente")
with st.expander("📥 Digite apenas os Horários e Milhares", expanded=False):
    with st.form("form_auto_inteligente"):
        loto_atual = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
        
        for h_idx in range(1, 9):
            st.markdown(f"#### ⏰ Horário {h_idx}")
            col_hora, col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns([1, 1, 1, 1, 1, 1])
            
            h_v = col_hora.text_input("Hora", key=f"h_{h_idx}", placeholder="00:00")
            m1 = col_m1.text_input("1º Milhar", key=f"m1_{h_idx}")
            m2 = col_m2.text_input("2º Milhar", key=f"m2_{h_idx}")
            m3 = col_m3.text_input("3º Milhar", key=f"m3_{h_idx}")
            m4 = col_m4.text_input("4º Milhar", key=f"m4_{h_idx}")
            m5 = col_m5.text_input("5º Milhar", key=f"m5_{h_idx}")
            st.markdown("---")
            
        if st.form_submit_button("🚀 Publicar e Atualizar"):
            novos = []
            for h_idx in range(1, 9):
                hora = st.session_state.get(f"h_{h_idx}")
                if hora:
                    for p in range(1, 6):
                        milhar = st.session_state.get(f"m{p}_{h_idx}")
                        if milhar:
                            centena = extrair_centena(milhar)
                            grupo = identificar_grupo(milhar)
                            novos.append({
                                "Horário": hora, "Prêmio": f"{p}º",
                                "Milhar": milhar, "Centena": centena,
                                "Grupo": grupo, "Bicho": BICHO_MAP[grupo],
                                "Loteria": loto_atual
                            })
            if novos:
                st.session_state.vagas_resultados = novos
                st.success("✅ Centenas e Grupos calculados automaticamente!")
                st.rerun()

st.divider()

# --- 2. INTERFACE DE ANÁLISE ---
df = pd.DataFrame(st.session_state.vagas_resultados)
loto_ativa = df['Loteria'].iloc[0] if not df.empty else "NACIONAL"
cor = CORES.get(loto_ativa, "#333")
st.markdown(f"<h1 style='color: {cor}; text-align: center;'>📍 Resultados de Hoje: {loto_ativa}</h1>", unsafe_allow_html=True)

# Cards (Somente 1º Prêmio para não poluir)
df_1 = df[df['Prêmio'] == "1º"].sort_values(by="Horário", ascending=False)
if not df_1.empty:
    cols = st.columns(len(df_1.head(4)))
    for i, (idx, row) in enumerate(df_1.head(4).iterrows()):
        with cols[i]:
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
    if g_vivos:
        sug = random.choice(g_vivos)
        st.markdown(f"<div style='background-color:{cor}; padding:15px; border-radius:10px; color:white; text-align:center;'><b>PRÓXIMO GRUPO PROVÁVEL</b><br><span style='font-size: 28px;'>{BICHO_MAP[sug]}</span></div>", unsafe_allow_html=True)
        
        st.markdown("#### 🎰 Milhares Sugeridos")
        g_int = int(sug)
        dezenas = [str(g_int*4).replace('100','00').zfill(2), str(g_int*4-1).zfill(2)]
        for i in range(5):
            m_s = f"{random.randint(1,9)}{random.randint(1,9)}{random.choice(dezenas)}"
            st.write(f"🔥 **{i+1}º Milhar:** {m_s} | **C:** {m_s[-3:]}")

# Termômetro
st.divider()
st.subheader("🔥 Termômetro Geral (Frequência 1º ao 5º)")
freq = df['Bicho'].value_counts().reset_index()
freq.columns = ['Bicho', 'Qtd']
fig = px.bar(freq, x='Bicho', y='Qtd', color='Bicho', text_auto=True, color_continuous_scale=[[0, '#eee'], [1, cor]])
st.plotly_chart(fig, use_container_width=True)
