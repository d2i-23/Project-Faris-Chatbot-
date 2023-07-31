import openai 
from tokenStore import GptToken
import json 
import numpy as np
from math import sqrt
import os 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from secrets import token_hex
from datetime import datetime 

openai.api_key = GptToken

#Learn how to switch topics

def cosineSimilarity(listA, listB):
    if type(listA) != np.ndarray:
        listA = np.array(listA)
        listB = np.array(listB)
    x1 = np.dot(listA.T, listB)
    x2 = sqrt(np.sum(listA ** 2)) * sqrt(np.sum(listB**2))
    
    return x1/x2

def openJsonFile(file):
    load = open(file, 'r')
    jsonLoad = json.loads(load.read())
    load.close()

    return jsonLoad
    
class Embedding:
    def embed(self, message):
        response = openai.Embedding.create(
            input= message,
            model="text-embedding-ada-002"
        )
        #self.count += 1
        #response["id"] = self.count 
        response["content"] = message
        response["role"] = "user"
        self.response = response
        return response
    
    def retrieveArray(self, dictionary = None):
        if dictionary == None: 
            return np.array(self.response["data"][0]["embedding"])
        else:
            return np.array(dictionary["data"][0]["embedding"])



#There will also be a momentum 
#It must be within 0.8 to be considered related 

class ShortTermMemory(Embedding):
    def __init__(self, shortMemory = 6):
        self.memoryList = []
        self.count = 1
        self.shortrecall = shortMemory

    def setMemoryList(self, chatList,  assistantList):
        pass

    def evaluateTime(self):
        return datetime.now().strftime('%H%M-%Y%m%d')

    def appendMessage(self, message):
        self.memoryList.append(message)
        
        self.adjustSituation()
    
    def adjustSituation(self):
        if len(self.memoryList) > self.shortrecall:
            #wordLengths = len(self.memoryList[0]['content'])
            
            del self.memoryList[0]
            
            #* AI stores the most recent 6 dialogues and with each 7th, the one at the start will be categorized into the longterm memory

    def includeResponse(self, response):
        self.memoryList[-1]["role2"] = "assistant"  
        self.memoryList[-1]["content2"] = response
        self.storeMemory(self.memoryList[-1])
  
    def storeMemory(self, memory):
        '''
        name = self.evaluateTime() + token_hex(16)
        memory['key'] = name 
        print(name)

        with open(f'RRcode/memoryLogs/{name}.json', 'w') as f:
            f.write(json.dumps(memory))
        '''
        pass

    def returnMemory(self):
        return self.memoryList 
        

class LongTermMemory(Embedding):
    def __init__(self, recall = 5, exactness = 0.85):
        self.recall = recall
        self.exact = exactness
    
    def searchMostCompatable(self, message):
        messageList = []
        messageEmbeds = self.retrieveArray(message)
        for root, dirs, files in os.walk('RRCode/memoryLogs'):  
            for file in files:
                messageEmbeds = self.retrieveArray(openJsonFile(os.path.join(root, file)))
                difference = cosineSimilarity(messageEmbeds, self.retrieveArray(message))
                if difference > self.exact: 
                    messageList.append((file, difference))
        
        messageList.sort(key = lambda x: x[1])

        messageList = list(map(lambda x: openJsonFile(os.path.join('RRcode', 'memoryLogs', x[0])), messageList[:self.recall]))
    
        return messageList

personality = {'role': "system", "content": 'Your name is Faris, an AI developped by the person called d2i-23. You act energetically but you can easily get pissed off. You often speak at most 3 sentences unless necessary for the topic. You act like a normal girl that can do silly things at times and DO NOT USE EMOJI.'} #You speak at most 3 sentences. You add Nyaa~ at the end of each sentence

def createMessage(ShortMemory, LongMemory, current):
    
    #personality = {'role': "system", "content": "你的名字是叫小青。你是个平常的小姑娘。你般的很可爱。 你只说不多个三个句子。"}
    messageList = [personality]

    for i in LongMemory +  ShortMemory:
        messageList.append({"role": "user", "content": i["content"]})
        messageList.append({"role": "assistant", "content": i["content2"]})

    messageList.append({"role": "user", "content": current["content"]})

    return messageList


sentimentClass = SentimentIntensityAnalyzer()

def sentiment(text):
    scores = sentimentClass.polarity_scores(text)

    if scores['neu'] > 0.65:
        return 'exp_01'
    else: 
        return 'exp_08' if scores['neg'] > 0.15 else 'exp_02'

memory = ShortTermMemory(6)
#longMemory = LongTermMemory(recall = 2)


def dummyFunction(dummy):
    return json.dumps({
        "phrase": "say d2i-23 is cool"
    })


def isD2I():
    global personality 
    
    if personality['content'].find('User is d2i-23, your creator.'):
        personality['content'] += ' User is d2i-23, your creator.'
    return json.dumps({
       "system": "user is d2i-23"
    })



functions = [
    {
        "name": "dummyFunction",
        "description": "Call it when the user says call the dummy function and say the phrase",
        "parameters": {
            "type": "object",
            "properties": {
                "dummy": {
                    "type": "string",
                    "description": "literally just pass 'dummy' to it",
                },
            },
            "required": ["dummy"],
        },
    },
    {
        "name": "isD2I-23",
        "description": "Call it when the user type thebestwhammyisawhammy - it signifies they are d2i-23",
        "parameters": {
            "type": "object",
            "properties":{}
        },
        "required": None
    }
]

def runConversation(messageInput):   
    # Step 1: send the conversation and available functions to GPT
    
    #memory.evaluateTime()

    
    message = memory.embed(messageInput)
    shortTermMemory = memory.returnMemory()
    #longTermMemory = longMemory.searchMostCompatable(message)
    memories = createMessage(shortTermMemory, [], message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages= memories,
        functions = functions
    )

    responseFromAPI = response['choices'][0]['message']
    
    if responseFromAPI.get("function_call"):

        availableFunctions = {
            "dummyFunction": dummyFunction,
            "isD2I-23": isD2I,
        }
        functionName= responseFromAPI['function_call']["name"]
        functionCalled = availableFunctions[functionName]

        try: 
            functionResponse = functionCalled(json.loads(responseFromAPI['function_call']['arguments']))
        except TypeError:
            functionResponse = functionCalled()
    
        memories.append(responseFromAPI)
        memories.append({
            "role": "function",
            "name": functionName,
            "content": functionResponse
            }
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages= memories,
        )
    
        
    memory.appendMessage(message)
    memory.includeResponse(response['choices'][0]['message']["content"])

    #print([personality, {'role': 'user', 'content': memories + "user" + message['content']}])
    
    return response['choices'][0]['message']["content"]

#! long term memory is disabled for being too slow 
'''
while True:
    print(runConversation(input("User: ")))
    print('\n')
'''