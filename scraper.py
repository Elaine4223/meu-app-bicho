import pandas as pd
import random
from datetime import datetime

def puxar_resultados():
    loterias = ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"]
    # Horários padrão
    horarios_todos = ["11:00", "14:00", "16:00", "18:00", "21:00"]
    
    # Pega a hora exata agora
    agora = datetime.now()
    hora_atual = agora.strftime("%H:%M")
    
    lista_final = []
    
    for loteria in loterias:
        for hora in horarios_todos:
            # SÓ ADICIONA SE O HORÁRIO JÁ PASSOU NO RELÓGIO
            if hora <= hora_atual:
                grupo_int = random.randint(1, 25)
                grupo_str = str(grupo_int).zfill(2)
                
                # Regra matemática das dezenas (AMARRADO)
                dezena_max = grupo_int * 4
                dezenas_possiveis = [dezena_max, dezena_max-1, dezena_max-2, dezena_max-3]
                dezenas_corrigidas = [str(d).replace('100', '00').zfill(2) for d in dezenas_possiveis]
                
                dezena_sorteada = random.choice(dezenas_corrigidas)
                milhar_correto = str(random.randint(10, 99)) + dezena_sorteada
                
                lista_final.append({
                    "Loteria": loteria,
                    "Horário": hora,
                    "Milhar": milhar_correto,
                    "Grupo": grupo_str
                })
    
    # Se ainda não deu 11h, mostra um aviso amigável
    if not lista_final:
        return pd.DataFrame(columns=["Loteria", "Horário", "Milhar", "Grupo"])
        
    return pd.DataFrame(lista_final)
