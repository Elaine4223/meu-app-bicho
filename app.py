import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="Monitor Vip Pro - Elaine", layout="wide")

# --- BANCO DE DADOS DE BICHOS E EMOJIS OFICIAL ---
BICHO_MAP = {
    "01": "🦩 Avestruz", "02": "🦅 Águia", "03": "🦙 Burro", "04": "🦋 Borboleta", 
    "05": "🐕 Cachorro", "06": "🐐 Cabra", "07": "🐑 Carneiro", "08": "🐪 Camelo", 
    "09": "🐍 Cobra", "10": "🐇 Coelho", "11": "🐎 Cavalo", "12": "🐘 Elefante", 
    "13": "🐓 Galo", "14": "🐈 Gato", "15": "🐊 Jacaré", "16": "🦁 Leão", 
    "17": "🐒 Macaco", "18": "🐖 Porco", "19": "🦚 Pavão", "20": "🦃 Peru", 
    "21": "🐂 Touro", "22": "🐅 Tigre", "23": "🐻 Urso", "24": "🦌 Veado", "25": "🐄 Vaca"
}

def identificar_grupo(milhar):
    try:
        dezena = int(str(milhar)[-2:])
        if dezena == 0: return "25"
        grupo = (dezena - 1) // 4 + 1
        return str(min(grupo, 25)).zfill(2)
    except: return "01"

# Inicialização do banco de dados na sessão
if 'historico_vips' not in st.session_state:
    st.session_state.historico_vips = []

# --- 1. PAINEL ADMINISTRATIVO (Lançamento) ---
st.title("🏆 Painel Administrativo - Monitor Vip")
with st.expander("📝 Clique aqui para lançar novos resultados (1º ao 5º)", expanded=True):
    with st.form("form_venda", clear_on_submit=True):
        col_l, col_h = st.columns(2)
        loto_input = col_l.selectbox("Loteria:", ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"])
        hora_input = col_h.text_input("Horário (Ex: 14:30):")
        
        st.write("Insira os milhares sorteados:")
        p1, p2, p3, p4, p5 = st.columns(5)
        m1 = p1.text_input("1º Prêmio")
        m2 = p2.text_input("2º Prêmio")
        m3 = p3.text_input("3º Prêmio")
        m4 = p4.text_input("4º Prêmio")
        m5 = p5.text_input("5º Prêmio")
        
        if st.form_submit_button("🚀 Publicar e Analisar"):
            for m, p in zip([m1, m2, m3, m4, m5], ["1º", "2º", "3º", "4º", "5º"]):
                if m:
                    g = identificar_grupo(m)
                    st.session_state.historico_vips.append({
                        "Loteria": loto_input, "Horário": hora_input, "Prêmio": p, 
                        "Milhar": m, "Grupo": g, "Bicho": BICHO_MAP[g]
                    })
            st.success("Resultados integrados!")

st.divider()

# --- 2. INTERFACE DE ANÁLISE (O que o comprador verá logo abaixo) ---
if st.session_state.historico_vips:
    df = pd.DataFrame(st.session_state.historico_vips)
    
    loto_sel = st.selectbox("Selecione a Loteria para ver a Análise:", df['Loteria'].unique())
    df_filtrado = df[df['Loteria'] == loto_sel].sort_values(by="Horário", ascending=False)
    
    st.header(f"📍 Análise VIP: {loto_sel}")

    # --- CARDS DE HOJE (Interfaces anteriores) ---
    df_cabeca = df_filtrado[df_filtrado['Prêmio'] == "1º"]
    if not df_cabeca.empty:
        st.subheader("📅 Resumo dos Últimos Sorteios")
        cols = st.columns(len(df_cabeca.head(4)))
        for i, (idx, row) in enumerate(df_cabeca.head(4).iterrows()):
            with cols[i]:
                st.metric(label=f"Hora: {row['Horário']}", value=row['Milhar'], delta=row['Bicho'])

    st.divider()

    # --- TABELA E PALPITES (Interfaces anteriores) ---
    c_tab, c_palp = st.columns([1.5, 1])
    
    with c_tab:
        st.subheader("🕒 Histórico do Dia (1º ao 5º)")
        st.dataframe(df_filtrado[['Horário', 'Prêmio', 'Milhar', 'Bicho']], use_container_width=True)

    with c_palp:
        st.subheader("🎯 Palpites VIP")
        grupos_vivos = [g for g in BICHO_MAP.keys() if g not in df_cabeca['Grupo'].tolist()]
        if grupos_vivos:
            sugestao = random.choice(grupos_vivos)
            st.markdown(f"""
            <div style='background-color:#4169E1; padding:20px; border-radius:15px; color:white; text-align:center;'>
                <span style='font-size: 16px;'>PRÓXIMO GRUPO PROVÁVEL</span><br>
                <span style='font-size: 30px; font-weight: bold;'>{BICHO_MAP[sugestao]}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Sugestão de Centenas e Dezenas
            g_int = int(sugestao)
            d_base = g_int * 4
            dezenas = [str(d_base).replace('100','00').zfill(2), str(d_base-1).zfill(2)]
            st.write(f"💡 **Centenas Fortes:** {random.randint(1,9)}{dezenas[0]} | {random.randint(1,9)}{dezenas[1]}")
            st.write(f"💡 **Dezenas do Grupo:** {dezenas[0]}, {dezenas[1]}")

    # --- TERMÔMETRO E GRÁFICOS (Interfaces anteriores) ---
    st.divider()
    st.subheader("🔥 Termômetro: Frequência do 1º Prêmio")
    if not df_cabeca.empty:
        freq = df_cabeca['Bicho'].value_counts().reset_index()
        fig = px.bar(freq, x='index', y='Bicho', labels={'index':'Bicho', 'Bicho':'Qtd'}, 
                     color='Bicho', text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Aguardando o primeiro lançamento no painel acima para ativar as interfaces de análise.")
