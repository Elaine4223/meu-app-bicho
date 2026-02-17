import streamlit as st
import pandas as pd
import plotly.express as px
from scraper import puxar_resultados

st.set_page_config(page_title="Monitor Vip - Elaine", layout="wide")

# --- DICIONÁRIO PARA TRADUZIR GRUPO EM BICHO ---
BICHO_MAP = {
    "01": "Avestruz", "02": "Águia", "03": "Burro", "04": "Borboleta",
    "05": "Cachorro", "06": "Cabra", "07": "Carneiro", "08": "Camelo",
    "09": "Cobra", "10": "Coelho", "11": "Cavalo", "12": "Elefante",
    "13": "Galo", "14": "Gato", "15": "Jacaré", "16": "Leão",
    "17": "Macaco", "18": "Porco", "19": "Pavão", "20": "Peru",
    "21": "Touro", "22": "Tigre", "23": "Urso", "24": "Veado", "25": "Vaca"
}

st.title("📊 Monitor de Loterias Pro - Elaine")

if st.button("🔄 Atualizar Dados e Analisar"):
    st.session_state.dados = puxar_resultados()
    st.success("Dados atualizados com sucesso!")

if 'dados' in st.session_state:
    df = st.session_state.dados.copy()
    
    # --- AQUI ESTÁ O CONSERTO DO "CARREGANDO" ---
    # Ele olha a coluna 'Grupo' e coloca o nome do bicho na coluna 'Bicho'
    df['Bicho'] = df['Grupo'].map(BICHO_MAP).fillna("Desconhecido")
    
    # --- FILTRO POR LOTERIA ---
    loterias_alvo = ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"]
    escolha = st.selectbox("Selecione a Loteria para Análise:", loterias_alvo)
    
    df_filtrado = df[df['Loteria'].str.contains(escolha, case=False, na=False)]
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"📍 Últimos Resultados: {escolha}")
        st.dataframe(df_filtrado, use_container_width=True)

    with col2:
        # --- LÓGICA DE ATRASO REAL ---
        st.subheader("⚠️ Alerta de Atraso")
        todos_grupos = [f"{i:02d}" for i in range(1, 26)]
        grupos_que_sairam = df_filtrado['Grupo'].unique()
        atrasados = [g for g in todos_grupos if g not in grupos_que_sairam]
        
        if atrasados:
            st.warning(f"Grupos que NÃO saíram na {escolha}:")
            # Mostra o número e o nome do bicho atrasado
            lista_atrasados = [f"{g} ({BICHO_MAP.get(g)})" for g in atrasados[:5]]
            st.write(f"👉 {', '.join(lista_atrasados)}")
        else:
            st.success("Todos os grupos saíram recentemente!")

    # --- GRÁFICO TERMÔMETRO ---
    st.divider()
    st.subheader(f"🔥 Termômetro: Bichos mais Quentes ({escolha})")
    frequencia = df_filtrado['Grupo'].value_counts().reset_index()
    frequencia.columns = ['Grupo', 'Frequência']
    frequencia['Bicho'] = frequencia['Grupo'].map(BICHO_MAP)
    
    fig = px.bar(frequencia, x='Bicho', y='Frequência', 
                 color='Frequência', color_continuous_scale='Reds',
                 title=f"Quais bichos mais saem na {escolha}")
    st.plotly_chart(fig, use_container_width=True)

    # --- SIMULADOR NA LATERAL ---
    st.sidebar.header("🎰 Simulador de Apostas")
    meu_palpite = st.sidebar.text_input("Seu Palpite (Milhar ou Grupo):")
    valor_aposta = st.sidebar.number_input("Valor da Aposta (R$):", min_value=1.0)
    
    if meu_palpite:
        ganhou = df_filtrado[df_filtrado['Milhar'].astype(str).str.contains(meu_palpite) | (df_filtrado['Grupo'] == meu_palpite)]
        if not ganhou.empty:
            st.sidebar.balloons()
            st.sidebar.success(f"✅ GANHOU NA {escolha}!")
        else:
            st.sidebar.error("❌ Não saiu nesta loteria ainda.")

else:
    st.info("Clique no botão acima para carregar as análises.")
