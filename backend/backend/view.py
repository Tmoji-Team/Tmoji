from django.shortcuts import render
# from pyspark.sql import SparkSession
import emoji
import json
from pymongo import MongoClient


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
        context[emoji.emojize(emojis[i])] = fres[i]
    # spark.stop()

    # q2
    # spark = SparkSession \
    #     .builder \
    #     .appName("myApp") \
    #     .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/bigdata.q2") \
    #     .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/bigdata.q2") \
    #     .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.3.1') \
    #     .getOrCreate()
    # df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
    cursor = db['q2'].find()
    cursor = list(cursor)
    emojis = [row['emoji'] for row in cursor]
    cols = [row['col'] for row in cursor]

    print(cols)
    # print(context)
    # context['hello'] = 'hello'
    # return render(request, 'index.html', context)

    return render(request, 'index.html', {'context': json.dumps(context)})


