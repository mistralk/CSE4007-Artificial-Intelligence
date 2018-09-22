import math

clusters = dict()
topics = dict()
wordnum = dict()
global_num = 0

def main():
    fin = open('WordEmbedding.txt', 'r')
    fout = open('WordClustering.txt', 'w')
    ftopic = open('WordTopic.txt', 'r')
    embedding = dict()
    original_input = dict()

    while True:
        word = fin.readline()
        word = word.rstrip()
        if not word: break
        vector = fin.readline()
        embedding[word] = vector.split(',')
        original_input[word] = vector

    while True:
        topic = ftopic.readline()
        topic = topic.rstrip()
        if not topic: break
        if topic.count('[') == 1:
            topic = topic.lstrip('[')
            topic = topic.rstrip(']')
            while True:
                word = ftopic.readline()
                word = word.rstrip()
                if not word: break
                topics[word.lower()] = topic

    print("Cosine Sim")
    root = word2vec(embedding, cosine_sim)
    print("\nthreshold: 0.8")
    traverse(root, 0.8)
    print("\nthreshold: 0.6")
    traverse(root, 0.6)
    print("\nthreshold: 0.4")
    traverse(root, 0.4)
    print("\nthreshold: 0.2")
    traverse(root, 0.2)
    
    for word in embedding:
        fout.write(word)
        fout.write(original_input[word])
        fout.write(wordnum[word])

    fin.close()
    fout.close()
    ftopic.close()

def entropy(cluster):
    ret = 0
    cnt = dict()
    for topic in topics.values():
        cnt[topic] = 0
    for word in cluster:
        cnt[topics[word]] += 1

    for topic in topics.values():
        if cnt[topic] != 0:
            ret += -cnt[topic] / len(cluster) * math.log2(cnt[topic] / len(cluster))
    return ret

def word2vec(embedding, sim):
    simmat = dict()

    number = 1
    print("Making Sim Matrix...")
    for word1 in embedding:
        a = embedding[word1]
        simrow = dict()
        for word2 in embedding:
            if word1 == word2:
                simrow[(word2,)] = float("-inf")
                continue
            b = embedding[word2]
            simrow[(word2,)] = sim(a, b)
            
        simmat[(word1,)] = simrow

        node = Node((word1,), None, None, 1.0, number)
        number+=1
        clusters[(word1,)] = node
        print("*", end="")
        
    print("\nClustering...")

    root = None
    while len(simmat) > 1:
        max_sim = float("-inf")
        
        max_a = ()
        max_b = ()
        for row in simmat.keys():
            key_max = max(simmat[row].keys(), key=(lambda k: simmat[row][k]))
            if simmat[row][key_max] > max_sim:
                max_sim = simmat[row][key_max]
                max_a = row
                max_b = key_max
        
        clustered = merge_tuple(max_a, max_b)

        node = Node(clustered, max_a, max_b, simmat[max_a][max_b], clusters[max_a].num)
        clusters[clustered] = node
        
        simrow = dict()
        for k in simmat.keys() :
            simrow[k] = min(simmat[max_a][k], simmat[max_b][k])
            simmat[k][clustered] = min(simmat[k][max_a], simmat[k][max_b])
        simrow[clustered] = float("-inf")
        simmat[clustered] = simrow

        for k in simmat.keys() :
            del simmat[k][max_b]
            del simmat[k][max_a]
        del simmat[max_a]
        del simmat[max_b]
        root = node
        
    return root

class Node(object):
    def __init__(self, me, left, right, sim, num):
        self.me = me
        self.left = left
        self.right = right
        self.sim = sim
        self.num = num

def traverse(node, threshold):
    if node.sim > threshold:
        print("entropy of cluster:",entropy(node.me))
        print(node.me)
        return
    if node.left != None:
        traverse(clusters[node.left], threshold)
    if node.right != None:
        traverse(clusters[node.right], threshold)

def merge_tuple(a, b):
    return tuple(sorted(a + b))
    
def cosine_sim(a, b):
    return dot(a, b) / (norm(a) * norm(b))

def euclidean_sim(a, b):
    ret = 0
    for aelem, belem in zip(a, b):
        ret += pow(float(aelem) - float(belem), 2)
    return math.sqrt(ret)

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
