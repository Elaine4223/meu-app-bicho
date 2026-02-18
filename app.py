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

def identificar_grupo(valor):
    try:
        dezena = int(str(valor)[-2:])
        if dezena == 0: return "25"
        grupo = (dezena - 1) // 4 + 1
        return str(min(grupo, 25)).zfill(2)
    except: return "01"

CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

# Dados iniciais para garantir que a interface não suma
if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = [
        {"Loteria": "NACIONAL", "Horário": "08:00", "Prêmio": "1º", "Milhar": "1224", "Grupo": "06", "Bicho": "🐐 Cabra"},
        {"Loteria": "NACIONAL", "Horário": "08:00", "Prêmio": "2º", "Milhar": "5594", "Grupo": "24", "Bicho": "🦌 Veado"}
    ]

# --- 1. CENTRAL DE LANÇAMENTO (VERTICAL POR PRÊMIO) ---
st.title("🏆 Central de Lançamento Profissional PRO")
with st.expander("📥 Painel de Lançamento Vertical (1º ao 5º Prêmio)", expanded=False):
    with st.form("form_vertical_8x5"):
        loto_atual = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
        
        # Loop para criar 8 blocos de horários
        for h_idx in range(1, 9):
            st.markdown(f"### ⏰ Horário {h_idx}")
            col_h, _ = st.columns([1, 4])
            hora = col_h.text_input(f"Horário {h_idx}", key=f"h_{h_idx}", placeholder="08:00")
            
            # Cabeçalho da tabela interna
            c_header = st.columns([0.5, 1, 1, 1])
            c_header[0].write("**Prêmio**")
            c_header[1].write("**Milhar**")
            c_header[2].write("**Centena**")
            c_header[3].write("**Grupo**")
            
            # 5 linhas de prêmios para cada horário
            for p_idx in range(1, 6):
                cp, cm, cc, cg = st.columns([0.5, 1, 1, 1])
                cp.write(f"**{p_idx}º**")
                m_val = cm.text_input(f"M{p_idx}_{h_idx}", key=f"m{p_idx}_{h_idx}", label_visibility="collapsed")
                c_val = cc.text_input(f"C{p_idx}_{h_idx}", key=f"c{p_idx}_{h_idx}", label_visibility="collapsed")
                g_val = cg.text_input(f"G{p_idx}_{h_idx}", key=f"g{p_idx}_{h_idx}", label_visibility="collapsed")
            st.markdown("---")
            
        if st.form_submit_button("🚀 Gravar e Sincronizar Monitor"):
            temp_dados = [] 
            for h_idx in range(1, 9):
                h_final = st.session_state.get(f"h_{h_idx}")
                if h_final:
                    for p_idx in range(1, 6):
                        milhar = st.session_state.get(f"m{p_idx}_{h_idx}")
                        if milhar:
                            g_manual = st.session_state.get(f"g{p_idx}_{h_idx}")
                            g_final = g_manual if g_manual else identificar_grupo(milhar)
                            temp_dados.append({
                                "Loteria": loto_atual, "Horário": h_final, 
                                "Prêmio": f"{p_idx}º", "Milhar": milhar, 
                                "Grupo": g_final, "Bicho": BICHO_MAP.get(g_final, "Sorte")
                            })
            if temp_dados:
                st.session_state.vagas_resultados = temp_dados
                st.success("Painel atualizado com sucesso!")
                st.rerun()

st.divider()

# --- 2. INTERFACE DE ANÁLISE ---
df = pd.DataFrame(st.session_state.vagas_resultados)
loto_ativa = df['Loteria'].iloc[0] if not df.empty else "NACIONAL"
cor = CORES.get(loto_ativa, "#333")

st.markdown(f"<h1 style='color: {cor}; text-align: center;'>📍 Monitor: {loto_ativa}</h1>", unsafe_allow_html=True)

# Cards (Destaque do 1º Prêmio)
df_1 = df[df['Prêmio'] == "1º"].sort_values(by="Horário", ascending=False)
if not df_1.empty:
    cols = st.columns(len(df_1.head(4)))
    for i, (idx, row) in enumerate(df_1.head(4).iterrows()):
        with cols[i]:
            st.metric(label=f"1º - {row['Horário']}", value=row['Milhar'], delta=row['Bicho'])

st.divider()

c1, c2 = st.columns([1.5, 1])
with c1:
    st.subheader("🕒 Histórico do Dia (1º ao 5º)")
    st.dataframe(df.sort_values(by=["Horário", "Prêmio"]), use_container_width=True)

with c2:
    st.subheader("🎯 Palpite VIP")
    g_1_saiu = df[df['Prêmio'] == "1º"]['Grupo'].tolist()
    g_vivos = [g for g in BICHO_MAP.keys() if g not in g_1_saiu]
    if g_vivos:
        sug = random.choice(g_vivos)
        st.markdown(f"<div style='background-color:{cor}; padding:25px; border-radius:15px; color:white; text-align:center;'><b>FORTE PARA O PRÓXIMO</b><br><span style='font-size: 32px; font-weight: bold;'>{BICHO_MAP[sug]}</span></div>", unsafe_allow_html=True)

# Termômetro Geral
st.divider()
st.subheader("🔥 Termômetro Geral (1º ao 5º)")
freq = df['Bicho'].value_counts().reset_index()
freq.columns = ['Bicho', 'Qtd']
fig = px.bar(freq, x='Bicho', y='Qtd', color='Bicho', text_auto=True, color_continuous_scale=[[0, '#eee'], [1, cor]])
st.plotly_chart(fig, use_container_width=True)
