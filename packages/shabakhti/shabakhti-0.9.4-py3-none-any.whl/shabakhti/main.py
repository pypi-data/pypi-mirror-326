import requests
import pyttsx3

def voce(aqi, city, temperature, humidity):
    engine = pyttsx3.init()
    engine.setProperty('rate', 100)
    engine.setProperty('volume', 1.0)
    engine.say(
        f"The AQI in {city} is {aqi} quality {air_pollution_level(aqi)}. The temperature is {temperature} degrees Celsius and the humidity is {humidity} percent.")
    print(
        f"The AQI in {city} is {aqi} quality {air_pollution_level(aqi)}. The temperature is {temperature} degrees Celsius and the humidity is {humidity} percent.")
    engine.runAndWait()

def air_pollution_level(aqi):
    aqi = int(aqi)
    if 0 <= aqi <= 50:
        return 'Good(خوب)'
    elif 51 <= aqi <= 100:
        return 'Moderate(در حد متوسط)'
    elif 101 <= aqi <= 150:
        return 'Unhealthy for Sensitive Groups(ناسالم برای گروه های حساس)'
    elif 151 <= aqi <= 200:
        return 'Unhealthy(ناسالم)'
    elif 201 <= aqi <= 300:
        return 'Very Unhealthy(خیلی ناسالم)'
    else:
        return 'Hazardous(خطرناک)'

def cities():
    cities = {
        '1': 'tehran',
        '2': 'varamin',
        '3': 'mashhad',
        '4': 'esfahan',
        '5': 'shiraz',
    }
    number = input(f'{cities}\n enter a number or city : ')
    if number in cities:
        city = cities[number]
        return api(city)
    else:
        city = number
        return api(city)

def api(city):
    site = f"http://api.waqi.info/feed/{city}/?token=a77ec062d00fbba59f2107ba7e85848113d7447e"
    response = requests.get(site).json()
    city = response['data']['city']['name']
    aqi = response['data']['aqi']
    temperature = response['data']['iaqi']['t']['v']
    humidity = response['data']['iaqi']['h']['v']
    return call(aqi, city, temperature, humidity)

def call(aqi, city, temperature, humidity):
    aqi = str(aqi)
    city = str(city)
    temperature = str(temperature)
    humidity = str(humidity)
    print('|\naqi(درصدالودگی) : ', aqi)
    print('_______________________________________')
    print('city(شهر) : ', city)
    print('_______________________________________')
    print(f'temperature(دما) : {temperature}c')
    print('_______________________________________')
    print(f'humidity(رطویت) :  {humidity}%')
    print('_______________________________________')
    print(f'Air Pollution Level(کیقیت) : {air_pollution_level(aqi)}\n')
    return voce(aqi, city, temperature, humidity)

if __name__ == '__main__':
    cities()
