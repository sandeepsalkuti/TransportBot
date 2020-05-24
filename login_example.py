
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import googlemaps
import json
import time
import re


app = Flask(__name__)

app.secret_key = 'mysecret'

app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb+srv://sumanth:sumanth123@sumanth-mzjwn.mongodb.net/test?retryWrites=true&w=majority'

mongo = PyMongo(app)
english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(english_bot)
#trainer.train("chatterbot.corpus.english")
#trainer.train("static\my_export.json")

trainer = ListTrainer(english_bot)

trainer.train([
    "what are the nearby gas stations",
    "could you please share your location.You can tap on the location button",
    "what are the nearby hardware stores",
    "could you please share your location.You can tap on the location button",
    "what are the nearby car repair",
    "could you please share your location.You can tap on the location button",
     "How are you?",
     "I am good.",
     "That is good to hear.",
     "Thank you",
     "You are welcome.",
])

trainer.train([
    "Greetings!",
    "Hello",
])

#trainer.export_for_training('./my_export.json')


@app.route('/')
def index():
    if 'username' in session:
        return render_template("test4.html")
        

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.checkpw(request.form['pass'].encode('utf-8'), login_user['password']):

        #if bcrypt.checkpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
        #if bcrypt.checkpw(bytes(request.form['pass'], 'utf-8'), hashpass) == hashpass:
        #if bcrypt.checkpw(pass, hashed):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            global hashpass
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass,'phonenumber' : request.form['Mobile'],
            'userAddress' : request.form['Address']})              
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')
@app.route("/get")
def getBotResponse():
    userText = request.args.get('data')
    global userquery
    #print(userText)
    
    #pattern = '.*'
    #txt = "gas station near me"
    if(re.search("^.*gas station.*$", userText)):
        userquery= {}
        userquery["0"]="gas_station"
    elif(re.search("^.*locksmith.*$", userText)):
        userquery= {}
        userquery["0"]="locksmith"
    elif(re.search("^.*car wash.*$", userText)):
        userquery= {}
        userquery["0"]="car_wash"
    elif(re.search("^.*hardware store.*$", userText)):
        
        userquery= {}
        userquery["0"]="hardware_store"
    elif(re.search("^.*car repair.*$", userText)):
        
        userquery= {}
        userquery["0"]="car_repair"


    #completestring = re.search(drivname[i]+pattern+drivver[i], userText)
    #print(lat_lng)
    if "longitude" in userText and "latitude" in userText:
        lat_lng = userText.split(":")
        print(userquery["0"])
        API_KEY = 'AIzaSyDK_M2hCax5JASPRAxKQ15ySRZPQ0232GU'
        gmaps = googlemaps.Client(key = API_KEY)
        #longitude:-94.58083169999999:latitude:39.060986199999995:locksmith
        places_result  = gmaps.places_nearby(location=lat_lng[3]+","+lat_lng[1], radius = 3000, open_now =False , type = ''+userquery["0"])
        del userquery["0"]
        #print(userquery["0"])
        dict1={}
        for i in range(3):
            place=places_result['results'][i]
            my_place_id = place['place_id']
            my_fields = ['name','formatted_phone_number','website']
            details  = gmaps.place(place_id= my_place_id , fields= my_fields)
            
            dict1["place"+str(i)] = details['result']
        print(dict1)
        return dict1
    else:
        return str(english_bot.get_response(userText))


    #You appear to be at longitude: -94.5809031 and latitude: 39.060996599999996 'rating', 'review'
@app.route('/logout',methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    
    app.run(debug=True)
