import streamlit as st
import pandas as pd
import re
import random

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Monitor Vip Pro - Elaine", layout="wide", page_icon="🏆")

# CSS para deixar as caixinhas menores e mais elegantes
st.markdown("""
    <style>
    .stAlert { padding: 5px; margin-bottom: 2px; }
    .css-1r6slb0 { padding: 5px; }
    div[data-testid="stMetricValue"] { font-size: 1.2rem; }
    </style>
""", unsafe_allow_html=True)

BICHO_MAP = {
    "01": "Avestruz", "02": "Águia", "03": "Burro", "04": "Borboleta", 
    "05": "Cachorro", "06": "Cabra", "07": "Carneiro", "08": "Camelo", 
    "09": "Cobra", "10": "Coelho", "11": "Cavalo", "12": "Elefante", 
    "13": "Galo", "14": "Gato", "15": "Jacaré", "16": "Leão", 
    "17": "Macaco", "18": "Porco", "19": "Pavão", "20": "Peru", 
    "21": "Touro", "22": "Tigre", "23": "Urso", "24": "Veado", "25": "Vaca"
}

def gerar_milhar_do_grupo(grupo):
    dezenas = [int(grupo)*4, int(grupo)*4-1, int(grupo)*4-2, int(grupo)*4-3]
    if grupo == "25": dezenas = [0, 99, 98, 97]
    prefixo = random.randint(10, 99)
    dezena = random.choice(dezenas)
    return f"{prefixo}{str(dezena).zfill(2)}"

def processar_texto_v2(texto):
    resultados = []
    linhas = [l.strip() for l in texto.split('\n') if l.strip()]
    for i, linha in enumerate(linhas):
        match_simples = re.search(r"(\d{3,4})\s+(\d{1,2})", linha)
        match_completo = re.search(r"(\d+)º?:\s*([\d.]+)\s*G\.?(\d+)", linha)
        if match_completo:
            p, m, g = match_completo.group(1), match_completo.group(2).replace('.',''), match_completo.group(3).zfill(2)
            resultados.append({"Prêmio": int(p), "Milhar": m, "Grupo": g, "Bicho": BICHO_MAP.get(g, "Sorte")})
        elif match_simples:
            m, g = match_simples.group(1), match_simples.group(2).zfill(2)
            resultados.append({"Prêmio": i + 1, "Milhar": m, "Grupo": g, "Bicho": BICHO_MAP.get(g, "Sorte")})
    return resultados

if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = []

st.title("🏆 Monitor Vip Pro")

# --- ÁREA DE ENTRADA ---
with st.sidebar:
    st.header("⚙️ Controle")
    loto = st.selectbox("Loteria:", ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"])
    hora_auto = st.text_input("Horário do Sorteio:", "02:00")
    texto_entrada = st.text_area("Cole os resultados aqui:", height=150)
    if st.button("🚀 Processar e Salvar", use_container_width=True):
        if texto_entrada:
            novos = processar_texto_v2(texto_entrada)
            for n in novos:
                n["Loteria"], n["Horário"] = loto, hora_auto
                if not any(d['Horário'] == n['Horário'] and d['Prêmio'] == n['Prêmio'] and d['Loteria'] == n['Loteria'] for d in st.session_state.vagas_resultados):
                    st.session_state.vagas_resultados.append(n)
            st.rerun()
    
    if st.button("🗑️ Resetar Dia", use_container_width=True):
        st.session_state.vagas_resultados = []
        st.rerun()

# --- PALPITES E RADAR (Destaque no topo) ---
if st.session_state.vagas_resultados:
    df_temp = pd.DataFrame(st.session_state.vagas_resultados)
    saíram_cabeça = df_temp[df_temp['Prêmio'] == 1]['Grupo'].unique()
    atrasados = [g for g in BICHO_MAP.keys() if g not in saíram_cabeça]
    
    c1, c2 = st.columns(2)
    if atrasados:
        c1.metric("Bicho VIP do Momento", BICHO_MAP[atrasados[0]])
        c2.metric("Milhar Sugerida", gerar_milhar_do_grupo(atrasados[0]))

st.divider()

# --- GRADE HORIZONTAL CLEAN ---
if st.session_state.vagas_resultados:
    df = pd.DataFrame(st.session_state.vagas_resultados)
    df_loto = df[df['Loteria'] == loto]
    
    if not df_loto.empty:
        horarios = sorted(df_loto['Horário'].unique())
        # Cria colunas de acordo com o número de horários (máx 8)
        cols_grade = st.columns(len(hor
