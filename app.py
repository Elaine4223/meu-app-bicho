import streamlit as st
import pandas as pd
import plotly.express as px
import random
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Monitor Vip Pro - Elaine", layout="wide", page_icon="🏆")

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

# --- LÓGICA DE EXTRAÇÃO ---
def processar_texto_colado(texto):
    resultados = []
    padrao = re.compile(r"(\d+)º?:\s*([\d.]+)\s*G\.?(\d+)")
    linhas = texto.split('\n')
    for linha in linhas:
        match = padrao.search(linha)
        if match:
            n_premio = match.group(1)
            milhar_suja = match.group(2).replace('.', '')
            grupo = match.group(3).zfill(2)
            resultados.append({
                "Prêmio": f"{n_premio}º", "Milhar": milhar_suja, 
                "Centena": milhar_suja[-3:], "Grupo": grupo, "Bicho": obter_bicho(grupo)
            })
    return resultados

CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = []

# --- 1. CENTRAL DE LANÇAMENTO ---
st.title("🏆 Painel Administrativo VIP")

col_auto, col_manual = st.columns([1.2, 1])

with col_auto:
    st.subheader("⚡ Importação Rápida")
    loto_selecionada = st.selectbox("Loteria:", list(CORES.keys()))
    hora_selecionada = st.text_input("Horário:", value="14:00")
    texto_entrada = st.text_area("Cole aqui o resultado completo:", height=150)
    
    if st.button("✨ Processar e Atualizar", use_container_width=True):
        if texto_entrada:
            novos_dados = processar_texto_colado(texto_entrada)
            for d in novos_dados:
                d["Loteria"] = loto_selecionada
                d["Horário"] = hora_selecionada
            st.session_state.vagas_resultados.extend(novos_dados)
            st.rerun()

with col_manual:
    if st.button("🗑️ Limpar Tudo (Novo Dia)"):
        st.session_state.vagas_resultados = []
        st.rerun()

st.divider()

# --- 2. ÁREA DE ANÁLISE (O QUE VOCÊ VENDE) ---
if st.session_state.vagas_resultados:
    df = pd.DataFrame(st.session_state.vagas_resultados)
    cor = CORES.get(loto_selecionada, "#333")

    st.markdown(f"<h1 style='color: {cor}; text-align: center;'>📊 Radar de Oportunidades: {loto_selecionada}</h1>", unsafe_allow_html=True)

    # --- NOVIDADE: CÁLCULO DE ATRASO ---
    st.subheader("🐢 Ranking de Atrasos (1º Prêmio)")
    
    # Pegamos apenas os 1ºs prêmios da loteria atual, ordenados por horário
    df_atraso = df[(df['Prêmio'] == "1º") & (df['Loteria'] == loto_selecionada)].sort_values(by="Horário")
    
    col_atr1, col_atr2 = st.columns(2)
    
    with col_atr1:
        st.write("**Bichos que MAIS saíram hoje:**")
        st.write(df[df['Loteria'] == loto_selecionada]['Bicho'].value_counts().head(5))

    with col_atr2:
        # Lógica simples de atraso: Quais grupos do 01 ao 25 NÃO estão no df_atraso?
        grupos_saíram = df_atraso['Grupo'].unique()
        atrasados = [g for g in BICHO_MAP.keys() if g not in grupos_saíram]
        st.write(f"**⚠️ {len(atrasados)} Bichos Atrasados no 1º:**")
        st.caption("Estes ainda não apareceram na cabeça hoje")
        st.write(", ".join([BICHO_MAP[g] for g in atrasados[:8]]) + "...")

    st.divider()

    # Histórico de Hoje
    st.subheader("📅 Tabela de Resultados")
    st.dataframe(df[df['Loteria'] == loto_selecionada][['Horário', 'Prêmio', 'Milhar', 'Grupo', 'Bicho']], use_container_width=True)
else:
    st.warning("Aguardando inserção de dados para iniciar análise...")