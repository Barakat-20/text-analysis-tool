from random_username.generate import generate_username

def welcomeuser():
    print("Welcome to the text analysis tool, I will mine and analyzes a body of text from a file you give me!")

#Get username
def getusername():
    # Get input user into the terminal
    Greetings = input("\nTo begin, please enter your username:\n")

    #usernameLessThan5Chars = len(Greetings) < 5
    #print("Less than 5 characters: " + str(usernameLessThan5Chars))

    #usernameContainsSpaces = " " in Greetings
    #print("Contains spaces: " + str(usernameContainsSpaces))

    #firstCharIsNum = Greetings[0].isdigit()
    #print("First char is digit: " + str(firstCharIsNum))

    #isNotValidIdentifier = not Greetings.isidentifier()
    #print("Is not valid identifier: " + str(isNotValidIdentifier))

    #usernameIsInvalid = usernameLessThan5Chars or isNotValidIdentifier
    
    #or #usernameContainsSpaces or firstCharIsNum# 

    if len(Greetings) < 5 or not Greetings.isidentifier():
        print("Your username must be at least five characters long, alphanumeric only, have no spaces, and cannot start with a number!")
        print("Assigning new username...")
        return generate_username()[0]

    return Greetings


# Print message prompting user to input their name
#print("\nTo begin, please enter your username")

 


#Argument function
#def greetuser(Greetingsx, feelings): 
    # Greet the user
    #print("Hello, " + Greetingsx + ", " + feelings)
    #print("Hey, " + Greetingsx2)
def greetuser(name):
        print("Hello, " + name)


#def textvariable():
    #print("TESTING: " + Greetings)

#def runprogram():

welcomeuser()
Greetings = getusername()
greetuser(Greetings)
#Greetings2 = getusername()
#greetuser(Greetings, "I miss you")
#greetuser("How are you doing?")
#textvariable()

#runprogram()

#Greetingsx is a local variable
#Greetings is a global variable