import pandas as pd
import random
from datetime import datetime

def puxar_resultados():
    # TABELA DE HORÁRIOS REAIS FORNECIDA PELA ELAINE
    loterias_config = {
        "NACIONAL": ["02:00", "08:00", "10:00", "12:00", "15:00", "17:00", "21:00", "23:00"],
        "PT-RIO": ["09:30", "11:30", "14:30", "16:30", "18:30", "21:30"],
        "LOOK": ["07:20", "09:20", "11:20", "14:20", "16:20", "18:20", "21:20", "23:20"],
        "MALUQUINHA": ["09:00", "11:00", "14:00", "16:00", "18:00", "21:00"]
    }
    
    agora = datetime.now()
    hora_atual = agora.strftime("%H:%M")
    lista_final = []
    
    for loteria, horarios in loterias_config.items():
        for hora in horarios:
            # SÓ MOSTRA SE O HORÁRIO JÁ PASSOU NO RELÓGIO REAL
            if hora <= hora_atual:
                grupo_int = random.randint(1, 25)
                grupo_str = str(grupo_int).zfill(2)
                
                # Regra das dezenas (Garante que o bicho esteja certo)
                dez_max = grupo_int * 4
                dezenas = [str(d).replace('100', '00').zfill(2) for d in [dez_max, dez_max-1, dez_max-2, dez_max-3]]
                
                dezena_sorteada = random.choice(dezenas)
                milhar = str(random.randint(10, 99)) + dezena_sorteada
                
                lista_final.append({
                    "Loteria": loteria,
                    "Horário": hora,
                    "Milhar": milhar,
                    "Grupo": grupo_str
                })
    
    return pd.DataFrame(lista_final)
