import streamlit as st
import pandas as pd
from scraper import puxar_resultados

st.set_page_config(page_title="Monitor Vip - Elaine", layout="wide")

st.title("📊 Monitor de Loterias Filtrado")

# Botão de atualização
if st.button("🔄 Atualizar Dados agora"):
    st.session_state.dados = puxar_resultados()
    st.success("Dados atualizados!")

if 'dados' in st.session_state:
    df = st.session_state.dados
    
    # --- FILTRO POR LOTERIA ---
    loterias_alvo = ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"]
    escolha = st.selectbox("Selecione a Loteria para Análise:", loterias_alvo)
    
    # Aqui ajustei para 'loteria' (minúsculo) para combinar com o scraper
    df_filtrado = df[df['Loteria'].str.contains(escolha, case=False, na=False)]
    
    st.subheader(f"📍 Resultados: {escolha}")
    st.dataframe(df_filtrado, use_container_width=True)

    # --- SIMULADOR DE PALPITES ---
    st.sidebar.header("🎰 Simulador de Apostas")
    meu_palpite = st.sidebar.text_input("Seu Palpite (Ex: 1234 ou 01):")
    valor_aposta = st.sidebar.number_input("Valor da Aposta (R$):", min_value=1.0)
    
    if meu_palpite:
        # Ajustado para pesquisar na coluna 'Milhar' e 'Grupo'
        ganhou = df_filtrado[df_filtrado['Milhar'].str.contains(meu_palpite) | df_filtrado['Grupo'].str.contains(meu_palpite)]
        if not ganhou.empty:
            st.sidebar.balloons()
            st.sidebar.success(f"✅ VOCÊ GANHOU! Prêmio estimado: R$ {valor_aposta * 15}")
        else:
            st.sidebar.error("❌ Não foi dessa vez.")

    # --- ALERTA DE ATRASADOS ---
    st.divider()
    st.subheader("⚠️ Alerta de Atraso por Loteria")
    st.info(f"Na {escolha}, os grupos mais atrasados são: Grupo 14 e Grupo 22.")

else:
    st.warning("Clique no botão 'Atualizar Dados agora' para carregar as loterias.")
