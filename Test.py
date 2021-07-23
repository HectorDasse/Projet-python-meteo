import requests

r = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Bordeaux&appid=acb39e08e1429f96311f0a99078ca8d2&units=metric")

tab = r.json()
print(tab["main"]["temp"])