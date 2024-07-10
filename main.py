from colorama import init, Fore, Style
import requests
import keyboard  # Importa a biblioteca keyboard para capturar a tecla ESC
import time  # Importa a função sleep da biblioteca time
from telegram_utils import send_telegram_message
from actions import predict_next_color, update_rule_points

init()  # Inicializa a biblioteca colorama

array = []
last_rule = None  # Armazenar a última regra usada para a previsão

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        return response.json()  # Retorna os dados em formato JSON
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def setWin(value):
    if value is None or (isinstance(value, (str, list)) and len(value) == 0):
        return 0  # ou outra lógica adequada para tratamento de valor vazio
    else:
        return value

def filtrarNumber(objeto, id):
    return objeto["id"] == id

def print_game_type(game_type, value, length):
    if game_type == 'red':
        print(Style.RESET_ALL, f"{length} - {Fore.RED} [{value}] {Style.RESET_ALL}")
    elif game_type == 'black':
        print(Style.RESET_ALL, f"{length} - {Fore.BLACK} [{value}] {Style.RESET_ALL}")
    elif game_type == 'white':
        print(Style.RESET_ALL, f"{length} - {Fore.GREEN} [{value}] {Style.RESET_ALL}")

def process_data(data):
    global last_rule
    
    for obj in reversed(data['records']):
        number = setWin(obj['roll'])
        game_type = obj['color']
        
        aux = list(filter(lambda p: filtrarNumber(p, obj['id']), array))
        
        if not aux:
            array.append({"id": obj['id'], "valor": number, "color": game_type})
            print_game_type(game_type, array[-1]['valor'], len(array))
            
            if len(array) > 99:
                # Verifica se há uma previsão anterior a ser validada
                if last_rule:
                    if last_rule[0].lower() == game_type:
                        update_rule_points(last_rule[1], 1)  # Incrementa pontos se a previsão anterior estava correta
                    else:
                        update_rule_points(last_rule[1], -1)  # Diminui pontos se a previsão anterior estava incorreta
                
                # Faz uma nova previsão
                prediction, rule_title = predict_next_color(array)
                send_telegram_message(prediction)
                
                # Armazena a regra usada para a próxima validação
                last_rule = (prediction, rule_title)


def main_loop(url):
    while True:
        data = fetch_data(url)
        
        if data:
            process_data(data)
        
        if keyboard.is_pressed('esc'):  # Verifica se a tecla ESC foi pressionada
            break  # Sai do loop se ESC for pressionado
        
        time.sleep(5)  # Espera por 5 segundos antes de continuar a próxima iteração

if __name__ == "__main__":
    url = "https://blaze.com/api/roulette_games/history?startDate=2024-07-08T18:54:13.324Z&page=1"
    main_loop(url)
