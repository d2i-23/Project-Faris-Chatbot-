from bs4 import BeautifulSoup
import requests
from googlesearch import search
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer



texts = TextRankSummarizer()

def summarize(text):
    parser = PlaintextParser.from_string(text,Tokenizer("english"))

    summary = texts(parser.document, 30)
    summaryString = ''

    for sentence in summary: 
        summaryString += str(sentence) + ' '

    return summaryString
    
 

def findParagraphs(link):
    req = requests.get(link)
    soup = BeautifulSoup(req.content, "html.parser")
    p = soup.select('p')
    pList = []

    for paragraphs in p: 
        item = paragraphs.get_text()
        pList.append(item)

    

    return ''.join(pList)


def searchGoogle(contents, noOfSearch = 1):
    print(contents)
    textList = []
    links = []


    for link in search(contents, lang = 'en'):
        #print(link)
        try: 
            words = findParagraphs(link)
            
            if len(words) > 3000:
                words = words #summarize(words, contents)

            if words != '':
                links.append(link)
                textList.append(words)

                if len(textList) == noOfSearch:
                    break
        except:
            pass

        
    return ' '.join(textList), links
    
    #! Will not work with vpn 

#print(searchGoogle('Pandas Release Date '))



