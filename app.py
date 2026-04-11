import streamlit as st
import pandas as pd
import re
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Monitor Vip Pro - Elaine", layout="wide", page_icon="🏆")

# CSS para um visual mais profissional e cores destacadas
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { border: 1px solid #ddd; padding: 15px; border-radius: 10px; background-color: white; }
    .header-col { background-color: #1E1E1E; color: #FFD700; text-align: center; font-weight: bold; border-radius: 5px; padding: 5px; margin-bottom: 10px; }
    .resultado-box { border-bottom: 1px solid #eee; padding: 5px 0; font-size: 14px; }
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
    return f"{random.randint(10, 99)}{str(random.choice(dezenas)).zfill(2)}"

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

# --- SIDEBAR DE CONTROLE ---
with st.sidebar:
    st.title("🏆 Configurações")
    loto_selecionada = st.selectbox("Loteria Ativa:", ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"])
    hora_input = st.text_input("Horário do Sorteio:", "02:00")
    texto_area = st.text_area("Cole o resultado aqui:", height=200, placeholder="Ex: 3945 12")
    
    if st.button("🚀 Processar e Salvar", use_container_width=True):
        if texto_area:
            novos = processar_texto_v2(texto_area)
            for n in novos:
                n["Loteria"], n["Horário"] = loto_selecionada, hora_input
                if not any(d['Horário'] == n['Horário'] and d['Prêmio'] == n['Prêmio'] and d['Loteria'] == n['Loteria'] for d in st.session_state.vagas_resultados):
                    st.session_state.vagas_resultados.append(n)
            st.rerun()

    if st.button("🗑️ Limpar Painel (Novo Dia)", use_container_width=True):
        st.session_state.vagas_resultados = []
        st.rerun()

# --- PAINEL PRINCIPAL ---
st.header(f"📊 Monitor VIP Pro - {loto_selecionada}")

# 1. Seção de Palpites e Radar
st.subheader("💡 Inteligência de Palpites")
df_base = pd.DataFrame(st.session_state.vagas_resultados) if st.session_state.vagas_resultados else pd.DataFrame()

c1, c2, c3 = st.columns(3)

if not df_base.empty and loto_selecionada in df_base['Loteria'].values:
    df_loto = df_base[df_base['Loteria'] == loto_selecionada]
    saíram = df_loto[df_loto['Prêmio'] == 1]['Grupo'].unique()
    atrasados = [g for g in BICHO_MAP.keys() if g not in saíram]
    
    if atrasados:
        c1.metric("🎯 Bicho Sugerido", BICHO_MAP[atrasados[0]])
        c2.metric("🎲 Milhar VIP", gerar_milhar_do_grupo(atrasados[0]))
        c3.metric("🐢 Atrasados (Total)", len(atrasados))
else:
    c1.info("Aguardando dados...")
    c2.info("Aguardando dados...")
    c3.info("Aguardando dados...")

st.divider()

# 2. Grade de Acompanhamento Diário
st.subheader("📅 Acompanhamento por Horário")

if not df_base.empty and loto_selecionada in df_base['Loteria'].values:
    df_loto = df_base[df_base['Loteria'] == loto_selecionada]
    horarios = sorted(df_loto['Horário'].unique())
    
    # Criar colunas dinâmicas (estilo Col 1, Col 2...)
    colunas_grade = st.columns(len(horarios))
    
    for i, hr in enumerate(horarios):
        with colunas_grade[i]:
            st.markdown(f'<div class="header-col">{hr}</div>', unsafe_allow_html=True)
            dados_hr = df_loto[df_loto['Horário'] == hr].sort_values('Prêmio')
            for p in range(1, 6):
                row = dados_hr[dados_hr['Prêmio'] == p]
                if not row.empty:
                    st.markdown(f"**{p}º** `{row.iloc[0]['Milhar']}` | {row.iloc[0]['Bicho']}")
                else:
                    st.write(f"**{p}º** `----` | ...")
else:
    st.warning("Nenhum resultado processado para esta
