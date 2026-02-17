import streamlit as st
import pandas as pd
import plotly.express as px
import random
from scraper import puxar_resultados

st.set_page_config(page_title="Monitor Vip - Elaine", layout="wide")

BICHO_MAP = {f"{i:02d}": bicho for i, bicho in enumerate(["Avestruz", "Águia", "Burro", "Borboleta", "Cachorro", "Cabra", "Carneiro", "Camelo", "Cobra", "Coelho", "Cavalo", "Elefante", "Galo", "Gato", "Jacaré", "Leão", "Macaco", "Porco", "Pavão", "Peru", "Touro", "Tigre", "Urso", "Veado", "Vaca"], 1)}
CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

st.title("🏆 Monitor Vip Pro - Elaine")

if st.button("🔄 Atualizar Resultados Agora"):
    st.session_state.dados = puxar_resultados()

if 'dados' in st.session_state and not st.session_state.dados.empty:
    df = st.session_state.dados.copy()
    df['Bicho'] = df['Grupo'].map(BICHO_MAP)
    
    escolha = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
    cor = CORES.get(escolha)
    
    df_filtrado = df[df['Loteria'] == escolha].sort_values(by="Horário", ascending=False)
    
    st.markdown(f"<h2 style='color: {cor}; text-align: center;'>📍 Resultados de Hoje: {escolha}</h2>", unsafe_allow_html=True)
    
    # 1. CARDS DE RESULTADOS
    ultimos = df_filtrado.head(5)
    cols = st.columns(len(ultimos) if not ultimos.empty else 1)
    for i, (idx, row) in enumerate(ultimos.iterrows()):
        with cols[i]:
            st.metric(label=f"Hora: {row['Horário']}", value=row['Milhar'], delta=row['Bicho'])

    st.divider()

    # 2. HISTÓRICO E PROJEÇÃO
    col_tab, col_prob = st.columns([1.5, 1])
    
    with col_tab:
        st.subheader("🕒 Histórico do Dia")
        st.table(df_filtrado[['Horário', 'Milhar', 'Grupo', 'Bicho']])

    with col_prob:
        st.subheader("🎯 Palpites e Projeções")
        grupo_provavel = random.choice([g for g in BICHO_MAP.keys() if g not in df_filtrado['Grupo'].head(2).tolist()])
        
        st.markdown(f"<div style='background-color:{cor}; padding:15px; border-radius:10px; color:white; text-align:center;'><b>PRÓXIMO GRUPO PROVÁVEL</b><br><span style='font-size: 28px; font-weight: bold;'>{grupo_provavel} - {BICHO_MAP[grupo_provavel]}</span></div>", unsafe_allow_html=True)
        
        st.write("")
        st.markdown("### 💰 Projeção de Ganhos")
        valor_aposta = st.number_input("Valor da Aposta (R$):", min_value=1.0, value=2.0)
        
        st.write(f"💵 **Grupo {grupo_provavel}**: Ganha **R$ {valor_aposta * 18:.2f}**")
        st.write(f"💎 **Milhar na Cabeça**: Ganha **R$ {valor_aposta * 4000:.2f}**")
        
        st.write("")
        st.markdown("<div style='background-color:#333;padding:10px;border-radius:10px;color:white;text-align:center;'><b>💡 Milhares Sugeridos</b></div>", unsafe_allow_html=True)
        for _ in range(2):
            g_int = int(grupo_provavel)
            d_final = str(random.randint(g_int*4-3, g_int*4)).replace('100', '00').zfill(2)
            m = str(random.randint(10, 99)) + d_final
            st.write(f"Milhar: **{m}**")

    # 3. TERMÔMETRO
    st.divider()
    st.subheader("🔥 Termômetro de Bichos")
    freq = df_filtrado['Bicho'].value_counts().reset_index()
    fig = px.bar(freq, x='Bicho', y='count', color='count', color_continuous_scale=[[0, '#eee'], [1, cor]], text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Aguardando sorteios reais de acordo com a tabela de horários.")
