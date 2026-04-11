import streamlit as st
import pandas as pd
import re
import random

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Monitor Vip Pro - Elaine", layout="wide", page_icon="🏆")

# CSS para layout ultra clean
st.markdown("""
    <style>
    .reportview-container .main .block-container { padding-top: 1rem; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
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

# --- BARRA LATERAL (CONFIGURAÇÃO) ---
with st.sidebar:
    st.header("⚙️ Entradas")
    loto_selecionada = st.selectbox("Escolha a Loteria:", ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"])
    hora_input = st.text_input("Horário (Ex: 11:00):", "02:00")
    texto_input = st.text_area("Cole os resultados aqui:", height=150)
    
    if st.button("🚀 Salvar no Painel", use_container_width=True):
        if texto_input:
            novos = processar_texto_v2(texto_input)
            for n in novos:
                n["Loteria"], n["Horário"] = loto_selecionada, hora_input
                # Trava contra duplicidade
                if not any(d['Horário'] == n['Horário'] and d['Prêmio'] == n['Prêmio'] and d['Loteria'] == n['Loteria'] for d in st.session_state.vagas_resultados):
                    st.session_state.vagas_resultados.append(n)
            st.rerun()

    if st.button("🗑️ Limpar Tudo", use_container_width=True):
        st.session_state.vagas_resultados = []
        st.rerun()

# --- ÁREA PRINCIPAL (PALPITES) ---
if st.session_state.vagas_resultados:
    df_base = pd.DataFrame(st.session_state.vagas_resultados)
    df_loto = df_base[df_base['Loteria'] == loto_selecionada]
    
    # Palpite baseado nos atrasos da loteria selecionada
    saíram = df_loto[df_loto['Prêmio'] == 1]['Grupo'].unique()
    atrasados = [g for g in BICHO_MAP.keys() if g not in saíram]
    
    c1, c2 = st.columns(2)
    if atrasados:
        c1.metric("🎯 Bicho Sugerido", BICHO_MAP[atrasados[0]])
        c2.metric("🎲 Milhar VIP", gerar_milhar_do_grupo(atrasados[0]))

    st.divider()

    # --- GRADE HORIZONTAL CLEAN ---
    if not df_loto.empty:
        horarios_disponiveis = sorted(df_loto['Horário'].unique())
        # Corrigido: Agora o parêntese fecha certinho!
        colunas_horario = st.columns(len(horarios_disponiveis))
        
        for i, hr in enumerate(horarios_disponiveis):
            with colunas_horario[i]:
                st.markdown(f"""<div style="background-color:#262730; color:white; text-align:center; border-radius:5px; padding:2px; font-weight:bold; margin-bottom:10px;">{hr}</div>""", unsafe_allow_html=True)
                
                dados_do_horario = df_loto[df_loto['Horário'] == hr].sort_values('Prêmio')
                for p in range(1, 6):
                    row = dados_do_horario[dados_do_horario['Prêmio'] == p]
                    if not row.empty:
                        # Estilo Milhar + Bicho Lado a Lado
                        st.write(f"**{p}º** `{row.iloc[0]['Milhar']}` | {row.iloc[0]['Bicho']}")
                    else:
                        st.write(f"**{p}º** `----` | ...")
    else:
        st.info(f"Nenhum dado salvo para {loto_selecionada} hoje.")
else:
    st.warning("👈 Comece colando um resultado na barra lateral!")
