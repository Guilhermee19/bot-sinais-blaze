from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from colorama import init, Fore, Style

from dotenv import load_dotenv
from assets.telegram import enviar_mensagem
from assets.logger import *

# Carrega as variáveis do .env
load_dotenv()

# Inicializa a biblioteca colorama
init()  

# Configurações do navegador
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--headless")  # Ativa o modo headless

# Inicializar navegador
nav = webdriver.Chrome(options=chrome_options)

# Mensagens de status
msg_ativo = "✅ Bot Ativo"
aviso_falso = "🚫 Alarme falso: Aguardando novo padrão."
sinal_vermelho = "⚫⚫ Atenção: Entrar no Preto ⚫⚫"
sinal_preto = "🔴🔴 Atenção entrar no Vermelho 🔴🔴"
sinal_gale = "📢 GALE - Duplicar aposta repetindo a entrada."
proteger_branco_10 = "⚪ Lembrar de proteger patrimônio com 10% no Branco.⚪"
msg_encerrado = "❌ Bot Encerrado"

# Variáveis configuráveis pelo usuário
banca = 42.02  # Banca inicial em reais
banca_inicial = 42.02  # Armazena o valor inicial da banca para cálculo de vitórias e derrotas
aposta_inicial = 2
protecao_inicial = aposta_inicial * 0.10
aposta_gale = 2 * aposta_inicial
protecao_gale = protecao_inicial * 2  # Valor da aposta inicial
sequencia_para_entrada = 5 # Configuração inicial: N cores iguais para entrada

# Controle de Resultados
vitorias = 5
perdas = 0
protegido = 0

# Variáveis globais para controle
historico_cores = []
fazendo_gale = True
ultima_lista = []  # Armazena a última lista capturada
alertado = False
entrada_realizada = False  # Controla se a entrada foi realizada
aguardando_resultado = False  # Variável para aguardar o próximo giro após entrada
resetar_entrada = False  # Variável para resetar padrão após conclusão de Gale
cor_da_entrada = None  # Armazena a cor da entrada para verificar vitória
contador_atualizado = False  # Garante que vitória ou derrota seja contabilizada apenas uma vez
em_pausa = False
vitorias_consecutivas = 0

# Capturar resultados da roleta com base na cor
from selenium.webdriver.common.by import By

# Acessar a página do jogo
def acessar_pagina():
    nav.get('https://blaze.bet.br/pt/games/double')
    try:
        WebDriverWait(nav, 10).until(
            EC.presence_of_element_located((By.ID, 'roulette-recent'))
        )
        print()
        print_colorama(Fore.BLUE, "Página acessada com sucesso e conteúdo carregado.")
        enviar_mensagem(msg_ativo)
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

# Verificar padrões e enviar sinais
def verificar_padroes(cores, numbers):
    global fazendo_gale, alertado, entrada_realizada, aguardando_resultado, banca, aposta, vitorias, perdas, protegido, resetar_entrada, cor_da_entrada, banca_inicial, contador_atualizado, ganho_acumulado, vitorias_consecutivas, em_pausa

    if em_pausa:
        # Aguardar o padrão de N + 2 cores iguais
        if cores[-(sequencia_para_entrada + 2):] == [cores[-1]] * (sequencia_para_entrada + 2):
            print(f"Padrão de pausa detectado: {cores[-(sequencia_para_entrada + 2):]}")
            enviar_mensagem(f"Padrão de pausa detectado: {cores[-(sequencia_para_entrada + 2):]}")
            em_pausa = False
            vitorias_consecutivas = 0  # Reseta o contador de vitórias consecutivas
        return

    # Reset do estado somente após vitória, derrota ou alarme falso
    if resetar_entrada:
        print("♻️ Resetando padrão após conclusão do ciclo anterior.")
        print(f"Antes do reset: alertado={alertado}, entrada_realizada={entrada_realizada}, aguardando_resultado={aguardando_resultado}, cor_da_entrada={cor_da_entrada}")
        resetar_entrada = False
        entrada_realizada = False
        alertado = False
        aguardando_resultado = False
        cor_da_entrada = None
        contador_atualizado = False
        aposta = aposta_inicial
        print(f"Após o reset: alertado={alertado}, entrada_realizada={entrada_realizada}, aguardando_resultado={aguardando_resultado}, cor_da_entrada={cor_da_entrada}")
        return

    def calcular_ganho_acumulado():
        global ganho_acumulado, banca_inicial, banca
        ganho_acumulado = banca - banca_inicial

    # Aguardar o próximo resultado após entrada
    if aguardando_resultado:
        if cores[-1] == cor_da_entrada:  # Vitória
            vitorias_consecutivas += 1
            if fazendo_gale:  # Vitória com Gale
                # Cálculo para vitória no Gale
                banca -= (aposta_gale + protecao_gale)
                ganho_bruto = aposta_gale * 2
                # Atualiza a banca e exibe os resultados
                banca += ganho_bruto
                calcular_ganho_acumulado()
                vitorias += 1
                print_colorama(Fore.GREEN ,f"✅ Vitória sem Gale!")
                print(f"📊 Banca atual: R${banca:.2f}, Ganho acumulado: R${ganho_acumulado:.2f}")
                enviar_mensagem(f"RELATORIO:\n✅ Vitória com Gale!\n\n\n\n")
                # enviar_mensagem(f"RELATORIO:\n✅ Vitória com Gale!\n📊 Banca atual: R${banca:.2f}\n🏆 Vitórias: {vitorias}\n💰 Ganho acumulado: R${ganho_acumulado:.2f}\n\n\n\n\n")
                resetar_entrada = True
                fazendo_gale = False

            else:  # Vitória sem Gale
                banca -= (aposta_inicial + protecao_inicial)

                # Cálculo para vitória sem Gale
                ganho_bruto = (aposta_inicial * 2)  # Ganho bruto

                # Atualiza a banca e exibe os resultados
                banca += ganho_bruto
                calcular_ganho_acumulado()
                vitorias += 1
                print_colorama(Fore.GREEN ,f"✅ Vitória sem Gale!")
                print(f"📊 Banca atual: R${banca:.2f}, Ganho acumulado: R${ganho_acumulado:.2f}")
                enviar_mensagem(f"RELATORIO:\n✅ Vitória sem Gale!\n📊 Banca atual: R${banca:.2f}\n🏆 Vitórias: {vitorias}\n💰 Ganho acumulado: R${ganho_acumulado:.2f}\n\n\n\n\n")
                
            if vitorias_consecutivas >= 4:
                print_colorama(Fore.CYAN ,"⏸️ Pausando após 4 vitórias consecutivas.")
                enviar_mensagem("⏸️ Pausando após 4 vitórias consecutivas, aguardando novo padrao.")
                em_pausa = True    
            resetar_entrada = True
            return
        
        elif cores[-1] == "Branco":  # Branco
            if fazendo_gale:
                banca -= (aposta_gale + protecao_gale)
                ganho_branco = protecao_gale * 14 # Branco paga 14 vezes a proteção
                # Atualiza a banca e exibe os resultados
                banca += ganho_branco
                calcular_ganho_acumulado()
                protegido += 1
                print(f"⚪ Proteçao ativada!")
                print(f"📊 Banca atual: R${banca:.2f}, Ganho acumulado: R${ganho_acumulado:.2f}")
                enviar_mensagem(f"RELATORIO:\n⚪ Proteçao ativada!!\n📊 Banca atual: R${banca:.2f}\n🏆 Vitórias: {vitorias}\n💰 Ganho acumulado: R${ganho_acumulado:.2f}\n⚪ Protegidos: {protegido}\n\n\n\n")
                fazendo_gale = False
                resetar_entrada = True
                
            else:
                banca -= (aposta_inicial + protecao_inicial)
                ganho_branco = (protecao_inicial * 14)
                banca += ganho_branco
                calcular_ganho_acumulado()
                protegido += 1
                print(f"⚪ Proteçao ativada!")
                print(f"📊 Banca atual: R${banca:.2f}, Ganho acumulado: R${ganho_acumulado:.2f}")
                enviar_mensagem(f"RELATORIO:\n⚪ Proteçao ativada!!\n📊 Banca atual: R${banca:.2f}\n🏆 Vitórias: {vitorias}\n💰 Ganho acumulado: R${ganho_acumulado:.2f}\n⚪ Protegidos: {protegido}\n\n\n\n")
                resetar_entrada = True
                return  # Interrompe o fluxo após vitória no Branco

        elif cores[-1] != cor_da_entrada:  # Derrota
            if fazendo_gale:  # Derrota no Gale
                vitorias_consecutivas = 0
                # Cálculo das perdas no Gale
                banca -= (aposta_gale + protecao_gale)
                calcular_ganho_acumulado()
                perdas += 1
                print_colorama(Fore.RED ,f"🚫 Derrota no Gale!")
                print(f"📉 Banca atual: R${banca:.2f}, Ganho acumulado: R${ganho_acumulado:.2f}")
                enviar_mensagem(f"RELATORIO:\n🚫 Derrota no Gale!\n📉 Banca atual: R${banca:.2f}\n💰 Ganho acumulado: R${ganho_acumulado:.2f}\n\n\n\n\n")
                resetar_entrada = True
                fazendo_gale = False

            else:  # Derrota inicial, inicia Gale
                banca -= (aposta_inicial + protecao_inicial)
                print_colorama(Fore.RED ,f"🚫 Derrota inicial. Iniciando Gale.")
                print(sinal_gale)
                enviar_mensagem(sinal_gale)
                fazendo_gale = True  # Ativa o Gale
                return  # Interrompe o fluxo após derrota


    # Verifica se há n-1 cores consecutivas e envia alerta apenas uma vez
    if not alertado and not entrada_realizada:
        if cores[-(sequencia_para_entrada-1):] == ["Vermelho"] * (sequencia_para_entrada-1):
            menssage= aviso_entrada("Preto", numbers[-1], aposta_inicial)
            print(menssage)
            enviar_mensagem(menssage)
            alertado = True
        elif cores[-(sequencia_para_entrada-1):] == ["Preto"] * (sequencia_para_entrada-1):
            menssage= aviso_entrada("Vermelho", numbers[-1], aposta_inicial)
            print(menssage)
            enviar_mensagem(menssage)
            alertado = True

    # Verifica se há n-1 cores iguais + 1 cor diferente (alarme falso)
    if alertado and not entrada_realizada:
        if cores[-sequencia_para_entrada:-1] == ["Vermelho"] * (sequencia_para_entrada-1) and cores[-1] != "Vermelho":
            print(aviso_falso)
            enviar_mensagem(aviso_falso + "\n\n\n\n\n")
            resetar_entrada = True
            alertado = False  # Reseta o estado do alerta para permitir novos padrões
            entrada_realizada = False  # Reseta o padrão para novas entradas

        elif cores[-sequencia_para_entrada:-1] == ["Preto"] * (sequencia_para_entrada-1) and cores[-1] != "Preto":
            print(aviso_falso)
            enviar_mensagem(aviso_falso + "\n\n\n\n\n")
            resetar_entrada = True
            alertado = False  # Reseta o estado do alerta para permitir novos padrões
            entrada_realizada = False  # Reseta o padrão para novas entradas  

    # Verifica se há n cores consecutivas para realizar entrada
    if alertado and not entrada_realizada:
        if cores[-sequencia_para_entrada:] == ["Vermelho"] * sequencia_para_entrada:
            print(sinal_vermelho)
            enviar_mensagem(sinal_vermelho)
            entrada_realizada = True
            cor_da_entrada = "Preto"  # Entrada será no Preto
            aguardando_resultado = True
        elif cores[-sequencia_para_entrada:] == ["Preto"] * sequencia_para_entrada:
            print(sinal_preto)
            enviar_mensagem(sinal_preto)
            entrada_realizada = True
            cor_da_entrada = "Vermelho"  # Entrada será no Vermelho
            aguardando_resultado = True

# Início do programa
try:
    acessar_pagina()
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        print("Iniciando nova iteração do loop...")
        resultados, numbers = capturar_resultados()
        if resultados and resultados != ultima_lista:
            ultima_lista = resultados
            verificar_padroes(resultados, numbers)
        else:
            print_colorama(Fore.BLUE,"Nenhuma alteração na lista capturada.")
        time.sleep(5)
except Exception as e:
    print(f"❌ Erro: {e}")
finally:
    print(msg_encerrado)
    enviar_mensagem(msg_encerrado)
    nav.quit()