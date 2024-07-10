from colorama import init, Fore, Style
import requests
import keyboard  # Importa a biblioteca keyboard para capturar a tecla ESC
import time  # Importa a função sleep da biblioteca time

init()  # Inicializa a biblioteca colorama

array = []

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

def process_data(data):
    for obj in reversed(data['records']):
        number = setWin(obj['roll'])
        game_type = obj['color']  # Renomeando para evitar conflito com palavra reservada
        
        aux = list(filter(lambda p: filtrarNumber(p, obj['id']), array))
        
        if not aux:
            array.append({"id": obj['id'], "valor": number})
            
            if game_type == 'red':
                print(Style.RESET_ALL, f"{len(array)} - {Fore.RED} [{array[-1]['valor']}] {Style.RESET_ALL}")
            elif game_type == 'black':
                print(Style.RESET_ALL, f"{len(array)} - {Fore.BLACK} [{array[-1]['valor']}] {Style.RESET_ALL}")
            elif game_type == 'white':
                print(Style.RESET_ALL, f"{len(array)} - {Fore.GREEN} [{array[-1]['valor']}] {Style.RESET_ALL}")

if __name__ == "__main__":
    url = "https://blaze.com/api/roulette_games/history?startDate=2024-07-08T18:54:13.324Z&page=1"
    
    while True:
        data = fetch_data(url)
        
        if data:
            process_data(data)
        
        if keyboard.is_pressed('esc'):  # Verifica se a tecla ESC foi pressionada
            break  # Sai do loop se ESC for pressionado
        
        time.sleep(5)  # Espera por 5 segundos antes de continuar a próxima iteração
