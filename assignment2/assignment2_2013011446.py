import math

out = open('test.txt', 'w')

def main():
    fin = open('WordEmbedding.txt', 'r')
    fout = open('WordClustering.txt', 'w')
    embedding = dict()
    original_input = dict()

    while True:
        word = fin.readline()
        word = word.rstrip()
        if not word: break
        vector = fin.readline()
        embedding[word] = vector.split(',')
        original_input[word] = vector

    simmat = word2vec(embedding, 0.5, cosine_sim)

    for word1 in embedding:
        for word2 in embedding:
            print(simmat[word1])

    for word in embedding:
        fout.write(word)
        fout.write(original_input[word])
        # fout.write(cluster[word])

    fin.close()
    fout.close()
    
def word2vec(embedding, threshold, sim):
    ranks = []
    simmat = dict()
    
    for word1 in embedding:
        a = embedding[word1]
        simrow = dict()
        for word2 in embedding:
            # build sim matrix
            if word1 == word2:
                simrow[word2] = 0.0
                continue
            pair = set([word1, word2])
            b = embedding[word2]
            simrow[word2] = sim(a, b)
            
            ranks.append([pair, simrow[word2]])
        simmat[word1] = simrow
    
    sorted(ranks, key=lambda x: x[1])
    reversed(ranks)
    print(ranks)
    out.close()
    return simmat

    
def cosine_sim(a, b):
    return dot(a, b) / (norm(a) * norm(b))

def euclidean_sim(a, b):
    ret = 0
    for index, elem in enumerate(a):
        ret += pow(a[index] - b[index], 2)
    return math.sqrt(ret)

# For vector math
def dot(a, b):
    ret = 0
    for aelem, belem in zip(a, b):
        ret += float(aelem) * float(belem)
    return ret

def norm(a):
    ret = 0
    for elem in a:
        ret += pow(float(elem), 2)
    return math.sqrt(ret)
