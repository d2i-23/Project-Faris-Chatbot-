from flask import Flask, request, jsonify, send_file, after_this_request
from chat import runConversation, sentiment
import os
from voice import generateVoice
import threading
from time import sleep

app = Flask(__name__)




@app.route('/returnResponse', methods=['GET', 'POST'])
def returnResponse():

    if request.method == "POST":
        form = request.get_json()
        try: 
            response = runConversation(form['message'])
            if response != '':
                token, length = generateVoice(response)
                feeling = sentiment(response)
                return jsonify({'message': response, 'token': token, 'mood': feeling, 'time': length}), 200
        except: 
            token, length = generateVoice('what?')
            return jsonify({'message': 'what?', 'token': token, 'mood': 'exp_05', 'time': length}), 200


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

