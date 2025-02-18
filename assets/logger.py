from colorama import init, Fore, Style
from assets.telegram import enviar_mensagem

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
    icon = "⚫"
    if cor == "Vermelho":
        icon = "🔴"
        
    return (f"⚠️ Atenção para possível entrada\n"
            f"{icon} | {cor.capitalize()}\n")
    
    
def entrada_preto(number={"cor": "Vermelho", "numero": 1}):
    return (f"⚫⚫ Atenção: Entrar no Preto ⚫⚫\n"
            f"Entrar apos {number["numero"]}\n"
            "⚪ | Proteger no Branco \n"
            "📢 | Fazer até 2 GALES \n")
    
def entrada_vermelho(number={"cor": "Vermelho", "numero": 1}):
    return (f"🔴🔴 Atenção entrar no Vermelho 🔴🔴\n"
            f"Entrar apos {number["numero"]}\n"
            "⚪ | Proteger no Branco \n"
            "📢 | Fazer até 2 GALES \n")