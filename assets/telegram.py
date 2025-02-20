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
        data = {
            "chat_id": chat_id, 
            "text": mensagem, 
            "parse_mode": "HTML",
            "disable_web_page_preview": True  # Remove a prévia do link
        }
        response = requests.post(url, data)
        
        if response.status_code == 200:
            message_id = response.json().get("result", {}).get("message_id")
            return message_id
        else:
            print(f"Erro ao enviar mensagem: {response.json()}")
            return None
    else:
        print(f"Notificação desativada: {mensagem}")



# Função para enviar imagem no Telegram
def enviar_imagem(caminho_imagem):
    """ Envia uma imagem para o Telegram """
    if notificacoes_ativas:
        url = f"https://api.telegram.org/bot{token}/sendPhoto"
        try:
            with open(caminho_imagem, "rb") as imagem:
                files = {"photo": imagem}
                data = {"chat_id": chat_id}
                response = requests.post(url, data=data, files=files)
                if response.status_code == 200:
                    print("Imagem enviada com sucesso!")
                    # print_colorama(Fore.CYAN, "Imagem enviada com sucesso!")
                else:
                    print(f"Erro ao enviar imagem: {response.json()}")
                    # print_colorama(Fore.RED, f"Erro ao enviar imagem: {response.json()}")
        except Exception as e:
            print(f"Erro ao enviar imagem")
            # print_colorama(Fore.RED, f"Erro ao enviar imagem")
    else:
        print(f"Notificação desativada: Imagem {caminho_imagem} não enviada.")


def apagar_mensagem(message_id):
    """ Apaga uma mensagem já enviada no Telegram """
    url = f"https://api.telegram.org/bot{token}/deleteMessage"
    data = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    response = requests.post(url, data=data)

    if response.status_code == 200:
        print(f"Mensagem {message_id} apagada com sucesso!")
    else:
        print(f"Erro ao apagar mensagem: {response.json()}")