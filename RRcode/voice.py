import azure.cognitiveservices.speech as speechsdk
from tokenStore import speech_key
from secrets import token_hex
import wave 



def generateVoice(text, sentiment = None):

    service_region = "canadacentral"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = ""
    #"en-US-AnaNeural"
    token = token_hex(16)
    
    audioConfig = speechsdk.audio.AudioOutputConfig(filename= f"RRCode\\audioResult\\{token}.wav")
    #audioConfig.set_property(speechsdk.PropertyId.SpeechServiceResponse_RequestSynthesisOutputFormat, speechsdk.OutputFormat.Riff24Khz16BitMonoPcm)
    ssmlString = f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'><voice name='en-US-AshleyNeural'><prosody pitch='+20%' rate = '+5%'>{text}</prosody></voice></speak>"
    #ssmlString = f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='zh-CN'><voice name='zh-CN-XiaochenNeural'><prosody pitch='+20%' rate = '+5%'>{text}</prosody></voice></speak>"
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audioConfig)


    # use the default speaker as audio output.
    speech_synthesizer.speak_ssml_async(ssmlString).get()

    with wave.open(f"RRCode\\audioResult\\{token}.wav", 'rb') as wave_file:
        length =  wave_file.getnframes() / float(wave_file.getframerate())
    
    return token, length


