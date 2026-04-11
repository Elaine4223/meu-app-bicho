import streamlit as st
import pandas as pd
import re
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Monitor Vip Pro - Elaine", layout="wide", page_icon="🏆")

# CSS para layout profissional
st.markdown("""
    <style>
    .stMetric { border: 1px solid #ddd; padding: 15px; border-radius: 10px; background-color: white; }
    .header-col { background-color: #1E1E1E; color: #FFD700; text-align: center; font-weight: bold; border-radius: 5px; padding: 5px; margin-bottom: 10px; }
    .atrasados-box { background-color: #ffebee; padding: 10px; border-radius: 10px; border: 1px solid #ffcdd2; color: #b71c1c; font-weight: bold; }
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

# --- SIDEBAR ---
with st.sidebar:
    st.header("🏆 Entradas")
    loto_selecionada = st.selectbox("Loteria:", ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"])
    hora_input = st.text_input("Horário (Ex: 11:00):", "02:00")
    texto_area = st.text_area("Cole os resultados aqui:", height=180)
    
    if st.button("🚀 Salvar Resultado", use_container_width=True):
        if texto_area:
            novos = processar_texto_v2(texto_area)
            for n in novos:
                n["Loteria"], n["Horário"] = loto_selecionada, hora_input
                if not any(d['Horário'] == n['Horário'] and d['Prêmio'] == n['Prêmio'] and d['Loteria'] == n['Loteria'] for d in st.session_state.vagas_resultados):
                    st.session_state.vagas_resultados.append(n)
            st.rerun()

    if st.button("🗑️ Limpar Tudo", use_container_width=True):
        st.session_state.vagas_resultados = []
        st.rerun()

# --- ÁREA PRINCIPAL ---
st.title(f"📊 Monitor VIP - {loto_selecionada}")

# Palpites e Atrasos
st.subheader("💡 Análise e Palpites")
df_base = pd.DataFrame(st.session_state.vagas_resultados) if st.session_state.vagas_resultados else pd.DataFrame()

if not df_base.empty and loto_selecionada in df_base['Loteria'].values:
    df_loto = df_base[df_base['Loteria'] == loto_selecionada]
    saíram = df_loto[df_loto['Prêmio'] == 1]['Grupo'].unique()
    atrasados_cod = [g for g in BICHO_MAP.keys() if g not in saíram]
    atrasados_nomes = [BICHO_MAP[g] for g in atrasados_cod]
    
    c1, c2, c3 = st.columns(3)
    if atrasados_cod:
        c1.metric("🎯 Bicho Sugerido", BICHO_MAP[atrasados_cod[0]])
        c2.metric("🎲 Milhar VIP", gerar_milhar_do_grupo(atrasados_cod[0]))
        c3.metric("🐢 Total Atrasados", len(atrasados_nomes))
        
        # --- NOVA SEÇÃO VISÍVEL DE ATRASADOS ---
        st.markdown(f"""
            <div class="atrasados-box">
                🐢 Bichos que ainda não saíram no 1º Prêmio: <br>
                <span style="font-size: 14px; font-weight: normal;">{', '.join(atrasados_nomes)}</span>
            </div>
        """, unsafe_allow_html=True)
else:
    c1, c2, c3 = st.columns(3)
    c1.info("Aguardando dados...")
    c2.info("Aguardando dados...")
    c3.info("Aguardando dados...")

st.divider()

# Grade de Horários
st.subheader("📅 Tabela de Acompanhamento")
if not df_base.empty and loto_selecionada in df_base['Loteria'].values:
    df_loto = df_base[df_base['Loteria'] == loto_selecionada]
    horarios = sorted(df_loto['Horário'].unique())
    colunas_grade = st.columns(len(horarios) if len(horarios) > 0 else 1)
    
    for i, hr in enumerate(horarios):
        with colunas_grade[i]:
            st.markdown(f'<div class="header-col">{hr}</div>', unsafe_allow_html=True)
            dados_hr = df_loto[df_loto['Horário'] == hr].sort_values('Prêmio')
            for p in range(1, 6):
                row = dados_hr[dados_hr['Prêmio'] == p]
                if not row.empty:
                    st.write(f"**{p}º** `{row.iloc[0]['Milhar']}` | {row.iloc[0]['Bicho']}")
                else:
                    st.write(f"**{p}º** `----` | ...")
else:
    st.warning("Nenhum dado processado para esta loteria. Comece colando um resultado na barra lateral!")
