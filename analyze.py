def welcomeuser():
    print("Welcome to the text analysis tool, I will mine and analyzes a body of text from a file you give me!")

#Get username
def getusername():
    # Get input user into the terminal
    Greetings = input("\nTo begin, please enter your username:\n")
    return Greetings
# Print message prompting user to input their name
#print("\nTo begin, please enter your username")


#Argument function
def greetuser(Greetingsx, feelings): 
    # Greet the user
    print("Hello, " + Greetingsx + ", " + feelings)
    #print("Hey, " + Greetingsx2)

#def textvariable():
    #print("TESTING: " + Greetings)

#def runprogram():

welcomeuser()
Greetings = getusername()
#Greetings2 = getusername()
greetuser(Greetings, "I miss you")
#greetuser("How are you doing?")
#textvariable()

#runprogram()

#Greetingsx is a local variable
#Greetings is a global variable