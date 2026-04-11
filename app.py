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

def obter_bicho_pela_milhar(milhar):
    if not milhar or not milhar.isdigit(): return "Sorte"
    dezena = int(milhar[-2:])
    # Lógica do bicho: a cada 4 dezenas muda o grupo
    grupo = (dezena // 4) + 1
    if dezena == 0: grupo = 25 # Vaca é 00
    if dezena % 4 == 0 and dezena != 0: grupo = dezena // 4
    return BICHO_MAP.get(str(grupo).zfill(2), "Sorte")

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
                "Centena": milhar_suja[-3:], "Grupo": grupo, "Bicho": BICHO_MAP.get(grupo, "Sorte")
            })
    return resultados

if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = []

# --- 1. INTERFACE DE LANÇAMENTO ---
st.title("🏆 Painel Administrativo VIP")

col_auto, col_manual = st.columns([1, 1.2])

with col_auto:
    st.markdown("### ⚡ Importação Rápida")
    loto_selecionada = st.selectbox("Loteria Ativa:", ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"])
    texto_entrada = st.text_area("Cole o resultado bruto aqui:", height=150, placeholder="Ex: 1: 3.640 G.10")
    hora_auto = st.text_input("Horário da colagem:", "14:00")
    
    if st.button("✨ Processar Texto", use_container_width=True):
        if texto_entrada:
            novos = processar_texto_colado(texto_entrada)
            for n in novos:
                n["Loteria"] = loto_selecionada
                n["Horário"] = hora_auto
            st.session_state.vagas_resultados.extend(novos)
            st.rerun()

with col_manual:
    st.markdown("### ✍️ Lançamento Manual (Grade)")
    with st.container(border=True):
        c_hora, c_limpar = st.columns([2, 1])
        hora_manual = c_hora.text_input("Horário do Sorteio:", "10:00", key="h_man")
        if c_limpar.button("🗑️ Limpar Tudo", use_container_width=True):
            st.session_state.vagas_resultados = []
            st.rerun()

        # Cabeçalho da Grade
        g1, g2, g3 = st.columns([1, 2, 2])
        g1.caption("Prêmio")
        g2.caption("Milhar")
        g3.caption("Bicho Detectado")

        # Linhas de entrada (1º ao 5º)
        entradas_manuais = []
        for i in range(1, 6):
            r1, r2, r3 = st.columns([1, 2, 2])
            r1.write(f"**{i}º**")
            milhar_input = r2.text_input(f"milhar_{i}", label_visibility="collapsed", placeholder="Ex: 1224")
            bicho_detectado = obter_bicho_pela_milhar(milhar_input)
            r3.code(bicho_detectado)
            if milhar_input:
                entradas_manuais.append({
                    "Loteria": loto_selecionada, "Horário": hora_manual, 
                    "Prêmio": f"{i}º", "Milhar": milhar_input, 
                    "Centena": milhar_input[-3:], "Grupo": "", "Bicho": bicho_detectado
                })

        if st.button("📥 Salvar Lançamento Manual", use_container_width=True):
            if entradas_manuais:
                st.session_state.vagas_resultados.extend(entradas_manuais)
                st.rerun()

st.divider()

# --- 2. ÁREA DE ANÁLISE ---
if st.session_state.vagas_resultados:
    df = pd.DataFrame(st.session_state.vagas_resultados)
    
    st.subheader("🐢 Radar de Atrasos (1º Prêmio)")
    # Filtra apenas o que saiu no 1º prêmio para ver o atraso
    df_1 = df[df['Prêmio'] == "1º"]
    saíram = df_1['Bicho'].unique()
    atrasados = [b for b in BICHO_MAP.values() if b not in saíram]
    
    col1, col2 = st.columns(2)
    col1.metric("Bichos na Cabeça hoje", len(saíram))
    col2.metric("Bichos Atrasados", len(atrasados))
    
    st.write("**Sugestão de Atraso:** " + ", ".join(atrasados[:5]))
    
    st.divider()
    st.subheader("📋 Histórico Geral")
    st.dataframe(df, use_container_width=True)
else:
    st.info("💡 Dica: Use o lado esquerdo para colar resultados do WhatsApp ou o lado direito para digitar manualmente.")
    st.warning("Aguardando inserção de dados para iniciar análise...")
