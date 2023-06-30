import openai 
from tokenStore import GptToken
import json 
import numpy as np
from math import sqrt
import os 
from nltk.sentiment.vader import SentimentIntensityAnalyzer


openai.api_key = GptToken


# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API


#? Contain a short-term embed that stores memory inside RAM and when the conversation changed topic or the ai got closed
#? The RAM stored memory will summarize itself and store itself to the actual log 
#! if you run into RAM problems, store them inside a folder for shortterm specifically and gets cleared with each period 

#* First step is to make an embed main class that is responsible for two things: embedding data and translating translate embedded data
#* Second step is to make a subclass that is responsible for containing short term data, summarizing the group of data (with each iteration that is added), and summarize itself and classify 
#* itself to a topic 
#* Thirdly, create a function that is able to tell when the topic has changed (likely by detecting whether the cosine similarity reaches a certain point  )
#? Sort the similarity score (higher score means more in common)

#! considering saving the data inside a spreadsheet and process it with polars (pandas may be too slow for this)
#! Pair all memories in the short term memory together and summarize it (including the input message) before presenting it to chatgpt 

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

    def evaluateLog(self):
        self.idCount = len(os.listdir('RRcode/memoryLogs'))

    def appendMessage(self, message):
        
        self.memoryList.append(message)
        self.adjustSituation()
    
    def adjustSituation(self):
        if len(self.memoryList) > self.shortrecall:
            wordLengths = len(self.memoryList[0]['content'])
            
            self.storeMemory(self.memoryList[0])
            del self.memoryList[0]
            
            #* AI stores the most recent 6 dialogues and with each 7th, the one at the start will be categorized into the longterm memory

    def includeResponse(self, response):
        self.memoryList[-1]["role2"] = "assistant"  
        self.memoryList[-1]["content2"] = response
  
    def storeMemory(self, memory):
        '''
        self.idCount += 1
        memory['id'] = self.idCount

        with open(f'RRCode/memoryLogs/{self.idCount}.json', 'w') as f:
            f.write(json.dumps(memory))
        '''
        pass
    def returnMemory(self):
        return self.memoryList 
        
'''
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
'''

def createMessage(ShortMemory, LongMemory, current):
    personality = {'role': "system", "content": 'Your name is Faris, an AI developped by the person called d2i-23. You act like an ordinary girl, and speak at most 3 sentences.'} #You speak at most 3 sentences. You add Nyaa~ at the end of each sentence
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
        return 'exp_08' if scores['neg'] > scores['pos'] else 'exp_02'



def runConversation(messageInput):   
    # Step 1: send the conversation and available functions to GPT

    memory = ShortTermMemory(3)
    #longMemory = LongTermMemory(recall = 1)

    memory.evaluateLog()
    
    message = memory.embed(messageInput)
    shortTermMemory = memory.returnMemory()
    #longTermMemory = longMemory.searchMostCompatable(message)
    memories = createMessage(shortTermMemory, [], message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages= memories,
    )
    
    memory.appendMessage(message)
    memory.includeResponse(response['choices'][0]['message']["content"])

    
    return response['choices'][0]['message']["content"]


#Step 1: Make the ai be able to recall recent conversation topics 
#Embed each input 
'''
while True:
    print(runConversation(input("User: ")))
    print('\n')
'''