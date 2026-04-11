import streamlit as st
import pandas as pd
import re
import random

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Monitor Vip Pro - Elaine", layout="wide", page_icon="🏆")

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

st.title("🏆 Monitor Vip Pro - Painel de Controle")

# --- ÁREA DE ENTRADA ---
col_auto, col_info = st.columns([1.5, 1])

with col_auto:
    with st.expander("➕ Lançar Novo Resultado", expanded=True):
        l1, l2, l3 = st.columns([1,1,1])
        loto = l1.selectbox("Loteria:", ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"])
        hora_auto = l2.text_input("Horário:", "02:00")
        btn_processar = st.button("✨ Processar e Salvar", use_container_width=True)
        texto_entrada = st.text_area("Cole o resultado aqui:", height=100)
        
        if btn_processar and texto_entrada:
            novos = processar_texto_v2(texto_entrada)
            for n in novos:
                n["Loteria"], n["Horário"] = loto, hora_auto
                # Evita duplicidade exata
                if not any(d['Horário'] == n['Horário'] and d['Prêmio'] == n['Prêmio'] and d['Loteria'] == n['Loteria'] for d in st.session_state.vagas_resultados):
                    st.session_state.vagas_resultados.append(n)
            st.rerun()

with col_info:
    if st.button("🗑️ Limpar Painel (Novo Dia)", use_container_width=True):
        st.session_state.vagas_resultados = []
        st.rerun()
    
    # Palpites inteligentes baseados nos dados salvos
    if st.session_state.vagas_resultados:
        df_temp = pd.DataFrame(st.session_state.vagas_resultados)
        saíram_cabeça = df_temp[df_temp['Prêmio'] == 1]['Grupo'].unique()
        atrasados = [g for g in BICHO_MAP.keys() if g not in saíram_cabeça]
        if atrasados:
            st.success(f"🎯 **Palpite VIP:** {BICHO_MAP[atrasados[0]]}")
            st.code(f"Milhar: {gerar_milhar_do_grupo(atrasados[0])}")

st.divider()

# --- A MÁGICA DA GRADE HORIZONTAL (ESTILO FOTO) ---
if st.session_state.vagas_resultados:
    df = pd.DataFrame(st.session_state.vagas_resultados)
    
    # Filtra pela loteria selecionada para não misturar as grades
    df_loto = df[df['Loteria'] == loto]
    
    if not df_loto.empty:
        st.subheader(f"📅 Acompanhamento Diário - {loto}")
        
        # Pegamos os horários únicos e ordenamos
        horarios = sorted(df_loto['Horário'].unique())
        
        # Criamos as colunas dinamicamente (Máximo de 8 colunas como na sua foto)
        cols_grade = st.columns(len(horarios) if len(horarios) <= 8 else 8)
        
        for idx, hr in enumerate(horarios):
            if idx < 8:
                with cols_grade[idx]:
                    # Estilização do cabeçalho da coluna
                    st.markdown(f"""
                        <div style="background-color: #444; color: white; text-align: center; border-radius: 5px; padding: 5px; margin-bottom: 10px;">
                            {hr}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Filtra dados desse horário
                    dados_hr = df_loto[df_loto['Horário'] == hr].sort_values('Prêmio')
                    
                    # Mostra do 1º ao 5º
                    for p in range(1, 6):
                        linha = dados_hr[dados_hr['Prêmio'] == p]
                        if not linha.empty:
                            texto_celula = f"**{p}º** {linha.iloc[0]['Milhar']}\n\n{linha.iloc[0]['Bicho']}"
                            st.info(texto_celula)
                        else:
                            st.write(f"**{p}º** ---")
    else:
        st.info(f"Nenhum dado lançado para a loteria {loto} ainda.")

else:
    st.warning("⚠️ O painel está vazio. Use o campo acima para 'Lançar Novo Resultado'.")
