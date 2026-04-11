import streamlit as st
import pandas as pd
import re

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

def obter_bicho_pela_milhar(milhar):
    if not milhar or not milhar.isdigit(): return "Sorte"
    dezena = int(milhar[-2:])
    grupo = (dezena // 4) + 1
    if dezena == 0: grupo = 25
    if dezena % 4 == 0 and dezena != 0: grupo = dezena // 4
    return BICHO_MAP.get(str(grupo).zfill(2), "Sorte")

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
            # Se não tem o número do prêmio, assume a sequência da lista
            num_p = i + 1
            resultados.append({"Prêmio": num_p, "Milhar": m, "Grupo": g, "Bicho": BICHO_MAP.get(g, "Sorte")})
    return resultados

if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = []

st.title("🏆 Painel Administrativo VIP")

col_auto, col_manual = st.columns([1, 1.2])

with col_auto:
    st.markdown("### ⚡ Importação Rápida")
    loto = st.selectbox("Loteria Ativa:", ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"])
    texto_entrada = st.text_area("Cole aqui os resultados do dia:", height=150, placeholder="Pode colar vários horários, um de cada vez.")
    hora_auto = st.text_input("Horário deste sorteio:", "02:00")
    
    if st.button("✨ Processar e Organizar", use_container_width=True):
        if texto_entrada:
            novos = processar_texto_v2(texto_entrada)
            for n in novos:
                n["Loteria"], n["Horário"] = loto, hora_auto
            st.session_state.vagas_resultados.extend(novos)
            st.rerun()

with col_manual:
    st.markdown("### ✍️ Gestão de Dados")
    with st.container(border=True):
        if st.button("🗑️ Limpar Tudo (Resetar Dia)", use_container_width=True):
            st.session_state.vagas_resultados = []
            st.rerun()
        st.info("O sistema organiza automaticamente os horários e prêmios na tabela abaixo.")

st.divider()

if st.session_state.vagas_resultados:
    # Criar DataFrame e organizar
    df = pd.DataFrame(st.session_state.vagas_resultados)
    
    # Organiza por Horário e depois por Prêmio
    df = df.sort_values(by=['Horário', 'Prêmio'])
    
    # Formata a coluna prêmio para exibir com "º" novamente
    df['Prêmio'] = df['Prêmio'].astype(str) + "º"

    # --- RADAR DE ATRASOS ---
    st.subheader("🐢 Radar de Atrasos (1º Prêmio)")
    df_1 = df[df['Prêmio'] == "1º"]
    saíram = df_1['Bicho'].unique()
    atrasados = [b for b in BICHO_MAP.values() if b not in saíram]
    
    c1, c2 = st.columns(2)
    c1.success(f"**Bichos que já saíram:** {', '.join(list(saíram)[:5])}...")
    c2.error(f"**Atrasados (Sugestão):** {', '.join(atrasados[:5])}")

    st.divider()
    
    # --- HISTÓRICO ORGANIZADO ---
    st.subheader("📋 Histórico Geral Organizado")
    # Estilizando a tabela para facilitar a leitura
    st.dataframe(df[['Horário', 'Prêmio', 'Milhar', 'Bicho', 'Loteria']], use_container_width=True, hide_index=True)
else:
    st.info("💡 Aguardando dados. Cole os resultados das 02:00, 11:00, etc., para iniciar a análise.")
