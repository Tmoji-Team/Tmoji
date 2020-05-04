from django.shortcuts import render
# from pyspark.sql import SparkSession
import emoji
import json
from pymongo import MongoClient
import numpy as np


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        # mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        mongo_uri = 'mongodb://%s/%s' % (host, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


def q(request):
    context = {}

    # collect to mongodb
    db = _connect_mongo(host='127.0.0.1', port=27017, username='admin', password='123456', db='bigdata')
    cursor = db['q1'].find()

    # q1
    q1 = {}

    # spark = SparkSession \
    #     .builder \
    #     .appName("myApp") \
    #     .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/bigdata.q1") \
    #     .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/bigdata.q1") \
    #     .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.3.1') \
    #     .getOrCreate()
    #
    # df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
    cursor = list(cursor)
    emojis = [row['emoji'] for row in cursor]
    fres = [row['fre'] for row in cursor]

    for i in range(len(emojis)):
        q1[emoji.emojize(emojis[i])] = fres[i]
    context['q1'] = q1

    # q2
    cursor = db['q2'].find()
    cursor = list(cursor)
    emojis = [row['emoji'] for row in cursor]
    cols = [row['col'] for row in cursor]

    emojis = [':face_with_tears_of_joy:', ':red_heart:', ':loudly_crying_face:', ':fire:',
             ':smiling_face_with_heart-eyes:', ':female_sign:', ':clapping_hands:',
             ':folded_hands:', ':male_sign:', ':backhand_index_pointing_right:', 'others']
    matrix = [[0]*11]*11
    indexByName = []
    nameByIndex = []

    for emo, col in zip(emojis, cols):
        idx = emojis.index(emo)
        for val_dict in col.values():
            emo1 = val_dict['_1']
            val1 = val_dict['_2']
            matrix[idx][emojis.index(emo1)] = val1

    for i in range(len(emojis)):
        indexByName.append([emoji.emojize(emojis[i]), i])
        nameByIndex.append([i, emoji.emojize(emojis[i])])
    # print(context)
    # context['hello'] = 'hello'
    # return render(request, 'index.html', context)
    q2 = {'matrix': matrix, 'indexByName': indexByName, 'nameByIndex': nameByIndex}
    context['q2'] = q2

    # q7
    cursor = db['q7'].find()
    num = []
    counts = []
    for row in cursor:
        num.append(row['num'])
        counts.append((row['counts']))

    q7 = []
    for n, c in zip(num, counts):
        tmp = {}
        tmp['num'] = n
        tmp['counts'] = c
        q7.append(tmp)
    print(q7)

    context['q7'] = q7

    return render(request, 'index.html', {'context': json.dumps(context)})


