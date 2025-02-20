from colorama import init, Fore, Style

def print_colorama(color, message):
  print(color + f"\n{message}")
  print(Style.RESET_ALL)
  
  
  
def print_resultados(resultados):
  print("\n\nResultados capturados:\n")
  
  for resultado in resultados:
    cor = resultado['cor']
    numero = resultado['numero']
    
    # Definindo as cores conforme a variável 'cor'
    if cor == 'Vermelho':
        cor_console = Fore.RED
    elif cor == 'Preto':
        cor_console = Fore.BLACK
    elif cor == 'Branco':
        cor_console = Fore.WHITE
    else:
        cor_console = Fore.YELLOW  # Cor padrão, caso seja desconhecido

    # Imprime o número com a cor, sem pular linha
    print(f"{cor_console}[{numero}] {Style.RESET_ALL}", end=" ")
    
    
    
def aviso_entrada(cor="Preto", number={"cor": "Vermelho", "numero": 1}, aposta=2):
    return (f"⚠️ <b>Analisando uma possível entrada!</b> ⚠️\n")
    
    
def entrada_preto(number={"cor": "Vermelho", "numero": 1}):
    return (f"⏰ <b><i>SINAL CONFIRMADO!</i></b>\n\n"
            f"Apostar no ⚫ PRETO | após o {number['numero']}\n\n"+
            "<a href='https://blaze.bet.br/pt/games/double'>DOUBLE - Blaze</a>")
    
    
    
def entrada_vermelho(number={"cor": "Vermelho", "numero": 1}):
    return (f"⏰ <b><i>SINAL CONFIRMADO!</i></b>\n\n"
            f"Apostar no 🔴 VERMELHO | após o {number['numero']}\n\n"+
            "<a href='https://blaze.bet.br/pt/games/double'>DOUBLE - Blaze</a>")

    
    
def vitoria_com_gales():
    return ("----- RELATORIO -----\n"+
            "✅ Vitória com Gale!\n")
    
    
def vitoria_sem_gales(number={"cor": "Vermelho", "numero": 1}):
    return (f"✅ Vitória no {number['number']}!\n")
    
def vitoria_sem_gales():
    return ("✅ Vitória sem Gale!\n")
    