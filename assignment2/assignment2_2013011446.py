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

    for word in embedding:
        fout.write(word)
        fout.write(original_input[word])
        # fout.write(cluster[word])

    fin.close()
    fout.close()
    
def word2vec(embedding, threshold, sim):
    #ranks = []
    simmat = dict()
    clusters = dict()
    
    for word1 in embedding:
        a = embedding[word1]
        simrow = dict()
        for word2 in embedding:
            # build sim matrix
            if word1 == word2:
                simrow[(word2)] = 0.0
                continue
            #pair = set([word1, word2])
            b = embedding[word2]
            simrow[(word2)] = sim(a, b)
            
            #ranks.append([pair, simrow[word2]])
        simmat[(word1)] = simrow
    
    #sorted(ranks, key=lambda x: x[1])
    #reversed(ranks)

    while simmat.len() > 1:
        max_sim = 0.0
        max_a = ()
        max_b = ()
        for row in simmat:
            key_max = max(row.keys(), key=(lambda k: row[k]))
            if row[key_max] > max_sim :
                max_sim = row[key_max]
                max_a = row
                max_b = key_max

        clustered = merge_tuple(max_a, max_b)

        clusteres[clustered] = simmat[max_a][max_b]
        simrow = dict()
        for k in simrow.keys() :
            simrow[k] = min(simmat[max_a][k], simmat[max_b][k])
        simmat[clustered] = simrow

        del simmat[max_a][max_b]
        del simmat[max_b][max_a]
        del simmat[max_a]
        del simmat[max_b]
    

    return simmat

def merge_tuple(a, b):
    return tuple(sorted(list(a + b)))
    
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
