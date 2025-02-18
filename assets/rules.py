from colorama import init, Fore, Style

from dotenv import load_dotenv
from assets.telegram import *
from assets.logger import *
from assets.configs import *

# Carrega as variáveis do .env
load_dotenv()

# Inicializa a biblioteca colorama
init()  

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
                print(f"📊 Banca atual: R${banca:.2f}")
                enviar_mensagem(f"RELATORIO:\n✅ Vitória com Gale!\n\n\n\n")
                # enviar_mensagem(f"RELATORIO:\n✅ Vitória com Gale! \n\n\n\n\n")
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
                print(f"📊 Banca atual: R${banca:.2f}")
                enviar_mensagem(f"RELATORIO:\n✅ Vitória sem Gale! \n\n\n\n\n")
                
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
                print(f"📊 Banca atual: R${banca:.2f}")
                enviar_mensagem(f"RELATORIO:\n⚪ Proteçao ativada!!\n\n\n\n")
                fazendo_gale = False
                resetar_entrada = True
                
            else:
                banca -= (aposta_inicial + protecao_inicial)
                ganho_branco = (protecao_inicial * 14)
                banca += ganho_branco
                calcular_ganho_acumulado()
                protegido += 1
                print(f"⚪ Proteçao ativada!")
                print(f"📊 Banca atual: R${banca:.2f}")
                enviar_mensagem(f"RELATORIO:\n⚪ Proteçao ativada!!\n\n\n\n")
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
                print(f"📉 Banca atual: R${banca:.2f}")
                enviar_mensagem(f"RELATORIO:\n🚫 Derrota no Gale!\n\n\n\n\n")
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
        if cores[-(sequencia_para_entrada-1):] == ['Vermelho'] * (sequencia_para_entrada-1):
            menssage= aviso_entrada("Preto", numbers[-1], aposta_inicial)
            print(menssage)
            enviar_mensagem(menssage)
            alertado = True
        elif cores[-(sequencia_para_entrada-1):] == ['Preto'] * (sequencia_para_entrada-1):
            menssage= aviso_entrada("Vermelho", numbers[-1], aposta_inicial)
            print(menssage)
            enviar_mensagem(menssage)
            alertado = True

    # Verifica se há n-1 cores iguais + 1 cor diferente (alarme falso)
    if alertado and not entrada_realizada:
        if cores[-sequencia_para_entrada:-1] == ['Vermelho'] * (sequencia_para_entrada-1) and cores[-1] != "Vermelho":
            print(aviso_falso)
            enviar_mensagem(aviso_falso + "\n\n\n\n\n")
            resetar_entrada = True
            alertado = False  # Reseta o estado do alerta para permitir novos padrões
            entrada_realizada = False  # Reseta o padrão para novas entradas

        elif cores[-sequencia_para_entrada:-1] == ['Preto'] * (sequencia_para_entrada-1) and cores[-1] != "Preto":
            print(aviso_falso)
            enviar_mensagem(aviso_falso + "\n\n\n\n\n")
            resetar_entrada = True
            alertado = False  # Reseta o estado do alerta para permitir novos padrões
            entrada_realizada = False  # Reseta o padrão para novas entradas  

    # Verifica se há n cores consecutivas para realizar entrada
    if alertado and not entrada_realizada:
        if cores[-sequencia_para_entrada:] == ['Vermelho'] * sequencia_para_entrada:
            menssage = entrada_preto(numbers[-1])
            print(menssage)
            enviar_mensagem(menssage)
            
            entrada_realizada = True
            cor_da_entrada = "Preto"  # Entrada será no Preto
            aguardando_resultado = True
        elif cores[-sequencia_para_entrada:] == ['Preto'] * sequencia_para_entrada:
            menssage = entrada_vermelho(numbers[-1])
            print(menssage)
            enviar_mensagem(menssage)
            
            entrada_realizada = True
            cor_da_entrada = "Vermelho"  # Entrada será no Vermelho
            aguardando_resultado = True
