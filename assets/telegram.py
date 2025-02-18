import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Configuração do Telegram
token = os.getenv("TOKEN_TELEGRAM")
chat_id = os.getenv("CHAT_ID")

notificacoes_ativas = True  # Variável para ativar/desativar notificações do Telegram

def get_chat_id():
    """ Obtém o ID do último grupo onde o bot recebeu mensagem """
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    response = requests.get(url).json()
    
    try:
        for update in response['result']:
            chat = update['message']['chat']
            print(chat, "\n")
            if chat['type'] in ['group', 'supergroup']:  # Filtra apenas grupos
                return chat['id']
    except KeyError:
        return None
    
# Função para enviar mensagem no Telegram
def enviar_mensagem(mensagem):
    if notificacoes_ativas:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": mensagem}
        try:
            requests.post(url, data)
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
    else:
        print(f"Notificação desativada: {mensagem}")