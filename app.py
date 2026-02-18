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



def obter_bicho(grupo):

    return BICHO_MAP.get(str(grupo).zfill(2), "Sorte")



CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}



if 'vagas_resultados' not in st.session_state:

    st.session_state.vagas_resultados = [

        {"Loteria": "NACIONAL", "Horário": "08:00", "Prêmio": "1º", "Milhar": "1224", "Centena": "224", "Grupo": "06", "Bicho": "🐐 Cabra"}

    ]



# --- 1. CENTRAL DE LANÇAMENTO VERTICAL ---

st.title("🏆 Central de Lançamento VIP")

with st.expander("📥 Painel Manual (1º ao 5º Prêmio)", expanded=False):

    with st.form("form_final_v1"):

        loto_atual = st.selectbox("Selecione a Loteria:", list(CORES.keys()))

        for h_idx in range(1, 9):

            st.markdown(f"### ⏰ Horário {h_idx}")

            col_h, _ = st.columns([1, 4])

            hora = col_h.text_input(f"Horário", key=f"h_{h_idx}", placeholder="Ex: 08:00")

            c_header = st.columns([0.5, 1, 1, 1])

            c_header[0].write("**Prêmio**")

            c_header[1].write("**Milhar**")

            c_header[2].write("**Centena**")

            c_header[3].write("**Grupo**")

            for p_idx in range(1, 6):

                cp, cm, cc, cg = st.columns([0.5, 1, 1, 1])

                cp.write(f"**{p_idx}º**")

                m_v = cm.text_input(f"M{p_idx}_{h_idx}", key=f"m{p_idx}_{h_idx}", label_visibility="collapsed")

                c_v = cc.text_input(f"C{p_idx}_{h_idx}", key=f"c{p_idx}_{h_idx}", label_visibility="collapsed")

                g_v = cg.text_input(f"G{p_idx}_{h_idx}", key=f"g{p_idx}_{h_idx}", label_visibility="collapsed")

            st.markdown("---")

        if st.form_submit_button("🚀 Atualizar Monitor"):

            temp = [] 

            for h_idx in range(1, 9):

                hf = st.session_state.get(f"h_{h_idx}")

                if hf:

                    for p_idx in range(1, 6):

                        m = st.session_state.get(f"m{p_idx}_{h_idx}")

                        g = st.session_state.get(f"g{p_idx}_{h_idx}")

                        c = st.session_state.get(f"c{p_idx}_{h_idx}")

                        if m and g:

                            temp.append({"Loteria": loto_atual, "Horário": hf, "Prêmio": f"{p_idx}º", "Milhar": m, "Centena": c, "Grupo": g, "Bicho": obter_bicho(g)})

            if temp:

                st.session_state.vagas_resultados = temp

                st.rerun()



st.divider()



# --- 2. INTERFACE DE ANÁLISE ---

df = pd.DataFrame(st.session_state.vagas_resultados)

loto_ativa = df['Loteria'].iloc[0] if not df.empty else "NACIONAL"

cor = CORES.get(loto_ativa, "#333")

st.markdown(f"<h1 style='color: {cor}; text-align: center;'>📍 Resultados de Hoje: {loto_ativa}</h1>", unsafe_allow_html=True)



# Cards 1º Prêmio

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

        dezenas = [str(g_int*4).replace('100','00').zfill(2), str(g_int*4-1).zfill(2), str(g_int*4-2).zfill(2), str(g_int*4-3).zfill(2)]

        for i in range(5):

            m_sug = f"{random.randint(0,9)}{random.choice(dezenas).zfill(3)}"

            st.write(f"🔥 **{i+1}º Milhar:** {random.randint(1,9)}{m_sug[-3:]} | **C:** {m_sug[-3:]}")



# Termômetro

st.divider()

st.subheader("🔥 Termômetro Geral (Frequência 1º ao 5º)")

freq = df['Bicho'].value_counts().reset_index()

freq.columns = ['Bicho', 'Qtd']

fig = px.bar(freq, x='Bicho', y='Qtd', color='Bicho', text_auto=True, color_continuous_scale=[[0, '#eee'], [1, cor]])

st.plotly_chart(fig, use_container_width=True)
