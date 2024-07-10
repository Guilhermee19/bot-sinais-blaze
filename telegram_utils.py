import requests
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def send_telegram_message(TYPE):
    # Agora você pode acessar suas variáveis de ambiente
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')

    if(TYPE == '-'): 
        return
    
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    message = setMessage(TYPE)
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'  # Optional: Define the text formatting mode
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message: {response.status_code} - {response.text}")

def setMessage(TYPE):
    messages = {
        'WHITE': "🤖BotBlaze\n\nAPOSTAR NO BRANCO ⚪ !",
        'RED': "🤖BotBlaze\n\nAPOSTAR NO RED 🔴 !",
        'BLACK': "🤖BotBlaze\n\nAPOSTAR NO BLACK ⚫ !"
    }
    return messages.get(TYPE, "🤖BotBlaze\n\n⚠️ Tipo desconhecido.")