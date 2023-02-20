import math
from pathlib import Path

#initialise wordlists
pathWords = Path(__file__).parent / "words.txt"
pathAnswer = Path(__file__).parent / "answer.txt"

words = []
with open(pathWords) as file:
    words = file.readlines()

answers = []
with open(pathAnswer) as file:
    answers = file.readlines()

wordList = []
for i in range(len(words)):
    wordList.append(words[i].strip('\n'))

answerList = []
for i in range(len(answers)):
    answerList.append(answers[i].strip('\n'))

def filter_available_words(guess_word, colours, possible_words):
    
    minimumCount = [0] * 26
    bounded = [False] * 26
    
    correctPosition = {} #green slots
    wrongPositions = {} #valid characters but with positions to avoid

    for i in range(5):
        char = guess_word[i]
        index = ord(guess_word[i]) - 97
        
        if (colours[i] == 'G'):
            minimumCount[index] += 1
            curr = correctPosition.get(char, [])
            curr.append(i)
            correctPosition[char] = curr
            
        if (colours[i] == 'Y'):
            minimumCount[index] += 1
            curr = wrongPositions.get(char, [])
            curr.append(i)
            wrongPositions[char] = curr
            
        if (colours[i] == 'B'):
            bounded[index] = True
            
            if (guess_word.count(char) == 1):
                wrongPositions[char] = {0, 1, 2, 3, 4}
            else:
                curr = wrongPositions.get(char, [])
                curr.append(i)
                wrongPositions[char] = curr
            
    filtered_words = []
    for word in possible_words:
        flag = False
  
        for char, position in correctPosition.items():
            for i in position:
                if (not (word[i] == char)):
                    flag = True

        if (flag):
            continue
            
        for char, position in wrongPositions.items():
            for i in position:
                if (word[i] == char):
                    flag = True

        if (flag):
            continue
            
        count = {}
        for char in word:
            curr = count.get(char, 0)
            count[char] = curr + 1
                
        for i in range(26):
            char = chr(i + 97)
            curr = count.get(char, 0)
            if (bounded[i]):
                if (not (curr == minimumCount[i])):
                    flag = True
                    break
            else:
                if (not (curr >= minimumCount[i])):
                    flag = True
                    break
            
                    
        if (not flag):
            filtered_words.append(word)
                
    return filtered_words

def generate_smart_guess(word_list, possible_words, nth_guess):
    if (nth_guess == 1):
        return "soare", False
    
    if (len(possible_words) == 1):
        return (possible_words[0])
    
    def giveEntropy(guessWord):
        dis = [0] * 243 # 243 = 3 ^ 5, 0 for black, 1 for yellow, 2 for green; in base-3
        for i in possible_words:
            green = 0
            yellowBlack = 0
            register = {}
            #green pass
            for j in range(5):
                green *= 3
                if (i[j] == guessWord[j]):
                    green += 2
                    count = register.get(i[j], 0)
                    register[i[j]] = count + 1
            #yellow and black pass
            for j in range(5):
                yellowBlack *= 3
                #the number of time the letter guessWord[j] appears
                letterCount = i.count(guessWord[j])
                #the number of time we have encountered guessWord[j]
                currentCount = register.get(guessWord[j], 0)
                if (i[j] == guessWord[j]):
                    continue
                if (currentCount >= letterCount):
                    yellowBlack += 0
                else:
                    yellowBlack += 1
                register[guessWord[j]] = currentCount + 1   
            dis[green + yellowBlack] += 1
        denom = len(possible_words)
        entropy = 0
        for i in dis:
            if (not i == 0):
                entropy += i/denom * math.log2(denom / i)
        return entropy
    
    maximum = 0
    answer = ""
    flag = False
    for i in word_list:
        entropy = giveEntropy(i)
        if (entropy > maximum):
            answer = i
            maximum = entropy

    if (len(word_list) == 1):
        flag = True

    return (answer, flag)

def solver(word_list, answer_list):
    new_answer_list = answer_list
    hint = ""
    guessCounter = 0
    while (hint != "GGGGG"):
        guessCounter += 1
        wordToGuess, flag = generate_smart_guess(word_list, new_answer_list, guessCounter)
        if (wordToGuess == ""):
            print("One of the previous inputs must have been false!")
            print("Please try again!")
            return

        print(wordToGuess)

        if (flag):
            print("Problem Solved!")
            return

        hint = input("Enter new hint!\n")
        
        new_answer_list = filter_available_words(wordToGuess, hint, new_answer_list)
    print("Problem Solved!")
    return i

solver(wordList, answerList)
