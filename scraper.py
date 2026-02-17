import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def puxar_resultados():
    url = "https://www.bichocerto.com/resultados"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # Aqui o robô vai buscar a página real
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Criamos a lista que vai separar as suas loterias favoritas
        lista_final = []
        
        # Lógica para identificar cada loteria (Nacional, PT Rio, etc)
        # O app vai organizar os dados assim para o seu filtro funcionar:
        loterias_alvo = ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"]
        
        for loteria in loterias_alvo:
            # Simulando a captura de 5 resultados para cada uma
            for i in range(1, 6):
                lista_final.append({
                    "Data": datetime.now().strftime("%d/%m/%Y"),
                    "Loteria": loteria,
                    "Premio": f"{i}º",
                    "Milhar": f"{i}123", # Exemplo: 1123, 2123...
                    "Grupo": f"0{i+5}",
                    "Bicho": "Carregando..."
                })
        
        return pd.DataFrame(lista_final)
    except:
        return pd.DataFrame()
