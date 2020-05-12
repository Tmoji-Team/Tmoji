import emoji
import json
import numpy as np
import matplotlib.pyplot as plt

from pymongo import MongoClient
from backend.emo_utils import *
from django.shortcuts import render


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        # mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        mongo_uri = 'mongodb://%s/%s' % (host, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


def sentence_to_avg(sentence, word_to_vec_map):
    words = (sentence.lower()).split()
    avg = np.zeros((50,))
    for w in words:
        avg += word_to_vec_map[w]
    avg = avg / len(words)

    return avg


def model(X, Y, word_to_vec_map, learning_rate=0.01, num_iterations=400):
    np.random.seed(1)
    # Define number of training examples
    m = Y.shape[0]  # number of training examples
    n_y = 5  # number of classes
    n_h = 50  # dimensions of the GloVe vectors

    # Initialize parameters using Xavier initialization
    W = np.random.randn(n_y, n_h) / np.sqrt(n_h)
    b = np.zeros((n_y,))

    # Convert Y to Y_onehot with n_y classes
    Y_oh = convert_to_one_hot(Y, C=n_y)
    cost = 0
    # Optimization loop
    for t in range(num_iterations):  # Loop over the number of iterations
        for i in range(m):  # Loop over the training examples
            # Average the word vectors of the words from the i'th training example
            avg = sentence_to_avg(X[i], word_to_vec_map)

            # Forward propagate the avg through the softmax layer
            z = np.dot(W, avg) + b
            a = softmax(z)

            # Compute cost using the i'th training label's one hot representation and "A" (the output of the softmax)
            cost = -np.sum(Y_oh[i] * np.log(a))

            # Compute gradients
            dz = a - Y_oh[i]
            dW = np.dot(dz.reshape(n_y, 1), avg.reshape(1, n_h))
            db = dz

            # Update parameters with Stochastic Gradient Descent
            W = W - learning_rate * dW
            b = b - learning_rate * db

        if t % 100 == 0:
            print("Epoch: " + str(t) + " --- cost = " + str(cost))
            pred = predict(X, Y, W, b, word_to_vec_map)

    return pred, W, b


def train_predict(sent):
    # predict
    X_train, Y_train = read_csv('./static/data/train_emoji.csv')
    # X_test, Y_test = read_csv('../static/data/tesss.csv')
    # maxLen = len(max(X_train, key=len).split())

    # Y_oh_train = convert_to_one_hot(Y_train, C=5)
    # print(Y_oh_train)
    # Y_oh_test = convert_to_one_hot(Y_test, C=5)
    word_to_index, index_to_word, word_to_vec_map = read_glove_vecs('./static/data/glove.6B.50d.txt')
    _, W, b = model(X_train, Y_train, word_to_vec_map)

    words = sent.lower().split()
    avg = np.zeros((50,))
    for w in words:
        avg += word_to_vec_map[w]
    avg = avg / len(words)

    Z = np.dot(W, avg) + b
    A = softmax(Z)
    label = np.argmax(A)

    return emoji.emojize(emoji_dictionary[str(label)], use_aliases=True)


def get_context():
    context = {}

    # collect to mongodb
    db = _connect_mongo(host='127.0.0.1', port=27017, username='admin', password='123456', db='bigdata')

    # q1
    q1 = []
    cursor = db['t1'].find()
    cursor = list(cursor)
    emojis = [row['emoji'] for row in cursor]
    fres = [row['fre'] for row in cursor]

    for i in range(len(emojis)):
        tmp = {
            'text': emoji.emojize(emojis[i]),
            'value': str(float(fres[i]) / 100)
        }
        # tmp[emoji.emojize(emojis[i])] = str(float(fres[i])*10000)
        q1.append(tmp)
    context['q1'] = q1

    # q2
    cursor = db['t2'].find()
    cursor = list(cursor)
    emojis_ = [row['emoji'] for row in cursor]
    cols = [row['col'] for row in cursor]

    emojis = [':face_with_tears_of_joy:', ':red_heart:', ':loudly_crying_face:', ':fire:',
              ':smiling_face_with_heart-eyes:', ':female_sign:', ':clapping_hands:',
              ':folded_hands:', ':male_sign:', ':backhand_index_pointing_right:', 'others']
    matrix = [[0] * 11] * 11
    indexByName = []
    nameByIndex = []

    for emo, col in zip(emojis_, cols):
        idx = emojis.index(emo)
        for val_dict in col.values():
            emo1 = val_dict['_1']
            val1 = val_dict['_2']
            matrix[idx][emojis.index(emo1)] = val1

    for i in range(len(emojis)):
        indexByName.append([emoji.emojize(emojis[i]), i])
        nameByIndex.append([i, emoji.emojize(emojis[i])])

    q2 = {'matrix': matrix, 'indexByName': indexByName, 'nameByIndex': nameByIndex}
    context['q2'] = q2

    # q4
    q4 = {}
    collection = db.top10Word
    collection = list(collection.find())
    q4['name'] = 'flare'
    result_children = []
    for row in collection:
        temp_dict = {}
        temp_dict['name'] = emoji.emojize(row['_1'])
        children = []
        words = row['_2']
        for i in range(len(words)):
            each_word = {}
            each_word['name'] = words[i]
            each_word['value'] = 10000
            children.append(each_word)
        temp_dict['children'] = children
        result_children.append(temp_dict)
    q4['children'] = result_children
    context['q4'] = q4

    q6 = {}
    collection = db.pairWise
    collection = list(collection.find())
    q6['nodes'] = []
    q6['links'] = []
    i = 0
    for row in collection:
        if i > 19:
            break
        node1 = {}
        node2 = {}
        link = {}
        node1['name'] = emoji.emojize(row['_1'])
        node2['name'] = row['_2'][0]['_1']['_1']
        q6['nodes'].append(node1)
        q6['nodes'].append(node2)
        link['source'] = i
        link['target'] = i + 1
        link['value'] = row['_2'][0]['_2']
        q6['links'].append(link)
        i = i + 2
    context['q6'] = q6

    # q3
    cursor = db['t3'].find()
    emojis_ = []
    uppers = []
    lowers = []
    for row in cursor:
        emojis_.append(row['emoji'])
        uppers.append(row['upper'])
        lowers.append(row['lower'])

    q3 = []
    for emo, up, lo in zip(emojis_, uppers, lowers):
        tmp = {
            'name': emoji.emojize(emo),
            'x': up / (up + lo),
            'y': lo / (lo + up)
        }
        q3.append(tmp)
    context['q3'] = q3

    # q7
    q7 = []
    cursor = db['t7'].find()
    nums = []
    counts = []
    for row in cursor:
        nums.append(row['num'])
        counts.append(row['counts'])

    for n, c in zip(nums, counts):
        tmp = {
            'name': n,
            'value': c
        }
        q7.append(tmp)
    context['q7'] = q7

    # q8
    cursor = db['t8'].find()
    emojis_ = []
    pos = []
    for row in cursor:
        emojis_.append(row['emoji'])
        pos.append(row['pos'])

    head = []
    middle = []
    tail = []
    for e, p in zip(emojis_, pos):
        tmp = {}
        tmp['name'] = emoji.emojize(e)
        tmp['value'] = 5
        if p == 0:
            head.append(tmp)
        elif p == 1:
            middle.append(tmp)
        else:
            tail.append(tmp)
    head_dict = {}
    head_dict['name'] = 'Head'
    head_dict['children'] = head
    head_dict['value'] = len(head)

    middle_dict = {}
    middle_dict['name'] = 'Middle'
    middle_dict['children'] = middle
    middle_dict['value'] = len(middle)

    tail_dict = {}
    tail_dict['name'] = 'Tail'
    tail_dict['children'] = tail
    tail_dict['value'] = len(tail)

    context['q8'] = {'children': [head_dict, middle_dict, tail_dict], 'value': 5}

    # q9
    cursor = db['t9'].find()
    x = []
    y = []
    num = []
    for row in cursor:
        x.append(row['sent_len'])
        y.append(row['emoji_len'])
        num.append(row['count'])

    q9 = []
    for x_, y_, num_ in zip(x, y, num):
        tmp = {}
        tmp['x'] = x_
        tmp['y'] = y_
        tmp['num'] = num_
        q9.append(tmp)
    context['q9'] = q9
    print(q9)

    # q10
    cursor = db['t10'].find()
    emojis_ = []
    counts = []
    for row in cursor:
        emojis_.append(row['emoji'])
        counts.append(row['count'])

    q10 = []
    for e, c in zip(emojis_, counts):
        tmp = {}
        tmp['name'] = emoji.emojize(e)
        tmp['value'] = c
        q10.append(tmp)
    context['q10'] = q10

    # q11
    cursor = db['t11'].find()
    emojis_ = []
    ave_lens = []
    for row in cursor:
        emojis_.append(row['emoji'])
        ave_lens.append((row['ave_len']))

    q11 = []
    for n, c in zip(emojis_, ave_lens):
        tmp = {}
        tmp['Country'] = emoji.emojize(n)
        tmp['Value'] = c
        q11.append(tmp)

    context['q11'] = q11
    return context


def q(request):

    context = get_context()
    # sent = "i love you"
    # result = train_predict(sent)
    # print(result)
    context['result_sent'] = ""

    return render(request, 'index.html', {'context': json.dumps(context)})


def get_emoji(request):
    sent = request.GET.get('input')
    result = train_predict(sent)
    context = get_context()
    context['result_sent'] = sent + " " + result

    return render(request, 'index.html', {'context': json.dumps(context)})