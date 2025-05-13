from dotenv import load_dotenv
load_dotenv()
import os
import requests
from typing import Dict, Optional
from datetime import datetime

class WeatherAPI:
    def __init__(self):
        self.api_key = os.getenv('OPEN_WEATHER_API_KEY')
        print(f"[LOG] OPEN_WEATHER_API_KEY carregada: {'SIM' if self.api_key else 'NÃO'}", self.api_key)
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
    def get_weather_by_city(self, city: str) -> Optional[Dict]:
        """
        Obtém dados do clima para uma cidade específica.
        
        Args:
            city (str): Nome da cidade
            
        Returns:
            Optional[Dict]: Dados do clima ou None em caso de erro
        """
        try:
            print(f"[LOG] Buscando clima para cidade: {city}")
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'pt_br'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return {
                'cidade': data['name'],
                'temperatura': data['main']['temp'],
                'sensacao_termica': data['main']['feels_like'],
                'umidade': data['main']['humidity'],
                'descricao': data['weather'][0]['description'],
                'data_hora': datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter dados do clima: {str(e)}")
            return None 