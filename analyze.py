from random_username.generate import generate_username
import re, nltk, json
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import pos_tag
from wordcloud import WordCloud
# NLTK DATA PATH (Render)
nltk.data.path.append("/opt/render/nltk_data")

wordLemmatizer = WordNetLemmatizer()
STOP_WORDS = set(stopwords.words('english'))
sentimentAnalyzer = SentimentIntensityAnalyzer()
from io import BytesIO
import base64

# Welcome User
def welcomeuser():
    print("Welcome to the text analysis tool, I will mine and analyzes a body of text from a file you give me!")

#Get username
def getusername():

    maxAttempts = 3
    attempts = 0

    while attempts < maxAttempts:
        # Print message prompting user to input their name
        inputPrompt = ""
        if attempts == 0:
            inputPrompt = "\nTo begin, please enter your username:\n"
        else:
            inputPrompt = "\nPlease try again:\n"
        Greetings = input(inputPrompt)

        #Validate username
        if len(Greetings) < 5 or not Greetings.isidentifier():
            print("Your username must be at least five characters long, alphanumeric only, have no spaces, and cannot start with a number!")
        else:
            return Greetings
        
        attempts += 1
    
    print("\nExhusted all " + str(maxAttempts) + " attempts, assigning new username...")
    return generate_username()[0]

# Greet the user
def greetuser(name):
        print("Hello, " + name)

# Get text from file
def getArticleText():
    f = open("files/article.txt", "r")
    rawText = f.read()
    f.close()
    return rawText.replace("\n", " ").replace("\r", "")

# Extract Sentences from raw Text Body 
def tokenizeSentences(rawText):
    return sent_tokenize(rawText)

# Extract Words from list of Sentences
def tokenizeWords(sentences):
    words = []
    for sentence in sentences:
        words.extend(word_tokenize(sentence))
    return words
    
# Get the key sentences based on serch pattern of key words
def extractKeySentences(sentences, searchPattern):
    matchedSentences = []
    for sentence in sentences:
        #If sentence matches desired pattern, add to matchedSentences
        if re.search(searchPattern, sentence.lower()):
            matchedSentences.append(sentence)
    return matchedSentences

# Get the average words per sentence, exculding punctuation
def getWordsPerSentences(sentences):
    totalWords = 0
    for sentence in sentences:
        totalWords += len(sentence.split(" "))
    return totalWords / len(sentences)

# Convert part of speech from pos_tag function into wordnet compatible pos tag
posToWordnetTag = {
    'J': wordnet.ADJ,
    'V': wordnet.VERB,
    'N': wordnet.NOUN,
    'R': wordnet.ADV
}

def treebankPosToWordnetPos(partOfSpeech):
    posFirstChar = partOfSpeech[0]
    if posFirstChar in posToWordnetTag:
        return posToWordnetTag[posFirstChar]
    return wordnet.NOUN


# convert raw list of (word, pos) tuples to a list of strings that
# only include valid english words
def cleasneWordList(posTaggedWordTuples):
    cleasneWords = []
    invalidWordPattern = "[^a-zA-Z-]"
    for posTaggedWordTuple in posTaggedWordTuples:
        word = posTaggedWordTuple[0]
        pos = posTaggedWordTuple[1]
        cleasneWord = word.replace(".", "").lower()
        if (not re.search(invalidWordPattern, cleasneWord)) and len(cleasneWord) > 1 and cleasneWord not in STOP_WORDS:
            cleasneWords.append(wordLemmatizer.lemmatize(cleasneWord, treebankPosToWordnetPos(pos)))
    return cleasneWords

def analyzeText(textToAnalyze):
    articleSentences = tokenizeSentences(textToAnalyze)
    articleWords = tokenizeWords(articleSentences)

    #Get Sentence Analytics
    stockSearchPattern = "[0-9]|[%$€£]|thousand|million|billion|trillion|profit|loss"
    keySentences = extractKeySentences(articleSentences, stockSearchPattern)
    wordsPerSentence = getWordsPerSentences(articleSentences)

    # Get Word Analytics 
    wordPosTagged = pos_tag(articleWords)
    articleWordsCleansed = cleasneWordList(wordPosTagged)

    #Generate Word Cloud
    separator = " "
    wordCloudFilePath = "results/wordcloud.png"
    wordcloud = WordCloud(width=800, height=400,\
    background_color="white", colormap="viridis", collocations=False).generate(separator.join(articleWordsCleansed))
    # wordcloud.to_file(wordCloudFilePath)

   # Convert WordCloud → PIL Image
    image = wordcloud.to_image()

    # Save image to memory buffer
    imgIO = BytesIO()
    image.save(imgIO, format="PNG")
    imgIO.seek(0)

    # Encode as Base64
    encodedWordCloud = base64.b64encode(imgIO.read()).decode("utf-8")


    # Run sentiment Analysis
    sentimentReslt = sentimentAnalyzer.polarity_scores(textToAnalyze)

    # Collate analysis into one dictionary
    finalReslt = {
    "data": {
            "keySentences": keySentences,
            "wordsPerSentence": round(wordsPerSentence, 1),
            "sentiment": sentimentReslt,
            "wordCloudFilePath": wordCloudFilePath,
            "wordCloudImage": encodedWordCloud
        },
        "metadata": {
            "sentencesAnalyzed": len(articleSentences),
            "wordAnalyzed": len(articleWordsCleansed),
        }
    }
    return finalReslt
def runAsFile():
    # Get user Details
    welcomeuser()
    Greetings = getusername()
    greetuser(Greetings)

    #Extract and Tokenize Text
    articleTextRaw = getArticleText()
    analyzeText(articleTextRaw)
