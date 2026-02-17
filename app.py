import streamlit as st
import pandas as pd
import plotly.express as px
import random
from scraper import puxar_resultados
from datetime import datetime

st.set_page_config(page_title="Monitor Vip - Elaine", layout="wide")

BICHO_MAP = {f"{i:02d}": bicho for i, bicho in enumerate(["Avestruz", "Águia", "Burro", "Borboleta", "Cachorro", "Cabra", "Carneiro", "Camelo", "Cobra", "Coelho", "Cavalo", "Elefante", "Galo", "Gato", "Jacaré", "Leão", "Macaco", "Porco", "Pavão", "Peru", "Touro", "Tigre", "Urso", "Veado", "Vaca"], 1)}
CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

st.title("📊 Monitor Vip Pro - Painel Inteligente")

if st.button("🔄 Atualizar Resultados Agora"):
    st.session_state.dados = puxar_resultados()

if 'dados' in st.session_state and not st.session_state.dados.empty:
    df = st.session_state.dados.copy()
    df['Bicho'] = df['Grupo'].map(BICHO_MAP)
    
    escolha = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
    cor = CORES.get(escolha)
    
    # Filtro e Ordenação (Mais recente primeiro)
    df_filtrado = df[df['Loteria'] == escolha].sort_values(by="Horário", ascending=False)
    
    st.markdown(f"<h2 style='color: {cor};'>📍 Resultados de Hoje: {escolha}</h2>", unsafe_allow_html=True)
    
    # 1. RESUMO EM CARDS
    ultimos_hoje = df_filtrado.head(5) 
    cols = st.columns(len(ultimos_hoje))
    for i, (idx, row) in enumerate(ultimos_hoje.iterrows()):
        with cols[i]:
            st.metric(label=f"Hora: {row['Horário']}", value=row['Milhar'], delta=row['Bicho'])

    st.divider()

    # 2. TABELA E PALPITES
    col_tab, col_prob = st.columns([1.5, 1])
    with col_tab:
        st.subheader("🕒 Histórico do Dia")
        st.table(df_filtrado[['Horário', 'Milhar', 'Grupo', 'Bicho']])

    with col_prob:
        st.subheader("🎯 Palpites VIP")
        grupo_provavel = random.choice([g for g in BICHO_MAP.keys() if g not in df_filtrado['Grupo'].head(2).tolist()])
        
        st.markdown(f"<div style='background-color:{cor}; padding:15px; border-radius:10px; color:white; text-align:center;'><b>PRÓXIMO GRUPO PROVÁVEL</b><br><span style='font-size: 28px;'>{grupo_provavel} - {BICHO_MAP[grupo_provavel]}</span></div>", unsafe_allow_html=True)
        
        st.write("")
        st.markdown("<div style='background-color:#333;padding:10px;border-radius:10px;color:white'><b>💡 Milhares Sugeridos</b></div>", unsafe_allow_html=True)
        for _ in range(2):
            g_int = int(grupo_provavel)
            d_max = g_int * 4
            d_final = str(random.randint(d_max-3, d_max)).replace('100', '00').zfill(2)
            m = str(random.randint(10, 99)) + d_final
            st.write(f"Milhar: **{m}** | Centena: {m[1:]}")

    # --- SIMULADOR NA LATERAL ---
    st.sidebar.header("🎰 Simulador")
    meu_palpite = st.sidebar.text_input("Seu Palpite:")
    valor_aposta = st.sidebar.number_input("Valor (R$):", min_value=1.0, value=1.0)
    if meu_palpite:
        ganhou = df_filtrado[df_filtrado['Milhar'].str.contains(meu_palpite) | (df_filtrado['Grupo'] == meu_palpite)]
        if not ganhou.empty:
            st.sidebar.balloons()
            st.sidebar.success(f"✅ GANHOU! Prêmio est.: R$ {valor_aposta * 15:.2f}")
        else:
            st.sidebar.error("❌ Não saiu ainda.")
else:
    st.info("Aguardando o primeiro sorteio do dia (11:00) ou clique em Atualizar.")
