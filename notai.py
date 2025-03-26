import requests
api = "https://api.dictionaryapi.dev/api/v2/entries/en/"
path = "./book.txt"
text = ""
words = []
with open(path, "r", encoding="UTF-8") as file:
    text = "".join(file.readlines())
words = text.split(" ")

def convertTextToNextTable(table):
    betterWords = [s for s in words if s]
    step2 = [s.replace('\n', '') for s in betterWords]
    step3 = [s.replace('!', '') for s in step2]
    step4 = [s.replace('--', ' ') for s in step3]
    step45 = " ".join(step4)
    step47 = step45.split(" ")
    step5 = [s.replace('?', '') for s in step47]
    step6 = [s.replace(')', '') for s in step5]
    step7 = [s.replace('(', '') for s in step5]
    step8 = [s.lower() for s in step7]
    finalClean = [s for s in step8 if s]
    next_word_table = []
    for x in finalClean:
        next_word_table.append({x: finalClean[finalClean.index(x) - 1]})
    return next_word_table

def convertTableToFreqTable(table):
    occur = []
    for k in table:
        table2 = []
        counter = 0
        for key, value in k.items():
            if value in table2:
                counter += 1
                table2[value] = counter
            else:
                counter += 1
                table2.append({value: counter})
        print(table2)
    return occur
nexties = convertTextToNextTable(words)
frequency_table = convertTableToFreqTable(nexties)