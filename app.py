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

def identificar_grupo(valor):
    try:
        dezena = int(str(valor)[-2:])
        if dezena == 0: return "25"
        grupo = (dezena - 1) // 4 + 1
        return str(min(grupo, 25)).zfill(2)
    except: return "01"

CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

# --- INICIALIZAÇÃO COM DADOS REAIS PARA INTERFACE APARECER ---
if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = [
        {"Loteria": "NACIONAL", "Horário": "08:00", "Prêmio": "1º", "Milhar": "1224", "Grupo": "06", "Bicho": "🐐 Cabra"},
        {"Loteria": "NACIONAL", "Horário": "08:00", "Prêmio": "2º", "Milhar": "5594", "Grupo": "24", "Bicho": "🦌 Veado"}
    ]

# --- 1. CENTRAL DE LANÇAMENTO (8 HORÁRIOS X 5 PRÊMIOS) ---
st.title("🏆 Central de Lançamento Profissional")
with st.expander("📥 Painel de Entrada Completo (1º ao 5º Prêmio)", expanded=False):
    with st.form("form_8x5_final"):
        loto_atual = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
        
        for h_idx in range(1, 9):
            st.markdown(f"#### ⏰ Horário {h_idx}")
            col_hora, col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns([1.2, 1, 1, 1, 1, 1])
            
            h_val = col_hora.text_input("Hora", key=f"h_{h_idx}", placeholder="Ex: 10:00")
            m1 = col_p1.text_input("1º Milhar", key=f"m1_{h_idx}")
            m2 = col_p2.text_input("2º Milhar", key=f"m2_{h_idx}")
            m3 = col_p3.text_input("3º Milhar", key=f"m3_{h_idx}")
            m4 = col_p4.text_input("4º Milhar", key=f"m4_{h_idx}")
            m5 = col_p5.text_input("5º Milhar", key=f"m5_{h_idx}")
            st.markdown("---")
            
        if st.form_submit_button("🚀 Gravar e Sincronizar Tudo"):
            temp_dados = [] 
            for h_idx in range(1, 9):
                hora = st.session_state.get(f"h_{h_idx}")
                if hora:
                    for p_idx in range(1, 6):
                        milhar = st.session_state.get(f"m{p_idx}_{h_idx}")
                        if milhar:
                            g = identificar_grupo(milhar)
                            temp_dados.append({
                                "Loteria": loto_atual, "Horário": hora, 
                                "Prêmio": f"{p_idx}º", "Milhar": milhar, 
                                "Grupo": g, "Bicho": BICHO_MAP.get(g, "Sorte")
                            })
            if temp_dados:
                st.session_state.vagas_resultados = temp_dados
                st.success("Painel de Análise Atualizado com 40 slots!")
                st.rerun()

st.divider()

# --- 2. INTERFACE DE ANÁLISE ---
df = pd.DataFrame(st.session_state.vagas_resultados)
loto_ativa = df['Loteria'].iloc[0] if not df.empty else "NACIONAL"
cor = CORES.get(loto_ativa, "#333")

st.markdown(f"<h1 style='color: {cor}; text-align: center;'>📍 Monitor: {loto_ativa}</h1>", unsafe_allow_html=True)

# Cards apenas do 1º Prêmio para não poluir o topo
df_1 = df[df['Prêmio'] == "1º"].sort_values(by="Horário", ascending=False)
if not df_1.empty:
    cols_cards = st.columns(len(df_1.head(4)))
    for i, (idx, row) in enumerate(df_1.head(4).iterrows()):
        with cols_cards[i]:
            st.metric(label=f"1º Prêmio - {row['Horário']}", value=row['Milhar'], delta=row['Bicho'])

st.divider()

c_hist, c_palp = st.columns([1.5, 1])
with c_hist:
    st.subheader("🕒 Histórico do Dia (1º ao 5º)")
    st.dataframe(df.sort_values(by=["Horário", "Prêmio"]), use_container_width=True)

with c_palp:
    st.subheader("🎯 Palpite VIP")
    # Palpite exclui grupos que saíram no 1º prêmio
    g_ja_foi = df[df['Prêmio'] == "1º"]['Grupo'].tolist()
    g_vivos = [g for g in BICHO_MAP.keys() if g not in g_ja_foi]
    if g_vivos:
        sug = random.choice(g_vivos)
        st.markdown(f"<div style='background-color:{cor}; padding:25px; border-radius:15px; color:white; text-align:center;'><b>FORTE PARA O PRÓXIMO</b><br><span style='font-size: 32px; font-weight: bold;'>{BICHO_MAP[sug]}</span></div>", unsafe_allow_html=True)

# Termômetro usa TODOS os prêmios (1º ao 5º) para precisão máxima
st.divider()
st.subheader("🔥 Termômetro Geral (Frequência do 1º ao 5º)")
if not df.empty:
    freq = df['Bicho'].value_counts().reset_index()
    freq.columns = ['Bicho', 'Qtd']
    fig = px.bar(freq, x='Bicho', y='Qtd', color='Bicho', text_auto=True, color_continuous_scale=[[0, '#eee'], [1, cor]])
    st.plotly_chart(fig, use_container_width=True)
