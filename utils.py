from google.generativeai.types import HarmCategory, HarmBlockThreshold
import requests
from datetime import datetime
safety_config = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT : HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    }

sample = "You need to provide different responses based on user input: If the user asks about your information or who are you, output Introduction(event=event). If the user expresses a desire to eat something), output FindRestaurant(event,query= {user's text}, keyword = {the thing of interest in the user's text},radius = {desired distance}). If the user inquires about the weather, output FindWeather(event=event,query={user's query}). If the user want to change the location, output AskForUserLocation(event).If the user's speech is not within the above range, just have a normal conversation. For example: I am hungry, what is for dinner?"
history=[{'role':'user',
                'parts':[sample]},
        {'role':'model',
        'parts':["FindRestaurant(event,query= \"I am hungry, what is for dinner?\")"]},
        {'role':'user',
                'parts':["Tell me something about you"]},
        {'role':'model',
        'parts':["Introduction(event=event)"]},
        {'role':'user',
                'parts':["how about some ramen nearby?"]},
        {'role':'model',
        'parts':["FindRestaurant(event=event, query = \"how about some ramen nearby?\"), keyword = \"ramen\",radius=1000)"]},
        {'role':'user',
                'parts':["Will today be hot?"]},
        {'role':'model',
        'parts':["FindWeather(event=event,query = \"Will today be hot?\")"]},
                ]

def RequestWeather(weather_parameters):
    response = requests.get(url="https://api.openweathermap.org/data/2.5/weather?", params=weather_parameters)
    response.raise_for_status()
    cur_data = response.json()
    response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast?", params=weather_parameters)
    response.raise_for_status()
    weather_data = response.json()
    forcast = []
    now = datetime.now()
    for data in weather_data['list']:
        dt = datetime.fromtimestamp(data['dt']) 
        if dt < now:
            continue
        if len(forcast) > 6:
             break
        forcast.append({
            'time': dt.strftime('%m-%d %H:%M:%S'),
            'main': data['main'],
            'weather': data['weather'][0]['main'],
            'weather discription':data['weather'][0]['description']
        })
    return cur_data,forcast