# 🎲 Monitor Jogo do Bicho

Aplicativo web completo para monitorar resultados do jogo do bicho com estatísticas e palpites inteligentes.

## 🚀 Funcionalidades

- ✅ Extração automática de resultados (Milhar, Centena e Grupo)
- 📊 Estatísticas detalhadas (frequência e atraso de cada bicho)
- 🎯 Sistema de palpites baseado em análise de atrasos
- 📱 Interface responsiva otimizada para celular
- 📈 Gráficos interativos com Plotly
- 🔄 Atualização em tempo real dos dados

## 📦 Estrutura do Projeto

```
app_bicho/
├── app.py                  # Interface Streamlit
├── scraper.py              # Extração de dados
├── requirements.txt        # Dependências
├── .gitignore             # Arquivos ignorados pelo Git
└── README.md              # Este arquivo
```

## 🛠️ Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/app_bicho.git
cd app_bicho
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o aplicativo:
```bash
streamlit run app.py
```

## ☁️ Deploy no Streamlit Cloud

1. Faça upload do projeto no GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte sua conta do GitHub
4. Selecione o repositório `app_bicho`
5. Defina o arquivo principal como `app.py`
6. Clique em "Deploy"

## 📱 Como Usar

1. **Atualizar Resultados**: Clique no botão "🔄 Atualizar Resultados" para buscar os dados mais recentes
2. **Ver Últimos Resultados**: Visualize os 5 sorteios mais recentes com destaque
3. **Palpites**: Veja os bichos mais atrasados (maior chance estatística)
4. **Estatísticas**: Explore tabelas e gráficos detalhados sobre frequências e atrasos
5. **Rankings**: Compare bichos mais frequentes vs. mais atrasados

## 🎯 Sistema de Palpites

O sistema analisa:
- **Atraso**: Quantos sorteios se passaram desde a última aparição
- **Frequência Histórica**: Quantas vezes cada bicho apareceu
- **Padrões Estatísticos**: Bichos com maior atraso tendem a aparecer em breve

## 📊 Estatísticas Disponíveis

- Total de sorteios analisados
- Bicho mais frequente
- Ranking de frequências
- Ranking de atrasos
- Gráficos de barras interativos
- Tabela completa com todas as métricas

## 🔧 Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit**: Interface web
- **BeautifulSoup**: Web scraping
- **Pandas**: Análise de dados
- **Plotly**: Visualizações interativas
- **Requests**: Requisições HTTP

## ⚠️ Avisos Importantes

- Este aplicativo é apenas para fins educacionais e de entretenimento
- Os dados são extraídos de fontes públicas
- Não incentivamos jogos de azar
- Use com responsabilidade

## 📝 Licença

Este projeto é livre para uso pessoal e educacional.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

## 📞 Contato

Para dúvidas ou sugestões, abra uma issue no GitHub.

---

Desenvolvido com ❤️ usando Streamlit
