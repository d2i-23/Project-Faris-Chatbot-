from flask import Flask, request, jsonify, send_file
from chat import runConversation, sentiment
import os
from voice import generateVoice, processCode
import threading
from time import sleep

app = Flask(__name__)




@app.route('/returnResponse', methods=['GET', 'POST'])
def returnResponse():

    if request.method == "POST":
        form = request.get_json()
    #try: 
    response, memory = runConversation(form['message'], form['sentMemory'])
    if response != '':
        
        processedResponse = processCode(response)
        token, length = generateVoice(processedResponse)
        feeling = sentiment(processedResponse)
        return jsonify({'response': [{'message': response, 'token': token, 'mood': feeling, 'time': length}], 'sentMemory': memory}), 200

    #except: 
        #token, length = generateVoice('what?')
        #return jsonify({'response': [{'message': 'what?', 'token': token, 'mood': 'exp_05', 'time': length}, form['sentMemory']], 'sentMemory': form['sentMemory']}), 200


@app.route('/Resources', methods=['POST'])
def resources():
    if request.method == "POST":
        form = request.get_json()
        fileLocation = form["location"][4:]

        filename = os.path.basename(fileLocation)
        extention = os.path.splitext(filename)[1]

        mimetypes2 = None
        if extention == '.png':
            mimetypes = "image/png"

        return send_file(fileLocation, mimetype=mimetypes2)


@app.route("/Resources/Mao/Mao.2048/texture_00.png", methods = ["GET"])
def resourcesPNG():
    return send_file("Resources/Mao/Mao.2048/texture_00.png", mimetype= "image/png")


def deleteAudio(path):
    sleep(1)
    os.remove(os.path.join(os.getcwd(), 'RRcode', 'audioResult', path +'.wav'))


@app.route("/audioBeg", methods = ["POST"])
def getAudio():
    if request.method == "POST":
        form = request.get_json()
        location = form['token']
        deletingFile = threading.Thread(target = deleteAudio, args=(location, ))
        deletingFile.start()
        return send_file(f'audioResult/{location}.wav', mimetype= 'audio/wav')


if __name__ == '__main__':
    app.run(host='localhost', port=5000)

