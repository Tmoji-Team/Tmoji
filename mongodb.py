from pymongo import MongoClient
from pprint import pprint
from random import randint


client = MongoClient(host='127.0.0.1',
                     port=27017, 
                     username='admin', 
                     password='123456',
                    authSource="admin")
db = client['bigdata']

f = open('./data/extract/train.txt', 'r')
count = 0
sentences =[]
for line in f:
    words = line.split('^')
    emoji = words[1].replace('\n', '')
    sentence = {
        'sentence' : words[0],
        'emoji' : emoji
    }
    sentences.append(sentence)
    # result = db.raw.insert_one(sentence)
    count += 1
    if count % 10000 == 0:
        print(count)
        _ = db.raw.insert_many(sentences)
        sentences = []
#Step 5: Tell us that you are done
print('finished')