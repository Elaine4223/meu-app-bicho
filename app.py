import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="Monitor Ouro da Sorte - Elaine", layout="wide")

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

if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = []

# --- 1. CENTRAL DE LANÇAMENTO (ESTRUTURA EM COLUNAS) ---
st.title("🏆 Central de Lançamento Profissional")
with st.expander("📥 Painel de Entrada - 8 Horários Disponíveis", expanded=True):
    with st.form("form_8_horarios_colunas"):
        loto_atual = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
        
        # Cabeçalho das Colunas
        header_cols = st.columns([1, 1, 1, 1])
        header_cols[0].markdown("**Horário**")
        header_cols[1].markdown("**Milhar**")
        header_cols[2].markdown("**Centena**")
        header_cols[3].markdown("**Grupo**")
        
        for i in range(1, 9):
            c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
            horario = c1.text_input(f"H{i}", key=f"h{i}", label_visibility="collapsed", placeholder="Ex: 10:00")
            milhar = c2.text_input(f"M{i}", key=f"m{i}", label_visibility="collapsed", placeholder="Milhar")
            centena = c3.text_input(f"C{i}", key=f"c{i}", label_visibility="collapsed", placeholder="Centena")
            grupo = c4.text_input(f"G{i}", key=f"g{i}", label_visibility="collapsed", placeholder="Grupo")
            
        if st.form_submit_button("🚀 Gravar e Sincronizar Monitor"):
            temp_dados = [] 
            for i in range(1, 9):
                h = st.session_state[f"h{i}"]
                m = st.session_state[f"m{i}"]
                if h and m:
                    # Se centena/grupo estiverem vazios, o sistema calcula do milhar
                    g_final = st.session_state[f"g{i}"] if st.session_state[f"g{i}"] else identificar_grupo(m)
                    temp_dados.append({
                        "Loteria": loto_atual, "Horário": h, 
                        "Milhar": m, "Grupo": g_final, "Bicho": BICHO_MAP.get(g_final, "Sorte")
                    })
            if temp_dados:
                st.session_state.vagas_resultados = temp_dados
                st.success("Dados processados com sucesso!")
                st.rerun()

st.divider()

# --- 2. INTERFACE DE ANÁLISE ---
if st.session_state.vagas_resultados:
    df = pd.DataFrame(st.session_state.vagas_resultados)
    loto_ativa = df['Loteria'].iloc[0]
    cor = CORES.get(loto_ativa, "#333")
    
    st.markdown(f"<h1 style='color: {cor}; text-align: center;'>📍 Monitor: {loto_ativa}</h1>", unsafe_allow_html=True)

    # Resumo Visual
    df_c = df.sort_values(by="Horário", ascending=False)
    cols = st.columns(len(df_c.head(4)))
    for i, (idx, row) in enumerate(df_c.head(4).iterrows()):
        with cols[i]:
            st.metric(label=f"⏰ {row['Horário']}", value=row['Milhar'], delta=row['Bicho'])

    st.divider()

    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.subheader("🕒 Histórico Detalhado")
        st.dataframe(df_c[['Horário', 'Milhar', 'Grupo', 'Bicho']], use_container_width=True)

    with c2:
        st.subheader("🎯 Sugestão da IA")
        g_vivos = [g for g in BICHO_MAP.keys() if g not in df['Grupo'].tolist()]
        if g_vivos:
            sug = random.choice(g_vivos)
            st.markdown(f"<div style='background-color:{cor}; padding:25px; border-radius:15px; color:white; text-align:center;'><b>TENDÊNCIA PARA AGORA</b><br><span style='font-size: 32px; font-weight: bold;'>{BICHO_MAP[sug]}</span></div>", unsafe_allow_html=True)

    st.divider()
    st.subheader("🔥 Termômetro de Frequência (Análise dos 8 Horários)")
    freq = df['Bicho'].value_counts().reset_index()
    freq.columns = ['Bicho', 'Qtd']
    fig = px.bar(freq, x='Bicho', y='Qtd', color='Bicho', text_auto=True, color_continuous_scale=[[0, '#eee'], [1, cor]])
    st.plotly_chart(fig, use_container_width=True)
