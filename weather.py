from helpers import take, drop, first, rest
import requests
import json

def http_get(url):
    '''Encapsulate the requests library and parsing
    so it doesn't get strewn about the code below
    '''
    response = requests.get(url)
    return json.loads(response.text)

def farenheit_to_kelvin(T):
    '''https://www.rapidtables.com/convert/temperature/fahrenheit-to-kelvin.html'''
    return (int(T) + 459.67) * 5/9


def convert_zip_to_lat_long(zip_code):
    '''Takes a zipcode, and returns only the lat longs from a public api'''
    api_key                = 'UR8RH5qWgfSbCp5Q2PLXaEFhwf8CGZFPcKePSjoVlrst1BydtKymbW2HiYCo5ZiW'
    zipcode_to_latlong_url = 'https://www.zipcodeapi.com/rest/{}/info.json/{}/degrees'.format(api_key,zip_code)
    results                = http_get(zipcode_to_latlong_url)
    return [v for k,v in results.items() if k in ['lat','lng']]


def get_weather_by_zip(zip_code):
    '''Take a zipcode and return description and temperature in kelvin
    Get the lat long response.
    Get the end-point response for the hourly forecast from the first response.
    Get the first hourly forecast (i.e. now)
    Get the required information, and convert Temp to Kelvin
    '''
    latitude, longitude          = convert_zip_to_lat_long(zip_code)
    national_weather_service_url = 'https://api.weather.gov/points/{},{}'.format(latitude, longitude)
    nws_response                 = http_get(national_weather_service_url)
    forecastHourly_url           = nws_response.get('properties').get('forecastHourly')
    hourly_response              = http_get(forecastHourly_url)
    current_forecast             = first(hourly_response.get('properties').get('periods'))
    temperature, description     = [v for k,v in current_forecast.items() if k in ['temperature', 'shortForecast']]
    return '{} {} degrees Kelvin'.format(description, farenheit_to_kelvin(temperature))

if __name__ == '__main__':
    print(get_weather_by_zip(80111))
