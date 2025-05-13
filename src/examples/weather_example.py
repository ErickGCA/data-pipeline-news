import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.weather_api import WeatherAPI

def main():
    # Inicializa a API do clima
    weather_api = WeatherAPI()
    
    # Lista de cidades para consulta
    cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte']
    
    print("=== Dados do Clima ===")
    for cidade in cidades:
        dados = weather_api.get_weather_by_city(cidade)
        if dados:
            print(f"\nCidade: {dados['cidade']}")
            print(f"Data/Hora: {dados['data_hora']}")
            print(f"Temperatura: {dados['temperatura']}°C")
            print(f"Sensação Térmica: {dados['sensacao_termica']}°C")
            print(f"Umidade: {dados['umidade']}%")
            print(f"Descrição: {dados['descricao']}")
            print("-" * 30)

if __name__ == "__main__":
    main() 