import streamlit as st
import pandas as pd  # CORRIGIDO: Agora o sistema reconhece a biblioteca
import plotly.express as px
import random

st.set_page_config(page_title="Monitor Vip Pro - Elaine", layout="wide")

# --- DICIONÁRIO OFICIAL ---
BICHO_MAP = {
    "01": "🦩 Avestruz", "02": "🦅 Águia", "03": "🦙 Burro", "04": "🦋 Borboleta", 
    "05": "🐕 Cachorro", "06": "🐐 Cabra", "07": "🐑 Carneiro", "08": "🐪 Camelo", 
    "09": "🐍 Cobra", "10": "🐇 Coelho", "11": "🐎 Cavalo", "12": "🐘 Elefante", 
    "13": "🐓 Galo", "14": "🐈 Gato", "15": "🐊 Jacaré", "16": "🦁 Leão", 
    "17": "🐒 Macaco", "18": "🐖 Porco", "19": "🦚 Pavão", "20": "🦃 Peru", 
    "21": "🐂 Touro", "22": "🐅 Tigre", "23": "🐻 Urso", "24": "🦌 Veado", "25": "🐄 Vaca"
}

# Funções de Cálculo Automático
def calcular_centena_grupo(m):
    if not m or len(str(m)) < 2: return "", ""
    c = str(m)[-3:] if len(str(m)) >= 3 else ""
    try:
        dezena = int(str(m)[-2:])
        g = "25" if dezena == 0 else str(min((dezena - 1) // 4 + 1, 25)).zfill(2)
    except: g = ""
    return c, g

CORES = {"NACIONAL": "#2E8B57", "PT-RIO": "#4169E1", "LOOK": "#FF8C00", "MALUQUINHA": "#C71585"}

if 'vagas_resultados' not in st.session_state:
    st.session_state.vagas_resultados = []

# --- 1. CENTRAL DE LANÇAMENTO (ESTRUTURA VERTICAL + AUTO) ---
st.title("🏆 Central de Lançamento Profissional PRO")
with st.expander("📥 Lançar Resultados (1º ao 5º Prêmio)", expanded=True):
    loto_atual = st.selectbox("Selecione a Loteria:", list(CORES.keys()))
    
    for h_idx in range(1, 9):
        st.markdown(f"### ⏰ Horário {h_idx}")
        col_h, _ = st.columns([1, 4])
        hora = col_h.text_input(f"Horário {h_idx}", key=f"h_{h_idx}", placeholder="Ex: 10:00")
        
        # Cabeçalho da Grade
        c_head = st.columns([0.5, 1, 1, 1])
        c_head[1].write("**Milhar**")
        c_head[2].write("**Centena**")
        c_head[3].write("**Grupo**")
        
        for p_idx in range(1, 6):
            cp, cm, cc, cg = st.columns([0.5, 1, 1, 1])
            cp.write(f"**{p_idx}º**")
            
            # Campo de Milhar (Onde você digita)
            m_input = cm.text_input(f"M", key=f"m_{h_idx}_{p_idx}", label_visibility="collapsed")
            
            # Mágica do Auto-Preenchimento
            c_auto, g_auto = calcular_centena_grupo(m_input)
            
            # Centena e Grupo aparecem preenchidos conforme a Milhar
            cc.text_input(f"C", value=c_auto, key=f"c_{h_idx}_{p_idx}", label_visibility="collapsed")
            cg.text_input(f"G", value=g_auto, key=f"g_{h_idx}_{p_idx}", label_visibility="collapsed")
        st.markdown("---")
            
    if st.button("🚀 Gravar e Sincronizar Tudo"):
        temp = []
        for h_idx in range(1, 9):
            h_val = st.session_state.get(f"h_{h_idx}")
            if h_val:
                for p_idx in range(1, 6):
                    milhar = st.session_state.get(f"m_{h_idx}_{p_idx}")
                    if milhar:
                        # Re-calcula para garantir precisão na gravação
                        c_val, g_val = calcular_centena_grupo(milhar)
                        temp.append({
                            "Loteria": loto_atual, "Horário": h_val, "Prêmio": f"{p_idx}º",
                            "Milhar": milhar, "Centena": c_val, "Grupo": g_val, 
                            "Bicho": BICHO_MAP.get(g_val, "Sorte")
                        })
        if temp:
            st.session_state.vagas_resultados = temp
            st.success("Tudo calculado e salvo com sucesso!")
            st.rerun()

st.divider()

# --- 2. INTERFACE DE ANÁLISE ---
if st.session_state.vagas_resultados:
    df = pd.DataFrame(st.session_state.vagas_resultados)
    loto_ativa = df['Loteria'].iloc[0]
    cor = CORES.get(loto_ativa, "#333")
    
    st.markdown(f"<h1 style='color: {cor}; text-align: center;'>📍 Monitor: {loto_ativa}</h1>", unsafe_allow_html=True)
    
    # Cards de Destaque
    df_1 = df[df['Prêmio'] == "1º"].sort_values(by="Horário", ascending=False)
    if not df_1.empty:
        cols_cards = st.columns(min(len(df_1), 4))
        for i, (idx, row) in enumerate(df_1.head(4).iterrows()):
            with cols_cards[i]:
                st.metric(label=f"⏰ {row['Horário']}", value=row['Milhar'], delta=row['Bicho'])

    st.divider()

    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.subheader("🕒 Histórico (1º ao 5º)")
        st.dataframe(df[['Horário', 'Prêmio', 'Milhar', 'Centena', 'Grupo', 'Bicho']].sort_values(by=["Horário", "Prêmio"]), use_container_width=True)

    with c2:
        st.subheader("🎯 Palpites VIP")
        g_1_saiu = df[df['Prêmio'] == "1º"]['Grupo'].tolist()
        g_vivos = [g for g in BICHO_MAP.keys() if g not in g_1_saiu]
        if g_vivos:
            sug = random.choice(g_vivos)
            st.markdown(f"<div style='background-color:{cor}; padding:20px; border-radius:10px; color:white; text-align:center;'><b>GRUPO PROVÁVEL</b><br><span style='font-size: 24px;'>{BICHO_MAP[sug]}</span></div>", unsafe_allow_html=True)
            
            st.markdown("#### 🎰 5 Palpites de Milhar")
            for i in range(5):
                # Gera milhar/centena baseada no grupo sugerido
                dezena_base = str(int(sug)*4).zfill(2)
                m_sug = f"{random.randint(1,9)}{random.randint(0,9)}{dezena_base}"
                st.write(f"🔥 **{m_sug}** | C: **{m_sug[-3:]}**")

    st.divider()
    st.subheader("🔥 Termômetro de Frequência (Análise 1º ao 5º)")
    freq = df['Bicho'].value_counts().reset_index()
    freq.columns = ['Bicho', 'Qtd']
    fig = px.bar(freq, x='Bicho', y='Qtd', color='Bicho', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
