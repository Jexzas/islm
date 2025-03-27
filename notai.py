from collections import defaultdict
import random
import re
import json
api = "https://api.dictionaryapi.dev/api/v2/entries/en/"
mode = input("Are you using training mode? 1 for yes, 2 for no")
path = "./book.txt" if mode == "1" else "./book2.txt"
text = ""
words = []
with open(path, "r", encoding="UTF-8") as file:
    text = "".join(file.read())
words = text.split(" ")

def convertTextToNextTable(text):
    newText = re.sub(r"[^\w\s]", "", text)
    finalClean = newText.lower().split()
    next_word_table = []
    for x in finalClean:
        next_word_table.append({x: finalClean[finalClean.index(x) + 1]})
    return next_word_table

def convertTableToFreqTable(table):
    finalTable = defaultdict(int)
    actualFinalTable = {}

    # Count occurrences of word pairs
    for pair in table:
        for key, value in pair.items():
            finalTable[(key, value)] += 1

    # Determine the most frequent next word for each word
    word_max_freq = defaultdict(lambda: (None, 0))  # Stores (word, max count)

    for (word, next_word), count in finalTable.items():
        if count > word_max_freq[word][1]:  # Compare count with stored max
            word_max_freq[word] = (next_word, count)

    # Convert to the desired dictionary format
    actualFinalTable = {word: next_word for word, (next_word, _) in word_max_freq.items()}

    return actualFinalTable 
frequency_table = []

def respond(prompt, text, table):
    words = prompt.lower().split()
    match = False
    matchWord = ""
    counter = 0
    while counter < len(words):
        rand = random.randint(0, len(words) -1)
        word = words[rand]
        if len(table) > 0:
            for x in table:
                if word == x:
                    match = True
                    counter += 1
                    matchWord = word
                else:
                    counter += 1
        else:
            nexties = convertTextToNextTable(text)
            table = convertTableToFreqTable(nexties)

    if match == False:
        matchWord = "the"
    responseString = " "
    while len(responseString) < 600:
        for x in table.keys():
            if x == matchWord:
                if matchWord != table[x]:
                    responseString += table[x] + " "
                    matchWord = table[x]
                else:
                    responseString += ". "
                    matchWord = random.choice(list(table.keys()))       
    print(responseString)
    newLine = str(text + prompt + ". " + responseString + ". ")
    newText = open("book2.txt", "w", encoding="UTF-8")
    newText.write(newLine)
    nexties = convertTextToNextTable(text)
    new_frequency_table = convertTableToFreqTable(nexties)
    file2 = open("model.txt", "w", encoding="UTF-8")
    file2.write(str(new_frequency_table))
    
exists = False

try:
    f = open("model.txt", "x")
    f.close()
except FileExistsError:
    exists = True

if exists:
    file = open("model.txt", "r")
    againFile = file.read()
    frequency_table = json.loads(againFile.replace("\'", "\""))
    userValue = input("What would you like a response for? ")
    respond(userValue, text, frequency_table)
else: 
    nexties = convertTextToNextTable(text)
    frequency_table = convertTableToFreqTable(nexties)
    f = open("model.txt", "w")
    f.write(str(frequency_table))