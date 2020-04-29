from django.shortcuts import render
from pyspark.sql import SparkSession
import emoji
import json

def q1(request):
    spark = SparkSession \
        .builder \
        .appName("myApp") \
        .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/bigdata.q1") \
        .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/bigdata.q1") \
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.3.1') \
        .getOrCreate()

    df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
    emojis = [row.emoji for row in df.collect()]
    fres = [row.fre for row in df.collect()]
    context = {}
    for i in range(len(emojis)):
        context[emoji.emojize(emojis[i])] = fres[i]

    # context['hello'] = 'hello'
    # return render(request, 'index.html', context)
    return render(request, 'index.html', {'context': json.dumps(context)})
