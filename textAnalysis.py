import nltk
def main(File):#where all the functions are put together. reads the file and stores the description and the facilities. implements the rest of the functions to produce a value for the 'goodness' of the description.
    Text=File["description"]
    TextWord=wordTokenizing(Text)
    TextSum=len(Text)
    try:
        facilities=File["facilities"]
    except:
        facilities=[]
    Dictionary=DictionaryOfWords(TextWord)
    TextFeatures={"Adjectives":countingAdjectives(Dictionary,TextSum),"Superlatives":countingSuperlatives(Dictionary,TextSum),"Proper Nouns":
    countingProperNouns(Dictionary,TextSum),"numbers":CountingNumbers(Dictionary,TextSum),"Listed Items":listing(TextWord),"missing":checkingFullStops(Text),"holidayWords":HolidayWords(TextWord),
    "facilities":facilitiesCheck(facilities,File["description"]),"sentiment":sentiment(Text)}
    TextFeatures["total"]=weighting(TextFeatures)
    return TextFeatures["total"],summary(Text,Dictionary)

def sentenceTokenizing(Text):#splits the text into an array of sentences
    from nltk.tokenize import sent_tokenize
    # nltk.download('punkt')
    Text=sent_tokenize(Text)
    return Text

def wordTokenizing(Text):#splits the text into an array of words
    from nltk.tokenize import word_tokenize
    # nltk.download('punkt')
    Text=word_tokenize(Text)
    return POS(Text)

def POS(Text):#creates an array of tuples containing the word/punctuation and the part of speech that it is e.g. adjective or noun
    # nltk.download('averaged_perceptron_tagger')
    partsOfspeech=nltk.pos_tag(Text)
    return partsOfspeech

def DictionaryOfWords(Text):#creates a dictionary where the key is the value from the POS array, namely a tuple, and the data is the number of times that appears in the text
    from collections import Counter
    return dict(Counter(Text))

def countingAdjectives(DictionaryOfWords,total):#counts the number of adjectives in the text and returns the percentage of words in the text that are adjectives
    Adjectives=0
    for x in DictionaryOfWords.keys():
        if x[-1]=="JJ":
            Adjectives+=DictionaryOfWords[x]
    return Adjectives/total*100

def countingSuperlatives(DictionaryOfWords,total):#counts the number of superlatives in the text and returns the percentage of words in the text that are superlatives
    Superlatives=0
    for x in DictionaryOfWords.keys():
        if x[-1]=="JJS":
            Superlatives+=DictionaryOfWords[x]
    return Superlatives/total*100

def countingProperNouns(DictionaryOfWords,total):#counts the number of proper nouns in the text and returns the percentage
    Nouns=0
    for x in DictionaryOfWords.keys():
        if x[-1]=="NNP" or x[-1]=="NNPS":
            Nouns+=DictionaryOfWords[x]
    return Nouns/total*100

def CountingNumbers(DictionaryOfWords,total):#counts the number of numbers in the text and returns the percentage
    numbers=0
    for x in DictionaryOfWords.keys():
        if x[-1]=="CD":
            numbers+=DictionaryOfWords[x]
    return numbers/total*100

def listing(Text):#returns the number of listed items in the text
    lists=0
    Comma=False
    count=0
    for x in range(len(Text)):
        if Text[x][0]=="," and Comma==False:
            Comma=True
        elif Text[x][0]=="," and Comma==True:
            count+=1
        if Text[x][0]=="." or Text[x][0]==":" or Text[x][0]=="!":
            Comma=False
            if count>3:
                lists+=count+1
                count=0
    return lists

def checkingFullStops(Text):#returns the number of missing spaces after the end of a sentence and the number of missing capitals at the start of a sentence.
    missingSpaces=0
    missingCapitals=0
    for x in range(len(Text)-2):
        if Text[x]=="." and Text[x-1].isnumeric()==False and Text[x+1].isnumeric()==False:
            if Text[x+1]!=" ":
                missingSpaces+=1
                #print(Text[x-1],Text[x],Text[x+1])
                if Text[x+1]!=Text[x+1].capitalize():
                    missingCapitals+=1
            elif Text[x+2]!=Text[x+2].capitalize():
                missingCapitals+=1
    return missingSpaces,missingCapitals

def HolidayWords(Text):#returns the percentage of words in the text that are in the document containing words about holidays
    FoundWords=0
    file=open("holidayWords.txt",'r')
    words=file.readlines()
    file.close()
    for x in range(len(words)):
        words[x]=words[x].strip("\n")
    words=set(words)
    for x in range(len(Text)):
        if Text[x][0].lower() in words:
            FoundWords+=1
    return FoundWords/len(words)*100

def weighting(Features):#for each attribute of the text a calculation is done to find a value, this is done by modelling each attribute as a different cubic function depending on its importance and normal range of that
    #attribute. these are then calculated for the value of this attribute in the specific text and all of these are added together to get a total 'score' of how 'good' the text is.
    import math
    adjective=(-(math.pow(Features["Adjectives"],3))/15)+(7*Features["Adjectives"])
    Superlative=(-(math.pow(Features["Superlatives"],3))/100)+(0.6*Features["Superlatives"])
    Nouns=(-(math.pow(Features["Proper Nouns"],3))/5)+(3*Features["Proper Nouns"])
    numbers=(-50*(math.pow(Features["numbers"],3)))+(25*Features["numbers"])
    lists=(-(math.pow(Features["Listed Items"],3))/200)+5
    missing=((-(math.pow(Features["missing"][0],3))/100)-Features["missing"][0]+8)+((-(math.pow(Features["missing"][1],3))/100)-Features["missing"][1]+8)
    holiday=(-(math.pow(Features["holidayWords"],3))/60)+(4*Features["holidayWords"])
    facilities=(-(math.pow(Features["facilities"],3))/1000)
    sentiment=math.pow(Features["sentiment"],3)/100000
    #print("adjective:",adjective,",","superlative:",Superlative,",","Nouns:",Nouns,",","numbers:",numbers,",","lists:",lists,",","missing:",missing,",","holiday:",holiday,",","facilities:",facilities,",","sentiment:",sentiment)
    return adjective+Superlative+Nouns+numbers+lists+missing+holiday+facilities+sentiment

def JSON():#returns a dictionary for each JSON file 
    import json
    f=open("Json1.txt",'r')
    file1=json.load(f)
    f.close()
    f=open("Json2.txt",'r')
    file2=json.load(f)
    f.close()
    return file1,file2

def facilitiesCheck(facilities,description):#calculates how many facilities are repeated in the description
    repeated=0
    for x in facilities:
        if x["label"].capitalize() in description or x["label"].lower() in description:
            repeated+=1
    return repeated

def sentiment(Text):#calculates the semtimental value of the text - from -1 to 1 where 1 is positive and -1 is negative
    # nltk.download('vader_lexicon')
    from nltk.sentiment import  SentimentIntensityAnalyzer
    s=SentimentIntensityAnalyzer()
    return s.polarity_scores(Text)["compound"]*100

def summary(Text,Frequencies):#returns a summary of the text based on how many of the words in each sentence aren't stop words
    # nltk.download('stopwords')
    filtered={}
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    stop_words=set(stopwords.words("english"))
    for word in Frequencies.keys():
        if word[0] not in stop_words:
            filtered[word]=Frequencies[word]
    Max_value=max(filtered.values())

    for word in filtered.keys():
        filtered[word]=filtered[word]/Max_value
    
    sentences=sentenceTokenizing(Text)
    sentenceWeight=dict()
    for sentence in sentences:
        sentenceWordCount=(len(word_tokenize(sentence)))
        sentenceCountWithoutStopWords=0
        for weight in filtered:
            if weight[0].lower() in sentence.lower():
                sentenceCountWithoutStopWords+=1
                if sentence in sentenceWeight:
                    sentenceWeight[sentence]+=filtered[weight]
                else:
                    sentenceWeight[sentence]=filtered[weight]
        sentenceWeight[sentence]=sentenceWeight[sentence]

    from heapq import nlargest
    length=5
    summary=nlargest(length,sentenceWeight,key=sentenceWeight.get)
    final=[word for word in summary]
    summary='   '.join(final)
    return summary


