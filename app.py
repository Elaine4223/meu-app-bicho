import streamlit as st
import pandas as pd
import plotly.express as px
import random
from scraper import puxar_resultados
from datetime import datetime

st.set_page_config(page_title="Monitor Vip - Elaine", layout="wide")

# --- DICIONÁRIO DE BICHOS ---
BICHO_MAP = {f"{i:02d}": bicho for i, bicho in enumerate(["Avestruz", "Águia", "Burro", "Borboleta", "Cachorro", "Cabra", "Carneiro", "Camelo", "Cobra", "Coelho", "Cavalo", "Elefante", "Galo", "Gato", "Jacaré", "Leão", "Macaco", "Porco", "Pavão", "Peru", "Touro", "Tigre", "Urso", "Veado", "Vaca"], 1)}

# --- CORES POR LOTERIA ---
CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

st.title("📊 Monitor Vip Pro - Painel Inteligente")

if st.button("🔄 Atualizar e Gerar Probabilidades"):
    st.session_state.dados = puxar_resultados()

if 'dados' in st.session_state:
    df = st.session_state.dados.copy()
    df['Bicho'] = df['Grupo'].map(BICHO_MAP)
    
    escolha = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
    cor = CORES.get(escolha)
    st.markdown(f"<h2 style='color: {cor};'>📍 Análise: {escolha}</h2>", unsafe_allow_html=True)
    
    # Filtro apenas para a loteria escolhida
    df_filtrado = df[df['Loteria'] == escolha].sort_values(by="Horário", ascending=False)
    
    # --- 1. RESUMO DOS ÚLTIMOS HORÁRIOS (APENAS HOJE) ---
    st.subheader(f"📅 Resultados de Hoje - {datetime.now().strftime('%d/%m')}")
    ultimos_hoje = df_filtrado.head(5) 
    cols = st.columns(len(ultimos_hoje))
    for i, (idx, row) in enumerate(ultimos_hoje.iterrows()):
        with cols[i]:
            st.metric(label=f"Hora: {row['Horário']}", value=row['Milhar'], delta=row['Bicho'])

    st.divider()

    # --- 2. PROBABILIDADES E PRÓXIMO GRUPO ---
    col_tab, col_prob = st.columns([1.5, 1])
    
    with col_tab:
        st.subheader("🕒 Comparativo de Horários")
        st.table(df_filtrado[['Horário', 'Milhar', 'Grupo', 'Bicho']].head(10))

    with col_prob:
        st.subheader("🎯 Palpites VIP")
        
        # Lógica de Probabilidade do Grupo para o Próximo Sorteio
        # Escolhe um grupo que não saiu nos últimos 3 horários
        grupo_provavel = random.choice([g for g in BICHO_MAP.keys() if g not in df_filtrado['Grupo'].head(3).tolist()])
        
        st.markdown(f"""
        <div style='background-color:{cor}; padding:15px; border-radius:10px; color:white; text-align:center;'>
            <span style='font-size: 14px;'>PRÓXIMO GRUPO PROVÁVEL</span><br>
            <span style='font-size: 32px; font-weight: bold;'>{grupo_provavel} - {BICHO_MAP[grupo_provavel]}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.markdown(f"<div style='background-color:#333;padding:10px;border-radius:10px;color:white'><b>💡 Milhares Sugeridos</b></div>", unsafe_allow_html=True)
        
        # --- LÓGICA DE DEZENAS CORRIGIDA ---
        for _ in range(2):
            g_int = int(grupo_provavel)
            d_max = g_int * 4
            # Escolhe uma dezena entre as 4 do grupo e corrige o "100" para "00"
            d_sorteada = random.randint(d_max-3, d_max)
            d_final = str(d_sorteada).replace('100', '00').zfill(2)
            # Monta o milhar final
            m = str(random.randint(10, 99)) + d_final
            st.write(f"Milhar: **{m}** | Centena: {m[1:]}")

    # --- 3. TERMÔMETRO ---
    st.divider()
    st.subheader("🔥 Termômetro: Bichos que mais saíram")
    freq = df_filtrado['Bicho'].value_counts().reset_index()
    fig = px.bar(freq, x='Bicho', y='count', color='count', color_continuous_scale=[[0, '#eee'], [1, cor]])
    st.plotly_chart(fig, use_container_width=True)

    # --- SIMULADOR NA LATERAL (COM VALOR DA APOSTA) ---
    st.sidebar.header("🎰 Simulador de Apostas")
    meu_palpite = st.sidebar.text_input("Seu Palpite (Milhar ou Grupo):")
    valor_aposta = st.sidebar.number_input("Valor da Aposta (R$):", min_value=1.0, value=1.0)
    
    if meu_palpite:
        ganhou = df_filtrado[df_filtrado['Milhar'].str.contains(meu_palpite) | (df_filtrado['Grupo'] == meu_palpite)]
        if not ganhou.empty:
            st.sidebar.balloons()
            # Cálculo de prêmio (exemplo: milhar paga 4000x, grupo paga 15x)
            fator = 4000 if len(meu_palpite) == 4 else 15
            premio = valor_aposta * fator
            st.sidebar.success(f"✅ GANHOU! Prêmio est.: R$ {premio:.2f}")
        else:
            st.sidebar.error("❌ Não saiu ainda.")
else:
    st.info("Clique no botão 'Atualizar' para carregar seu painel VIP.")
