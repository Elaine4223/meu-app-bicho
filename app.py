import streamlit as st
import pandas as pd
import re
import random

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Monitor Vip Pro - Elaine", layout="wide", page_icon="🏆")

BICHO_MAP = {
    "01": "🦩 Avestruz", "02": "🦅 Águia", "03": "🦙 Burro", "04": "🦋 Borboleta", 
    "05": "🐕 Cachorro", "06": "🐐 Cabra", "07": "🐑 Carneiro", "08": "🐪 Camelo", 
    "09": "🐍 Cobra", "10": "🐇 Coelho", "11": "🐎 Cavalo", "12": "🐘 Elefante", 
    "13": "🐓 Galo", "14": "🐈 Gato", "15": "🐊 Jacaré", "16": "🦁 Leão", 
    "17": "🐒 Macaco", "18": "🐖 Porco", "19": "🦚 Pavão", "20": "🦃 Peru", 
    "21": "🐂 Touro", "22": "🐅 Tigre", "23": "🐻 Urso", "24": "🦌 Veado", "25": "🐄 Vaca"
}

def gerar_milhar_do_grupo(grupo):
    # Gera uma milhar aleatória terminando em uma das dezenas do grupo
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

col_auto, col_manual = st.columns([1, 1.2])

with col_auto:
    st.markdown("### ⚡ Importação Rápida")
    loto = st.selectbox("Loteria Ativa:", ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"])
    texto_entrada = st.text_area("Cole os resultados aqui:", height=150)
    hora_auto = st.text_input("Horário:", "02:00")
    
    if st.button("✨ Processar e Analisar", use_container_width=True):
        if texto_entrada:
            novos = processar_texto_v2(texto_entrada)
            for n in novos:
                n["Loteria"], n["Horário"] = loto, hora_auto
                # SÓ ADICIONA SE NÃO FOR DUPLICADO (mesma loteria, hora, prêmio e milhar)
                if n not in st.session_state.vagas_resultados:
                    st.session_state.vagas_resultados.append(n)
            st.rerun()

with col_manual:
    st.markdown("### ✍️ Gestão")
    if st.button("🗑️ Limpar Tudo (Resetar Dia)", use_container_width=True):
        st.session_state.vagas_resultados = []
        st.rerun()
    
    # --- NOVIDADE: SEÇÃO DE PALPITES ---
    st.markdown("---")
    st.markdown("### 💡 Palpites Sugeridos")
    if st.session_state.vagas_resultados:
        df_temp = pd.DataFrame(st.session_state.vagas_resultados)
        saíram = df_temp[df_temp['Prêmio'] == 1]['Grupo'].unique()
        atrasados_g = [g for g in BICHO_MAP.keys() if g not in saíram]
        
        if atrasados_g:
            p_grupo = atrasados_g[0] # Sugere o que está mais atrasado
            st.success(f"**Bicho Forte:** {BICHO_MAP[p_grupo]}")
            st.code(f"Milhar Sugerida: {gerar_milhar_do_grupo(p_grupo)}")
        else:
            st.write("Aguardando mais dados para calcular palpite...")
    else:
        st.caption("Insira dados para gerar palpites.")

st.divider()

if st.session_state.vagas_resultados:
    df = pd.DataFrame(st.session_state.vagas_resultados)
    df = df.drop_duplicates(subset=['Horário', 'Prêmio', 'Milhar', 'Loteria']) # REMOVE DUPLICADAS
    df = df.sort_values(by=['Horário', 'Prêmio'])
    
    st.subheader("📋 Histórico Geral de Hoje")
    st.dataframe(df[['Horário', 'Prêmio', 'Milhar', 'Bicho', 'Loteria']], use_container_width=True, hide_index=True)
