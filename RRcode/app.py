from flask import Flask, request, jsonify, send_file, after_this_request
from chat import runConversation, sentiment
import os
from voice import generateVoice

app = Flask(__name__)



@app.route('/returnResponse', methods=['GET', 'POST'])
def returnResponse():

    if request.method == "POST":
        
        form = request.get_json()
        response = runConversation(form['message'])
        token, length = generateVoice(response)
        feeling = sentiment(response)

        return jsonify({'message': response, 'token': token, 'mood': feeling, 'time': length}), 200


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

@app.route("/audioBeg", methods = ["POST"])
def getAudio():
    if request.method == "POST":
        form = request.get_json()
        deleteOrNot = form['delete']
        location = form['token']
        absolute = os.path.join(os.getcwd(), 'RRcode')
        '''
        
        for roots, dir, files in os.walk(os.path.join(absolute, 'audioResult')):
            for file in files:
                if file.find("-del") != -1:
                    os.remove(os.path.join(absolute, roots, file))
        
        if deleteOrNot:
            delLocation = location + "-del"

            location1 = os.path.join(absolute, "audioResult", location + ".wav")
            location2 = os.path.join(absolute, "audioResult", delLocation + ".wav")
            os.rename(location1, location2)
            location = delLocation 
        '''
        return send_file(f'audioResult/{location}.wav', mimetype= 'audio/wav')


if __name__ == '__main__':
    app.run(host='localhost', port=5000)

