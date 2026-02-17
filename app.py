import streamlit as st
import pandas as pd
import plotly.express as px
import random
from scraper import puxar_resultados
from datetime import datetime

st.set_page_config(page_title="Monitor Vip - Elaine", layout="wide")

# --- DICIONÁRIO DE BICHOS OFICIAL ---
BICHO_MAP = {f"{i:02d}": bicho for i, bicho in enumerate(["Avestruz", "Águia", "Burro", "Borboleta", "Cachorro", "Cabra", "Carneiro", "Camelo", "Cobra", "Coelho", "Cavalo", "Elefante", "Galo", "Gato", "Jacaré", "Leão", "Macaco", "Porco", "Pavão", "Peru", "Touro", "Tigre", "Urso", "Veado", "Vaca"], 1)}
CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

st.title("📊 Monitor Vip Pro - Painel Completo")

if st.button("🔄 Atualizar Resultados Agora"):
    st.session_state.dados = puxar_resultados()

if 'dados' in st.session_state and not st.session_state.dados.empty:
    df = st.session_state.dados.copy()
    df['Bicho'] = df['Grupo'].map(BICHO_MAP)
    
    # Menu de seleção que o Simulador passará a respeitar
    escolha = st.selectbox("Selecione a Loteria para Análise:", list(CORES.keys()))
    cor = CORES.get(escolha)
    
    # Filtro da Loteria Selecionada
    df_filtrado = df[df['Loteria'] == escolha].sort_values(by="Horário", ascending=False)
    
    st.markdown(f"<h2 style='color: {cor}; text-align: center;'>📍 Resultados de Hoje: {escolha}</h2>", unsafe_allow_html=True)
    
    # --- 1. RESUMO EM CARDS ---
    ultimos_hoje = df_filtrado.head(5) 
    cols = st.columns(len(ultimos_hoje))
    for i, (idx, row) in enumerate(ultimos_hoje.iterrows()):
        with cols[i]:
            st.metric(label=f"Hora: {row['Horário']}", value=row['Milhar'], delta=row['Bicho'])

    st.divider()

    # --- 2. HISTÓRICO E PALPITES ---
    col_tab, col_prob = st.columns([1.5, 1])
    with col_tab:
        st.subheader("🕒 Histórico do Dia")
        st.table(df_filtrado[['Horário', 'Milhar', 'Grupo', 'Bicho']])

    with col_prob:
        st.subheader("🎯 Palpites VIP")
        grupos_recentes = df_filtrado['Grupo'].head(3).tolist()
        grupo_provavel = random.choice([g for g in BICHO_MAP.keys() if g not in grupos_recentes])
        
        st.markdown(f"<div style='background-color:{cor}; padding:15px; border-radius:10px; color:white; text-align:center;'><b>PRÓXIMO GRUPO PROVÁVEL</b><br><span style='font-size: 28px; font-weight: bold;'>{grupo_provavel} - {BICHO_MAP[grupo_provavel]}</span></div>", unsafe_allow_html=True)
        
        st.write("")
        st.markdown("<div style='background-color:#333;padding:10px;border-radius:10px;color:white;text-align:center;'><b>💡 Milhares Sugeridos</b></div>", unsafe_allow_html=True)
        for _ in range(2):
            g_int = int(grupo_provavel)
            d_max = g_int * 4
            d_final = str(random.randint(d_max-3, d_max)).replace('100', '00').zfill(2)
            m = str(random.randint(10, 99)) + d_final
            st.write(f"Milhar: **{m}** | Centena: {m[1:]}")

    # --- 3. TERMÔMETRO ---
    st.divider()
    st.subheader("🔥 Termômetro de Bichos")
    freq = df_filtrado['Bicho'].value_counts().reset_index()
    freq.columns = ['Bicho', 'Frequência']
    fig = px.bar(freq, x='Bicho', y='Frequência', color='Frequência', color_continuous_scale=[[0, '#eee'], [1, cor]])
    st.plotly_chart(fig, use_container_width=True)

    # --- SIMULADOR NA LATERAL (AGORA AMARRADO À LOTERIA ESCOLHIDA) ---
    st.sidebar.header(f"🎰 Simulador ({escolha})")
    meu_palpite = st.sidebar.text_input("Seu Palpite (Milhar ou Grupo):")
    valor_aposta = st.sidebar.number_input("Valor da Aposta (R$):", min_value=1.0, value=1.0)
    
    if meu_palpite:
        # AQUI ESTÁ O SEGREDO: Ele busca apenas no 'df_filtrado' (que já é a loteria certa)
        ganhou = df_filtrado[df_filtrado['Milhar'].str.contains(meu_palpite) | (df_filtrado['Grupo'] == meu_palpite)]
        if not ganhou.empty:
            st.sidebar.balloons()
            fator = 4000 if len(meu_palpite) == 4 else 15
            st.sidebar.success(f"✅ GANHOU NA {escolha}! Prêmio: R$ {valor_aposta * fator:.2f}")
        else:
            st.sidebar.error(f"❌ Não saiu na {escolha} ainda.")
else:
    st.info("Aguardando sorteios ou clique em 'Atualizar Resultados Agora'.")
