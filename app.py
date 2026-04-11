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

# --- LÓGICA DE EXTRAÇÃO AUTOMÁTICA (IGUAL AO ANALYTICS PEDRAS) ---
def processar_texto_colado(texto):
    """
    Extrai dados de formatos comuns como:
    '1: 3.640 G.10 COELHO' ou '1º: 3640 G10'
    """
    resultados = []
    # Regex robusta para capturar Prêmio, Milhar e Grupo
    padrao = re.compile(r"(\d+)º?:\s*([\d.]+)\s*G\.?(\d+)")
    
    linhas = texto.split('\n')
    for linha in linhas:
        match = padrao.search(linha)
        if match:
            n_premio = match.group(1)
            premio = f"{n_premio}º"
            milhar_suja = match.group(2).replace('.', '')
            grupo = match.group(3).zfill(2)
            centena = milhar_suja[-3:] if len(milhar_suja) >= 3 else ""
            
            resultados.append({
                "Prêmio": premio,
                "Milhar": milhar_suja,
                "Centena": centena,
                "Grupo": grupo,
                "Bicho": obter_bicho(grupo)
            })
    return resultados

CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

# Inicialização do estado
if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = [
        {"Loteria": "NACIONAL", "Horário": "08:00", "Prêmio": "1º", "Milhar": "1224", "Centena": "224", "Grupo": "06", "Bicho": "🐐 Cabra"}
    ]

# --- 1. CENTRAL DE LANÇAMENTO ---
st.title("🏆 Central de Lançamento VIP")

# Colunas principais para os dois tipos de entrada
col_auto, col_manual = st.columns([1.2, 1])

with col_auto:
    st.subheader("⚡ Processador Automático")
    st.info("Cole os resultados abaixo (ex: 1: 3.640 G.10)")
    loto_selecionada = st.selectbox("Loteria para este lote:", list(CORES.keys()), key="loto_auto")
    hora_selecionada = st.text_input("Horário do Sorteio:", value="10:00")
    texto_entrada = st.text_area("Área de Colagem:", height=200, placeholder="1: 3.640 G.10 COELHO\n2: 9.140 G.10 AGUIA...")
    
    if st.button("✨ Processar e Preencher", use_container_width=True):
        if texto_entrada:
            dados = processar_texto_colado(texto_entrada)
            if dados:
                for d in dados:
                    d["Loteria"] = loto_selecionada
                    d["Horário"] = hora_selecionada
                st.session_state.vagas_resultados = dados
                st.success(f"✅ {len(dados)} prêmios importados!")
                st.rerun()
            else:
                st.error("Formato não reconhecido.")

with col_manual:
    with st.expander("📥 Lançamento Manual Detalhado", expanded=False):
        with st.form("form_manual"):
            loto_atual = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
            hora = st.text_input("Horário", placeholder="Ex: 08:00")
            for p_idx in range(1, 6):
                st.write(f"**{p_idx}º Prêmio**")
                c1, c2, c3 = st.columns(3)
                m = c1.text_input(f"Milhar", key=f"m{p_idx}")
                c = c2.text_input(f"Centena", key=f"c{p_idx}")
                g = c3.text_input(f"Grupo", key=f"g{p_idx}")
            
            if st.form_submit_button("🚀 Atualizar Manualmente"):
                temp = []
                for p_idx in range(1, 6):
                    m_val = st.session_state.get(f"m{p_idx}")
                    g_val = st.session_state.get(f"g{p_idx}")
                    if m_val and g_val:
                        temp.append({
                            "Loteria": loto_atual, "Horário": hora, "Prêmio": f"{p_idx}º", 
                            "Milhar": m_val, "Centena": st.session_state.get(f"c{p_idx}"), 
                            "Grupo": g_val, "Bicho": obter_bicho(g_val)
                        })
                if temp:
                    st.session_state.vagas_resultados = temp
                    st.rerun()

st.divider()

# --- 2. INTERFACE DE ANÁLISE ---
df = pd.DataFrame(st.session_state.vagas_resultados)
loto_ativa = df['Loteria'].iloc[0] if not df.empty else "NACIONAL"
cor = CORES.get(loto_ativa, "#333")

st.markdown(f"<h1 style='color: {cor}; text-align: center;'>📍 Resultados de Hoje: {loto_ativa}</h1>", unsafe_allow_html=True)

# Cards de Destaque
df_1 = df[df['Prêmio'] == "1º"].sort_values(by="Horário", ascending=False)
if not df_1.empty:
    cols = st.columns(min(len(df_1), 4))
    for i, (idx, row) in enumerate(df_1.head(4).iterrows()):
        with cols[i]:
            st.metric(label=f"1º - {row['Horário']}", value=row['Milhar'], delta=row['Bicho'])

st.divider()

c1, c2 = st.columns([1.5, 1])
with c1:
    st.subheader("🕒 Histórico Detalhado")
    if not df.empty:
        st.table(df[['Horário', 'Prêmio', 'Milhar', 'Centena', 'Grupo', 'Bicho']].sort_values(by=["Horário", "Prêmio"]))

with c2:
    st.subheader("🎯 Palpites VIP")
    g_1_saiu = df[df['Prêmio'] == "1º"]['Grupo'].tolist()
    g_vivos = [g for g in BICHO_MAP.keys() if g not in g_1_saiu]
    
    if g_vivos:
        sug = random.choice(g_vivos)
        st.markdown(f"""
            <div style='background-color:{cor}; padding:15px; border-radius:10px; color:white; text-align:center;'>
                <b>PRÓXIMO GRUPO PROVÁVEL</b><br>
                <span style='font-size: 28px;'>{BICHO_MAP[sug]}</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 🎰 Milhares Sugeridos")
        g_int = int(sug)
        dezenas = [str(g_int*4).replace('100','00').zfill(2), str(g_int*4-1).zfill(2), str(g_int*4-2).zfill(2), str(g_int*4-3).zfill(2)]
        for i in range(3):
            m_sug = f"{random.randint(1,9)}{random.choice(dezenas).zfill(3)}"
            st.write(f"🔥 **{i+1}º Sugestão:** {m_sug} | **C:** {m_sug[-3:]}")

# Gráfico de Frequência
st.divider()
st.subheader("🔥 Termômetro Geral (Frequência)")
if not df.empty:
    freq = df['Bicho'].value_counts().reset_index()
    freq.columns = ['Bicho', 'Qtd']
    fig = px.bar(freq, x='Bicho', y='Qtd', color='Bicho', text_auto=True, 
                 color_continuous_scale=[[0, '#eee'], [1, cor]])
    st.plotly_chart(fig, use_container_width=True)
