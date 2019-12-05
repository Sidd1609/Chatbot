import aiml
import pyttsx
import requests
import json
import wikipedia

speechEngine = pyttsx.init

kernel = aiml.Kernel()
kernel.learn("aiml.xml")


def getweather(city):
    apikey = "8b0488bd2cdeb34c603a962e8b7ab883"
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?appid="+apikey+"&q="+city)

    jsonResponse = response.json()
    return jsonResponse

def getJoke():
    response =  requests.get('https://icanhazdadjoke.com/',headers= {'Accept':'application/json'})
    return json.loads(response.text)

def getWiki(search):
    return wikipedia.summary(search,sentences=2)
def  getWikiPage(page):
    return wikipedia.page(page).content

while True:
    #print(kernel.respond("hi"))
    response = kernel.respond( raw_input("Enter your msg here"))
    responseParts = response.split()
    if len(responseParts)>0:
        if responseParts[0]=='weather':
            #pull data from api
            weatherData = getweather(responseParts[1])
            if weatherData["cod"]!=404:
                temp=weatherData["main"]["temp"]
                f=((temp-273.15)*9)/5+32
                speechEngine.say("the temperature in")
                speechEngine.say(responseParts[1])
                speechEngine.say("is")
                speechEngine.say(f)
                speechEngine.runAndWait()
                print(f)
        elif responseParts[0]=='joke':
            jokeData = getJoke()
            if jokeData["status"]!=404:
                print(jokeData["joke"].encode("utf-8"))
                speechEngine.say(jokeData)
                speechEngine.runAndWait()
            else:
                print("There is some problem gettting your data.")
        elif responseParts[0]=='wikipedia':
            try:
                data=getWiki((response[10:]).encode("utf-8"))
                print(data)
                speechEngine.say(data)
                speechEngine.runAndWait()
            except wikipedia.exceptions.DisambiguationError as e:
                data1=getWikiPage(e.options[0]).encode("utf-8")[:500]
                print(data1)
                speechEngine.say(data1)
                speechEngine.runAndWait()
        else:
            print(response)