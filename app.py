import streamlit as st
import pandas as pd
from datetime import datetime
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
from scraper import BicoScraper

# Configuração da página
st.set_page_config(
    page_title="Monitor Jogo do Bicho",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado para mobile
st.markdown("""
    <style>
    .main {
        padding: 0.5rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    .resultado-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stat-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .palpite-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    h1, h2, h3 {
        color: #667eea;
    }
    .metric-value {
        font-size: 2em;
        font-weight: bold;
        color: #667eea;
    }
    </style>
""", unsafe_allow_html=True)

class AnalisadorBicho:
    def __init__(self, resultados):
        self.resultados = resultados
        self.bichos = {
            "01": "Avestruz", "02": "Águia", "03": "Burro", "04": "Borboleta",
            "05": "Cachorro", "06": "Cabra", "07": "Carneiro", "08": "Camelo",
            "09": "Cobra", "10": "Coelho", "11": "Cavalo", "12": "Elefante",
            "13": "Galo", "14": "Gato", "15": "Jacaré", "16": "Leão",
            "17": "Macaco", "18": "Porco", "19": "Pavão", "20": "Peru",
            "21": "Touro", "22": "Tigre", "23": "Urso", "24": "Veado", "25": "Vaca"
        }
    
    def calcular_estatisticas(self):
        """Calcula estatísticas de frequência e atraso"""
        grupos = [r['grupo'] for r in self.resultados]
        counter = Counter(grupos)
        
        estatisticas = []
        for grupo_num, bicho_nome in self.bichos.items():
            frequencia = counter.get(grupo_num, 0)
            
            # Calcular atraso (sorteios desde última aparição)
            atraso = 0
            for i, resultado in enumerate(self.resultados):
                if resultado['grupo'] == grupo_num:
                    atraso = i
                    break
            else:
                atraso = len(self.resultados)
            
            estatisticas.append({
                'Grupo': grupo_num,
                'Bicho': bicho_nome,
                'Frequência': frequencia,
                'Atraso': atraso,
                'Última Aparição': self._ultima_aparicao(grupo_num)
            })
        
        return pd.DataFrame(estatisticas).sort_values('Atraso', ascending=False)
    
    def _ultima_aparicao(self, grupo):
        """Encontra a data da última aparição do bicho"""
        for resultado in self.resultados:
            if resultado['grupo'] == grupo:
                return resultado['data']
        return "Nunca"
    
    def gerar_palpites(self, top_n=5):
        """Gera palpites baseados nos bichos mais atrasados"""
        stats = self.calcular_estatisticas()
        palpites = stats.nlargest(top_n, 'Atraso')
        return palpites[['Grupo', 'Bicho', 'Atraso']]
    
    def estatisticas_gerais(self):
        """Retorna estatísticas gerais"""
        grupos = [r['grupo'] for r in self.resultados]
        mais_frequente = Counter(grupos).most_common(1)
        
        if mais_frequente:
            grupo_freq = mais_frequente[0][0]
            return {
                'total_sorteios': len(self.resultados),
                'bicho_mais_frequente': f"{grupo_freq} - {self.bichos[grupo_freq]}",
                'frequencia_max': mais_frequente[0][1]
            }
        return {
            'total_sorteios': 0,
            'bicho_mais_frequente': 'N/A',
            'frequencia_max': 0
        }

def main():
    # Título
    st.markdown("<h1 style='text-align: center;'>🎲 Monitor Jogo do Bicho</h1>", unsafe_allow_html=True)
    
    # Botão de atualização
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Atualizar Resultados", type="primary"):
            with st.spinner("Carregando resultados..."):
                scraper = BicoScraper()
                novos_resultados = scraper.extrair_resultados()
                scraper.salvar_resultados(novos_resultados)
                st.success("✅ Resultados atualizados!")
                st.rerun()
    
    # Carregar dados
    scraper = BicoScraper()
    resultados = scraper.carregar_resultados()
    
    if not resultados:
        st.warning("Nenhum resultado disponível. Clique em 'Atualizar Resultados'")
        return
    
    # Criar analisador
    analisador = AnalisadorBicho(resultados)
    stats_gerais = analisador.estatisticas_gerais()
    
    # Métricas principais
    st.markdown("### 📊 Visão Geral")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="stat-card">
                <div style="font-size: 0.9em; color: #666;">Total de Sorteios</div>
                <div class="metric-value">{stats_gerais['total_sorteios']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="stat-card">
                <div style="font-size: 0.9em; color: #666;">Mais Frequente</div>
                <div style="font-size: 1.2em; font-weight: bold; color: #667eea;">{stats_gerais['bicho_mais_frequente']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="stat-card">
                <div style="font-size: 0.9em; color: #666;">Aparições</div>
                <div class="metric-value">{stats_gerais['frequencia_max']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Últimos Resultados
    st.markdown("### 🎯 Últimos Resultados")
    for i, resultado in enumerate(resultados[:5]):
        st.markdown(f"""
            <div class="resultado-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 1.5em; font-weight: bold;">{resultado['milhar']}</div>
                        <div style="font-size: 0.9em; opacity: 0.9;">Centena: {resultado['centena']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.2em; font-weight: bold;">{resultado['bicho']}</div>
                        <div style="font-size: 0.9em; opacity: 0.9;">Grupo {resultado['grupo']}</div>
                    </div>
                </div>
                <div style="margin-top: 0.5rem; font-size: 0.8em; opacity: 0.8;">📅 {resultado['data']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Palpites do Dia
    st.markdown("### 🎲 Palpites Baseados em Atraso")
    palpites = analisador.gerar_palpites(5)
    
    st.markdown("""
        <div class="palpite-card">
            <h4 style="margin: 0; color: white;">💡 Bichos Mais Atrasados</h4>
            <p style="margin: 0.5rem 0; opacity: 0.9; font-size: 0.9em;">
                Bichos que estão há mais tempo sem sair
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    for idx, row in palpites.iterrows():
        col1, col2, col3 = st.columns([1, 3, 2])
        with col1:
            st.markdown(f"**{row['Grupo']}**")
        with col2:
            st.markdown(f"**{row['Bicho']}**")
        with col3:
            st.markdown(f"⏰ {row['Atraso']} sorteios")
    
    # Estatísticas Completas
    st.markdown("### 📈 Estatísticas Completas")
    
    tab1, tab2, tab3 = st.tabs(["📋 Tabela", "📊 Gráficos", "🔥 Ranking"])
    
    with tab1:
        stats_df = analisador.calcular_estatisticas()
        st.dataframe(
            stats_df,
            use_container_width=True,
            hide_index=True,
            height=400
        )
    
    with tab2:
        stats_df = analisador.calcular_estatisticas()
        
        # Gráfico de Frequência
        fig_freq = px.bar(
            stats_df.sort_values('Frequência', ascending=True).tail(15),
            x='Frequência',
            y='Bicho',
            orientation='h',
            title='Top 15 Bichos Mais Frequentes',
            color='Frequência',
            color_continuous_scale='Viridis'
        )
        fig_freq.update_layout(height=500)
        st.plotly_chart(fig_freq, use_container_width=True)
        
        # Gráfico de Atraso
        fig_atraso = px.bar(
            stats_df.sort_values('Atraso', ascending=False).head(15),
            x='Bicho',
            y='Atraso',
            title='Top 15 Bichos Mais Atrasados',
            color='Atraso',
            color_continuous_scale='Reds'
        )
        fig_atraso.update_layout(height=500)
        st.plotly_chart(fig_atraso, use_container_width=True)
    
    with tab3:
        stats_df = analisador.calcular_estatisticas()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔥 Mais Frequentes")
            top_freq = stats_df.nlargest(10, 'Frequência')
            for idx, row in top_freq.iterrows():
                st.markdown(f"**{row['Grupo']} - {row['Bicho']}**: {row['Frequência']} vezes")
        
        with col2:
            st.markdown("#### ❄️ Mais Atrasados")
            top_atraso = stats_df.nlargest(10, 'Atraso')
            for idx, row in top_atraso.iterrows():
                st.markdown(f"**{row['Grupo']} - {row['Bicho']}**: {row['Atraso']} sorteios")
    
    # Rodapé
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9em; padding: 1rem;">
            <p>📱 Aplicativo otimizado para celular</p>
            <p>🔄 Atualize regularmente para ter os dados mais recentes</p>
            <p style="font-size: 0.8em; margin-top: 1rem;">
                ⚠️ Este aplicativo é apenas para fins educacionais e de entretenimento.
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
