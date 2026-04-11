import streamlit as st
import pandas as pd
import re
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Monitor VIP Pro - Elaine", layout="wide", page_icon="🏆")

# CSS para layout profissional e colunas mais limpas
st.markdown("""
    <style>
    .stMetric { border: 1px solid #ddd; padding: 15px; border-radius: 10px; background-color: white; }
    .header-col { background-color: #1E1E1E; color: #FFD700; text-align: center; font-weight: bold; border-radius: 5px; padding: 5px; margin-bottom: 10px; }
    .resultado-linha { border-bottom: 1px solid #eee; padding: 3px 0; font-size: 14px; white-space: nowrap; }
    .pala-sugerido { background-color: #f0f2f6; border-radius: 5px; padding: 5px; margin-bottom: 5px; }
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

# --- PAINEL PRINCIPAL (TUDO NA TELA) ---
st.title("🏆 Monitor VIP Pro")

# 1. Seção de Entrada de Dados (Agora no topo)
with st.expander("📥 Inserir Novo Resultado do Dia", expanded=True):
    col_loto, col_hora = st.columns([2, 1])
    with col_loto:
        loto_selecionada = st.selectbox("Loteria Ativa:", ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"])
    with col_hora:
        hora_input = st.text_input("Horário do Sorteio:", "07:20")
    
    texto_area = st.text_area("Cole os resultados aqui (Copie e Cole completo):", height=120)
    
    c1, c2, c3 = st.columns(3)
    if c1.button("🚀 Processar e Salvar", use_container_width=True):
        if texto_area:
            novos = processar_texto_v2(texto_area)
            for n in novos:
                n["Loteria"], n["Horário"] = loto_selecionada, hora_input
                if not any(d['Horário'] == n['Horário'] and d['Prêmio'] == n['Prêmio'] and d['Loteria'] == n['Loteria'] for d in st.session_state.vagas_resultados):
                    st.session_state.vagas_resultados.append(n)
            st.rerun()
    if c2.button("🗑️ Limpar Painel", use_container_width=True):
        st.session_state.vagas_resultados = []
        st.rerun()
    if c3.button("🚪 Sair"):
        st.session_state.autenticado = False
        st.rerun()

st.divider()

# 2. Seção de Palpites VIP (Turbinada)
st.subheader(f"💡 Inteligência VIP - {loto_selecionada}")
df_base = pd.DataFrame(st.session_state.vagas_resultados) if st.session_state.vagas_resultados else pd.DataFrame()

c_pala, c_atras = st.columns([2, 1])

with c_pala:
    st.markdown("**🎯 Top 4 Palpites VIP**")
    
    if not df_base.empty and loto_selecionada in df_base['Loteria'].values:
        df_loto = df_base[df_base['Loteria'] == loto_selecionada]
        saíram = df_loto[df_loto['Prêmio'] == 1]['Grupo'].unique()
        atrasados = sorted([g for g in BICHO_MAP.keys() if g not in saíram])
        
        # Mostra até 4 palpites baseados no atraso
        num_palpites = 4
        if atrasados:
            pal_cols = st.columns(min(len(atrasados), num_palpites))
            for idx, g_atrasado in enumerate(atrasados[:num_palpites]):
                with pal_cols[idx]:
                    st.markdown(f"""
                        <div class="pala-sugerido">
                            <b>Palpite {idx+1}</b><br>
                            Bicho: {BICHO_MAP[g_atrasado]}<br>
                            <span style="font-size: 1.2rem; font-family: monospace;">Milhar: {gerar_milhar_do_grupo(g_atrasado)}</span>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Todos os bichos já saíram no 1º prêmio!")
    else:
        st.info("Aguardando dados para analisar...")

with c_atras:
    st.markdown("**🐢 Radar de Atrasos**")
    if not df_base.empty and loto_selecionada in df_base['Loteria'].values:
        st.metric("Bichos que faltam (1º)", len(atrasados))
    else:
        st.metric("Bichos que faltam (1º)", 25)

st.divider()

# 3. Grade de Horários (Estilo Coluna Original)
st.subheader("📅 Tabela de Acompanhamento (Lado a Lado)")

if not df_base.empty and loto_selecionada in df_base['Loteria'].values:
    df_loto = df_base[df_base['Loteria'] == loto_selecionada]
    horarios = sorted(df_loto['Horário'].unique())
    
    # Criar colunas dinâmicas (Máximo de 10 colunas para não esticar demais)
    num_horarios = len(horarios)
    colunas_grade = st.columns(num_horarios if num_horarios <= 10 else 10)
    
    for i, hr in enumerate(horarios):
        if i < 10:
            with colunas_grade[i]:
                st.markdown(f'<div class="header-col">{hr}</div>', unsafe_allow_html=True)
                dados_hr = df_loto[df_loto['Horário'] == hr].sort_values('Prêmio')
                
                # Mostra do 1º ao 5º prêmio
                for p in range(1, 6):
                    row = dados_hr[dados_hr['Prêmio'] == p]
                    if not row.empty:
                        # Estilo Milhar | Bicho
                        st.markdown(f'<div class="resultado-linha">**{p}º** — `{row.iloc[0]["Milhar"]}` | {row.iloc[0]["Bicho"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="resultado-linha">**{p}º** — `----` | ...</div>', unsafe_allow_html=True)
        else:
            st.warning("Máximo de 10 horários exibidos. Limpe o painel para um novo dia.")
            break
else:
    st.info("Painel vazio. Use a seção no topo para inserir o primeiro resultado.")