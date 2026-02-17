import streamlit as st
import pandas as pd
import plotly.express as px
import random
from scraper import puxar_resultados

st.set_page_config(page_title="Monitor Vip - Elaine", layout="wide")

# --- DICIONÁRIO DE BICHOS ---
BICHO_MAP = {
    "01": "Avestruz", "02": "Águia", "03": "Burro", "04": "Borboleta",
    "05": "Cachorro", "06": "Cabra", "07": "Carneiro", "08": "Camelo",
    "09": "Cobra", "10": "Coelho", "11": "Cavalo", "12": "Elefante",
    "13": "Galo", "14": "Gato", "15": "Jacaré", "16": "Leão",
    "17": "Macaco", "18": "Porco", "19": "Pavão", "20": "Peru",
    "21": "Touro", "22": "Tigre", "23": "Urso", "24": "Veado", "25": "Vaca"
}

st.title("📊 Monitor de Loterias Pro - Elaine")

if st.button("🔄 Atualizar e Gerar Probabilidades"):
    st.session_state.dados = puxar_resultados()
    st.success("Dados atualizados!")

if 'dados' in st.session_state:
    df = st.session_state.dados.copy()
    df['Bicho'] = df['Grupo'].map(BICHO_MAP).fillna("Desconhecido")
    
    # --- FILTRO POR LOTERIA ---
    loterias_alvo = ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"]
    escolha = st.selectbox("Selecione a Loteria:", loterias_alvo)
    df_filtrado = df[df['Loteria'].str.contains(escolha, case=False, na=False)]
    
    # --- TABELA COMPARATIVA ---
    st.subheader(f"🕒 Comparativo de Horários: {escolha}")
    st.dataframe(df_filtrado[['Horário', 'Milhar', 'Grupo', 'Bicho']], use_container_width=True)

    # --- NOVO ÍTEM: PROBABILIDADES DE MILHAR E CENTENA ---
    st.divider()
    st.subheader(f"🎯 Sugestão de Probabilidades ({escolha})")
    
    # Lógica: Sugere milhares baseados nos grupos que mais saem (Quentes) e menos saem (Atrasados)
    grupos_quentes = df_filtrado['Grupo'].value_counts().index.tolist()[:3]
    todos_grupos = [f"{i:02d}" for i in range(1, 26)]
    atrasados = [g for g in todos_grupos if g not in df_filtrado['Grupo'].unique()][:2]
    
    p1, p2 = st.columns(2)
    
    with p1:
        st.write("🔥 **Baseado nos Quentes (Tendência):**")
        for g in grupos_quentes:
            dezena_base = random.randint(int(g)*4-3, int(g)*4)
            sugestao = f"{random.randint(10, 99)}{dezena_base:02d}"
            st.info(f"Bicho: {BICHO_MAP.get(g)} | Centena: {sugestao[1:]} | **Milhar: {sugestao}**")

    with p2:
        st.write("⌛ **Baseado nos Atrasados (Ciclo):**")
        for g in atrasados:
            dezena_base = random.randint(int(g)*4-3, int(g)*4)
            sugestao = f"{random.randint(10, 99)}{dezena_base:02d}"
            st.warning(f"Bicho: {BICHO_MAP.get(g)} | Centena: {sugestao[1:]} | **Milhar: {sugestao}**")

    # --- TERMÔMETRO ---
    st.divider()
    st.subheader(f"🔥 Termômetro de Grupos ({escolha})")
    frequencia = df_filtrado['Grupo'].value_counts().reset_index()
    frequencia.columns = ['Grupo', 'Frequência']
    frequencia['Bicho'] = frequencia['Grupo'].map(BICHO_MAP)
    fig = px.bar(frequencia, x='Bicho', y='Frequência', color='Frequência', color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)

    # --- RESUMO DO DIA EM CARDS ---
    st.subheader(f"📅 Resumo por Horário")
    ultimos_do_dia = df_filtrado.head(5)
    cols_resumo = st.columns(len(ultimos_do_dia))
    for i, (idx, row) in enumerate(ultimos_do_dia.iterrows()):
        with cols_resumo[i]:
            st.metric(label=row['Horário'], value=row['Milhar'], delta=row['Bicho'])

    # --- SIMULADOR NA LATERAL ---
    st.sidebar.header("🎰 Simulador")
    meu_palpite = st.sidebar.text_input("Seu Palpite:")
    if meu_palpite:
        ganhou = df_filtrado[df_filtrado['Milhar'].astype(str).str.contains(meu_palpite) | (df_filtrado['Grupo'] == meu_palpite)]
        if not ganhou.empty:
            st.sidebar.balloons()
            st.sidebar.success(f"✅ GANHOU NA {escolha}!")
        else:
            st.sidebar.error("❌ Não saiu ainda.")
else:
    st.info("Clique no botão atualizar para ver as probabilidades.")
