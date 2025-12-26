from random_username.generate import generate_username

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

welcomeuser()
Greetings = getusername()
greetuser(Greetings)
articleTextRaw = getArticleText()
print("GOT:")
print(articleTextRaw)