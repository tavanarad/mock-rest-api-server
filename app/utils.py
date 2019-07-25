from math import floor
import json

def find(data, key, value):
    return [x for x in data if str(x.get(key, None)) == str(value)]

def findIndex(data, key, value):
    return next((i for i, x in enumerate(data) if str(x.get(key, None)) == str(value)), -1)

def getData():
    data = [];

    with open('db.json') as f:
        data = json.load(f)

    return data;

def writeData(data):
    with open('db.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
