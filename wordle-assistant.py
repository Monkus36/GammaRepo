# Software Engineering Fall 2024
# Team Gamma
# Wordle Assistant
# Run 'python wordle-assistant.py'

from random import randrange
game_state_history = []

def rank_word(word_list):
    # How common each letter is by weight
    # All weights sum to a total of 10,000
    frequencyTable = {
        'e': 981,
        'a': 844,
        'r': 777,
        'o': 626,
        't': 621,
        'i': 602,
        'l': 600,
        's': 575,
        'n': 510,
        'u': 425,
        'c': 415,
        'y': 387,
        'h': 351,
        'd': 345,
        'p': 321,
        'g': 278,
        'm': 277,
        'b': 248,
        'f': 192,
        'k': 188,
        'w': 180,
        'v': 138,
        'x': 34,
        'z': 33,
        'q': 27,
        'j': 25
    }
    rankedDict = {}
    for word in word_list:
        score = 0
        for ch in word:
            score = score + frequencyTable[ch]
        rankedDict[score] = word
    
    sorted_dict = dict(sorted(rankedDict.items()))

    # print(sorted_dict) # DEBUGGING

    output = list(sorted_dict.values())[-1]
    
    return output

# Word Guessing Function
# Input a valid gamestate, and the next guess will be returned
def guess_word(game_State):
    
    greenLetters = {}

    yellowLetters = {}

    grayLetters = {}

    graySpecial = {}

    charCount = 0 # Ensures the correct amount of characters have been inputted
    prevLetter = '' # Stores letter to use in combination with symbol
    yellowCount = 0
    greenCount = 0
    grayCount = 0
    graySpecialCount = 0
    guessWord = ''

    for ch in game_State:
        if ch.isspace(): # Handle whitespace
            continue
        elif ch.isalpha(): # Handle letters
            prevLetter = ch
        elif ch in {'=', '-', '.'} and prevLetter != '': # Handle supported symbols
            wordNum = int((charCount/10)+1)
            letterNum = int((((charCount-1) % 10)/2)+1)

            #print("Word " + str(wordNum) + ", Letter " + str(letterNum) + ":  " + prevLetter + " " + ch) # FOR DEBUGGING PURPOSES

            #Adds letters to corresponding dictionaries for use in word guessing
            if ch == '=' :
                greenLetters[greenCount] = [prevLetter, letterNum] 
                greenCount = greenCount+1
                if prevLetter in grayLetters:
                    graySpecial[graySpecialCount] = [prevLetter, grayLetters[prevLetter]]
                    # print(graySpecial) # DEBUGGING
                    del grayLetters[prevLetter]
                    graySpecialCount = graySpecialCount + 1
                    
            elif ch == '-' :
                yellowLetters[yellowCount] = [prevLetter, letterNum] 
                yellowCount = yellowCount+1
                if prevLetter in grayLetters:
                    graySpecial[graySpecialCount] = [prevLetter, grayLetters[prevLetter]]
                    # print(graySpecial) # DEBUGGING
                    del grayLetters[prevLetter]
                    graySpecialCount = graySpecialCount + 1
            elif ch == '.' :
                if prevLetter not in grayLetters and prevLetter not in greenLetters:
                    inYellow = False
                    for item in yellowLetters:
                        if yellowLetters[item][0] == prevLetter:
                            inYellow = True
                    if inYellow == False:
                        grayLetters[prevLetter] = letterNum #gray just stores letters

            prevLetter = '' # Reset previous letter
        else: # Incorrect character inputted
            print("Unexpected Character in Input, Please Try Again")
            return ""
        charCount += 1
    
    # Incorrect amount of characters inputted
    if ((charCount % 10) != 0):
        print("Incorrect Number of Characters, Please Try Again")
        return ""
    
    # Valid input recieved
    wordCount = int((charCount/10))
    # print(str(wordCount) + " Words Inputted") # FOR DEBUGGING PURPOSES

    #Dictionary Debug
    # print("Green")
    # print(greenLetters)
    # print("Yellow")
    # print(yellowLetters)
    # print("Gray")
    # print(grayLetters)
    # print("Special")
    # print(graySpecial)

    #Selecting word list from game state rules
    with open("sortedWords.txt","r") as f:
        words = f.readlines()

    words = [w.strip() for w in words]
    critWords = []

    #input check
    #for ch in grayLetters:
        #if ch in greenLetters:
            #print("Error: Input not valid. Gray letter as Green Letter")
            #return ''
        #if ch in yellowLetters:
            #print("Error: Input not valid. Gray letter as Yellow Letter")
            #return ''

    #default words and rules
    if wordCount == 0:
        guess = 'adieu'
        return guess
    elif wordCount == 1:
        guess = 'wrong'
        return guess
    elif wordCount == 2:
        guess = 'lymph'
        return guess
    elif wordCount == 3:
        guess = 'stack'
        return guess
    elif wordCount > 3:
    #if wordCount > 0:
        for word in words:
            
            failState = False
            for ch in word:
                if grayLetters:
                    if ch in grayLetters:
                        failState = True
                        break
                 
            tempWord = {}
            if greenLetters:
                tempLoc = 1
                for ch in word:
                    tempWord[tempLoc]=ch
                    tempLoc = tempLoc + 1
                for item in greenLetters:
                    if tempWord[greenLetters[item][1]] != greenLetters[item][0]:
                        failState = True
                        break

            if yellowLetters:
                for item in yellowLetters:
                    if yellowLetters[item][0] not in word:
                        failState = True
                        break
                    else:
                        charLoc = 1 
                        for ch in word:
                            if charLoc == yellowLetters[item][1]:
                                if ch == yellowLetters[item][0]:
                                    failState = True
                                    break
                            charLoc = charLoc + 1

            if graySpecial:
                tempLoc = 1
                for ch in word:
                    tempWord[tempLoc]=ch
                    tempLoc = tempLoc + 1
                for item in graySpecial:
                    if tempWord[graySpecial[item][1]] == graySpecial[item][0]:
                        failState = True
                        break

            if failState == True:
                failState = False
            elif word not in critWords:
                critWords.append(word)

    #ranked word choice
    randNum = len(critWords)
    # print (randNum) # DEBUGGING
    if randNum > 0:
        #guessWord = critWords[randrange(randNum)]
        guessWord = rank_word(critWords)
    else:
        guessWord = 'xBADx'

    # for wrd in critWords: # DEBUGGING
    #     print(wrd) 
   
    return guessWord


# INPUT GAMESTATE:
# groups of 5 letters each suffixed by an identifying symbol (EX: 'g.u-e=s.s.')
# Green: "=", Yellow: '-', Gray: '.'
# Whitespace is disregaurded
# Gamestate should be inputted in full
# Information from previous inputs should not be retained
def repeat_previous_state():
    if game_state_history:
        state = game_state_history[-1]
        print(f"Reusing previous state: {state}")
        return state
    else:
        print("No previous state found. Please enter a new game state.")
        return None

state = ""
if __name__ == "__main__":
    while state != "ex":
        state = input("\nEnter Game State ('re' to use previous or 'ex' to exit): ")

        if state.strip().lower() == "re":
            state = repeat_previous_state()
            if state is None:
                continue
        elif state.strip().lower() == "ex":
            continue
        else:
            game_state_history.append(state.lower())

        guess = guess_word(state.lower())
        if guess != "":
            print("You should try '" + guess + "'.")
