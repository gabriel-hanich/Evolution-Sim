import json

def readJSON(filePath)->object:
    with open(filePath, "r", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
        return data