# Capturar resultados da roleta com base na cor
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from colorama import init, Fore

from assets.telegram import *
from assets.logger import *
from assets.utils import *
from assets.configs import *
from assets.rules import verificar_padroes

# Inicializa a biblioteca colorama
init()  

# nav = startChromeProd()
nav = startChromeDev()

# Acessar a página do jogo
def acessar_pagina():
    nav.get('https://blaze.bet.br/pt/games/double')
    try:
        WebDriverWait(nav, 10).until(
            EC.presence_of_element_located((By.ID, 'roulette-recent'))
        )
        print()
        print_colorama(Fore.BLUE, "Página acessada com sucesso e conteúdo carregado.")
        print_colorama(Fore.GREEN, msg_ativo)
        
        # enviar_mensagem(msg_ativo)
    except Exception as e:
        print(f"Erro ao carregar a página: {e}")


def capturar_resultados():
    try:
        # Localiza o contêiner principal baseado no novo HTML
        container = nav.find_element(By.CLASS_NAME, 'entries.main')

        # Localiza os elementos das cores
        elementos = container.find_elements(By.CLASS_NAME, 'sm-box')
        
        resultados = []
        resultados_print = []
        
        for e in elementos[:10]:  # Captura os últimos 10 resultados
            classe = e.get_attribute('class')
            try:
                numero = e.find_element(By.CLASS_NAME, 'number').text  # Obtém o número dentro da div "number"
            except:
                numero = '0'  # Caso não encontre o número, assume 0 (pode ser ajustado conforme o comportamento esperado)

            
            if 'red' in classe:
                cor = 'Vermelho'
            elif 'black' in classe:
                cor = 'Preto'
            elif 'white' in classe:
                cor = 'Branco'
            else:
                cor = 'Desconhecido'
            
            # Adiciona um dicionário com a cor e o número
            resultados.append(cor)
            resultados_print.append({'cor': cor, 'numero': numero})

        resultados.reverse()  # Inverte para que a ordem seja da direita para a esquerda
        resultados_print.reverse()
        print_resultados(resultados_print)
        print("\n")
        
        return resultados, resultados_print
    except Exception as e:
        print(f"Erro ao capturar resultados: {e}")
        return []


# Início do programa
try:
    acessar_pagina()
    while True:
        print("Iniciando nova iteração do loop...")
        resultados, numbers = capturar_resultados()
        if resultados and resultados != ultima_lista:
            os.system('cls' if os.name=='nt' else 'clear')
            ultima_lista = resultados
            verificar_padroes(resultados, numbers)
        # else:
            # print_colorama(Fore.BLUE,"Nenhuma alteração na lista capturada.")
        time.sleep(5)
except Exception as e:
    print_colorama(Fore.RED, f"❌ [Erro] {e}")
finally:
    print_colorama(Fore.RED, msg_encerrado)
    
    # enviar_mensagem(msg_encerrado)
    nav.quit()