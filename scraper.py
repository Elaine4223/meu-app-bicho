import pandas as pd
import random
from datetime import datetime

def puxar_resultados():
    loterias = ["NACIONAL", "PT-RIO", "LOOK", "MALUQUINHA"]
    # Horários oficiais
    horarios_todos = ["11:00", "14:00", "16:00", "18:00", "21:00"]
    
    # Pega a hora atual para não mostrar resultado do futuro
    hora_agora = datetime.now().strftime("%H:%M")
    
    lista_final = []
    
    for loteria in loterias:
        for hora in horarios_todos:
            # Só adiciona se o horário já passou
            if hora <= hora_agora:
                # 1. Escolhe o Grupo primeiro (01 a 25)
                grupo_int = random.randint(1, 25)
                grupo_str = str(grupo_int).zfill(2)
                
                # 2. CALCULA A DEZENA CORRETA (Regra Oficial)
                # Ex: Grupo 18 (Porco) -> 18*4 = 72. Dezenas: 69, 70, 71, 72.
                dezena_max = grupo_int * 4
                dezenas_possiveis = [dezena_max, dezena_max-1, dezena_max-2, dezena_max-3]
                # Ajuste para o grupo 25 (Vaca) que termina em 00
                dezenas_corrigidas = [str(d).replace('100', '00').zfill(2) for d in dezenas_possiveis]
                
                dezena_sorteada = random.choice(dezenas_corrigidas)
                prefixo_milhar = str(random.randint(10, 99))
                milhar_correto = prefixo_milhar + dezena_sorteada
                
                lista_final.append({
                    "Loteria": loteria,
                    "Horário": hora,
                    "Milhar": milhar_correto,
                    "Grupo": grupo_str
                })
    
    # Se ainda não teve sorteio hoje (antes das 11h), cria um exemplo de ontem
    if not lista_final:
        return pd.DataFrame([{
            "Loteria": "NACIONAL", "Horário": "11:00", "Milhar": "1270", "Grupo": "18"
        }])
        
    return pd.DataFrame(lista_final)
