# pylint: disable=missing-module-docstring

import sys
import urllib.parse
import requests

BASE_URI = "https://weather.lewagon.com"

def search_city(query):
    '''Look for a given city. If multiple options are returned, have the user choose between them.
       Return one city (or None)
    '''
    # YOUR CODE HERE
    # Geocoding API -> Coordinates by location name
    url = urllib.parse.urljoin(BASE_URI, "/geo/1.0/direct")
    cities = requests.get(url, params={'q': query, 'limit': 5}).json()
    if not cities:
        print(f"Sorry, OpenWeather does not know about {query}...")
        return None
    if len(cities) == 1:
        return cities[0]
    for i, city in enumerate(cities):
        print(f"{i + 1}. {city['name']},{city['country']}")
    index = int(input("Multiple matches found, which city did you mean?\n> ")) - 1
    return cities[index]

def weather_forecast(lat, lon):
    '''Return a 5-day weather forecast for the city, given its latitude and longitude.'''
    # YOUR CODE HERE
    url = urllib.parse.urljoin(BASE_URI, "/data/2.5/forecast")
    forecasts = requests.get(url, params={'lat': lat, 'lon': lon, 'units': 'metric'}).json()['list']
    return forecasts[::8]

def main():
    '''Ask user for a city and display weather forecast'''
    query = input("City?\n> ")
    city = search_city(query)
    # YOUR CODE HERE
    if city:
        forecasts = weather_forecast(city["lat"], city["lon"])
        print(f"Here's the weather in {query}")
        for forecast in forecasts:
            max_temp = round(forecast['main']['temp_max'])
            print(f"{forecast['dt_txt'][:10]}: {forecast['weather'][0]['main']} ({max_temp}°C)")

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
