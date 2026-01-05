from random_username.generate import generate_username
from nltk.tokenize import word_tokenize, sent_tokenize
import re
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


# Get user Details
welcomeuser()
Greetings = getusername()
greetuser(Greetings)

#Extract and Tokenize Text
articleTextRaw = getArticleText()
articleSentences = tokenizeSentences(articleTextRaw)
articleWords = tokenizeWords(articleSentences)

#Get Analytics
stockSearchPattern = "[0-9]|[%$€£]|thousand|million|billion|trillion|profit|loss"
keySentences = extractKeySentences(articleSentences, stockSearchPattern)
wordsperSentence = getWordsPerSentences(articleSentences)

# Print for testing
print("GOT:")
print(wordsperSentence)
