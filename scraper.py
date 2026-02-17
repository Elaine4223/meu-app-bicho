import pandas as pd
import random
from datetime import datetime

def puxar_resultados():
    loterias = ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"]
    horarios = ["11:00", "14:00", "16:00", "18:00", "21:00"]
    lista_final = []
    
    for loteria in loterias:
        for hora in horarios:
            milhar = str(random.randint(1000, 9999))
            # Garantindo que o grupo tenha 2 dígitos (ex: 01, 05, 10)
            grupo = str(random.randint(1, 25)).zfill(2)
            
            lista_final.append({
                "Loteria": loteria,
                "Horário": hora,
                "Milhar": milhar,
                "Grupo": grupo,
                "Data": datetime.now().strftime("%d/%m/%Y")
            })
    return pd.DataFrame(lista_final)
