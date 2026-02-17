import streamlit as st
import pandas as pd
import plotly.express as px
import random

# Configurações de layout
st.set_page_config(page_title="Monitor Vip Pro - Gestão de Resultados", layout="wide")

# --- BANCO DE DADOS DE BICHOS E EMOJIS ---
BICHO_MAP = {
    "01": "🦩 Avestruz", "02": "🦅 Águia", "03": "🦙 Burro", "04": "🦋 Borboleta", 
    "05": "🐕 Cachorro", "06": "🐐 Cabra", "07": "🐑 Carneiro", "08": "🐪 Camelo", 
    "09": "🐍 Cobra", "10": "🐇 Coelho", "11": "🐎 Cavalo", "12": "🐘 Elefante", 
    "13": "🐓 Galo", "14": "🐈 Gato", "15": "🐊 Jacaré", "16": "🦁 Leão", 
    "17": "🐒 Macaco", "18": "🐖 Porco", "19": "🦚 Pavão", "20": "🦃 Peru", 
    "21": "🐂 Touro", "22": "🐅 Tigre", "23": "🐻 Urso", "24": "🦌 Veado", "25": "🐄 Vaca"
}

# Função para identificar o grupo automaticamente pela milhar
def identificar_grupo(milhar):
    try:
        dezena = int(str(milhar)[-2:])
        if dezena == 0: return "25"
        grupo = (dezena - 1) // 4 + 1
        return str(min(grupo, 25)).zfill(2)
    except:
        return "01"

# Inicialização do banco de dados na sessão
if 'historico_resultados' not in st.session_state:
    st.session_state.historico_resultados = []

# --- INTERFACE DE LANÇAMENTO (VISÍVEL PARA O COMPRADOR) ---
st.title("🏆 Painel Administrativo - Lançamento de Resultados")
with st.expander("➕ Clique aqui para lançar um novo resultado", expanded=True):
    with st.form("form_lancamento", clear_on_submit=True):
        c1, c2 = st.columns(2)
        loteria_input = c1.selectbox("Selecione a Loteria:", ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"])
        horario_input = c2.text_input("Horário (Ex: 11:30):")
        
        st.write("Digite os milhares do 1º ao 5º prêmio:")
        p1, p2, p3, p4, p5 = st.columns(5)
        m1 = p1.text_input("1º Prêmio")
        m2 = p2.text_input("2º Prêmio")
        m3 = p3.text_input("3º Prêmio")
        m4 = p4.text_input("4º Prêmio")
        m5 = p5.text_input("5º Prêmio")
        
        if st.form_submit_button("🚀 Publicar Resultados"):
            novos_itens = []
            for m, p in zip([m1, m2, m3, m4, m5], ["1º", "2º", "3º", "4º", "5º"]):
                if m:
                    g = identificar_grupo(m)
                    novos_itens.append({
                        "Loteria": loteria_input, 
                        "Horário": horario_input, 
                        "Prêmio": p, 
                        "Milhar": m, 
                        "Grupo": g,
                        "Bicho": BICHO_MAP[g]
                    })
            st.session_state.historico_resultados.extend(novos_itens)
            st.success("Painel atualizado com sucesso!")

st.divider()

# --- EXIBIÇÃO E ANÁLISE ---
if st.session_state.historico_resultados:
    df = pd.DataFrame(st.session_state.historico_resultados)
    
    # Filtro Lateral
    st.sidebar.header("Filtros de Visualização")
    loto_selecionada = st.sidebar.selectbox("Escolha a Loteria para Analisar:", df['Loteria'].unique())
    
    df_filtrado = df[df['Loteria'] == loto_selecionada].sort_values(by="Horário", ascending=False)
    
    st.header(f"📍 Análise do Dia: {loto_selecionada}")

    # 1. Cards do 1º Prêmio (Resumo Visual)
    df_cabeca = df_filtrado[df_filtrado['Prêmio'] == "1º"]
    if not df_cabeca.empty:
        cols = st.columns(len(df_cabeca.head(5)))
        for i, (idx, row) in enumerate(df_cabeca.head(5).iterrows()):
            with cols[i]:
                st.metric(label=f"Hora: {row['Horário']}", value=row['Milhar'], delta=row['Bicho'])

    # 2. Tabela de Resultados e Palpites
    col_tab, col_palpite = st.columns([1.5, 1])
    
    with col_tab:
        st.subheader("🕒 Histórico Completo (1-5)")
        st.dataframe(df_filtrado[['Horário', 'Prêmio', 'Milhar', 'Bicho']], use_container_width=True)

    with col_palpite:
        st.subheader("🎯 Palpites VIP para Próximo Sorteio")
        # Sugere grupos que ainda não saíram no 1º prêmio
        grupos_fora = [g for g in BICHO_MAP.keys() if g not in df_cabeca['Grupo'].tolist()]
        if grupos_fora:
            sugestao = random.choice(grupos_fora)
            st.info(f"O Bicho mais provável agora é: **{BICHO_MAP[sugestao]}**")
        
        st.markdown("---")
        st.write("💰 **Simulador de Prêmios**")
        valor_aposta = st.number_input("Valor (R$):", 1.0, 100.0, 2.0)
        st.write(f"Acerto de Milhar: R$ {valor_aposta * 4000:.2f}")
        st.write(f"Acerto de Grupo: R$ {valor_aposta * 18:.2f}")

    # 3. Termômetro (Gráfico de Frequência)
    st.divider()
    st.subheader("🔥 Termômetro: Bichos mais Frequentes (1º Prêmio)")
    freq = df_cabeca['Bicho'].value_counts().reset_index()
    if not freq.empty:
        fig = px.bar(freq, x='index', y='Bicho', labels={'index': 'Bicho', 'Bicho': 'Qtd Saídas'}, 
                     color='Bicho', text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Aguardando o primeiro lançamento de resultados para gerar as análises.")
