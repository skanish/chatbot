"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request, response
import json
import datetime
from random import randint
import requests

boto_memory = {"user_name":""}

jokes = ["If a robot does the robot dance is it just called dancing?", "10010100010011100101000101001000101011", "What's a robot’s favorite type of music? Heavy metal"]

apiKey = "65fedf97cad5831bd4b42bd28bdc280d"

@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg').lower()
    boto_memory["user_name"] = request.get_cookie("user_name")
    if not boto_memory["user_name"]:
        boto_memory["user_name"] = user_message.split(" ")[0]
        response.set_cookie("user_name", boto_memory["user_name"])
        return {"animation": "giggling", "msg": "Nice to meet you " + boto_memory["user_name"]}
    if "weather" in user_message:
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Tel+Aviv&APPID=' + apiKey + "&units=metric")
        result = r.json()
        msg = "The weather forecast for Tel Aviv is " + str(result["main"]["temp"]) + "°C"
        return json.dumps({"animation": "excited", "msg": msg})
    elif "love" in user_message:
        return json.dumps({"animation": "inlove", "msg": "I love you!"})
    elif "time" in user_message:
        return time()
    elif "joke" in user_message or "funny" in user_message or "laugh" in user_message or "haha" in user_message or "ha"\
            in user_message or "lol" in user_message:
        return joke()
    elif "scared" in user_message or "afraid" in user_message or "scary" in user_message:
        return json.dumps({"animation": "afraid", "msg": "Don't be scared, I'm always here for you :)"})
    elif "sad" in user_message or "cry" in user_message or "upset" in user_message:
        return json.dumps({"animation": "crying", "msg": "Crying is dangerous for a robot :'("})
    elif "dog" in user_message or "bone" in user_message or "fetch" in user_message:
        return json.dumps({"animation": "dog", "msg": "Dog /dôɡ/ (noun): A mans 2nd best friend... after ROBOTS!!"})
    elif "doing" in user_message or "are" in user_message or "you" in user_message:
        return json.dumps({"animation": "ok", "msg": "I'm great! How are you?"})
    elif "like" in user_message or "do" in user_message or "spare" in user_message:
        return json.dumps({"animation": "takeoff", "msg": "I'm a robot, ain't nobody got time for that!"})
    elif "excited" in user_message or "happy" in user_message or "yay" in user_message:
        return json.dumps({"animation": "crying", "msg": "Crying is dangerous for a robot :'("})
    elif len(user_message) > 8:
        return json.dumps({"animation": "confused", "msg": "I don't understand"})
    else:
        return json.dumps({"animation": "dancing", "msg": "When in doubt... DANCE!"})


# date / time response
def time():
    time = datetime.datetime.now().time()
    return json.dumps({"animation": "waiting", "msg": "The time is:" + str(time)})


# tell me a joke response
def joke():
    ran = randint(0, len(jokes) - 1)
    return json.dumps({"animation": "laughing", "msg": jokes[ran]})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
