


f = open('./data/emojifydata-en/dev.txt', 'r')
w_f = open('./data/extract/dev.txt', 'w')

sentence = []
emoji = []
count = 0
place = 0
# for _ in range(100):
    # line = f.readline()
for line in f:
    line = line.replace('\n', '')
    word = line.split(' ')
    if word[0] == '<START>':
        place = 0
        continue
    if word[0] == '<STOP>':
        # print(sentence)
        # print(emoji)
        test = "".join(sentence)
        place = 0
        if test.find("^") == -1 and len(emoji) != 0:
        # if sum(not c.isalnum() for c in test) == 0:
            w_f.write(" ".join(sentence) + "^" + " ".join(emoji)+'\n')
        sentence, emoji = [], []
        count = count + 1
        if count % 1000 == 0:
            print(count)
    elif len(word) == 2:
        try:
            place += 1
            sentence.append(word[0])
            if word[1] != 'O':
                emoji.append(word[1]+','+str(place))
                sentence.append(word[1])
        except:
            continue

f.close()
w_f.close()
