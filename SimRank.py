#Author: BoYu Huang
#Date: 2018/12/21
#Reference: https://github.com/chihsuan/link-analysis
import pandas as pd
import numpy as np 
import itertools 
import time 

class Link:
    def __init__(self, name):
        self.item = name
        self.ch = None
        self.pa = None
        
    def add_ch(self,ch_list):
        self.ch = ch_list
        
    def add_pa(self,pa_list):
        self.pa = pa_list
        
    def pr(self):
        print(self.item)
        print(self.ch)
        print(self.pa)

def creategraph(data):
    totalnode = []
    subgraph = {}

    for item in data['first node']:
        #print(item)
        if item not in totalnode:
            subgraph[item] = Link(item)
            totalnode.append(item)
            subgraph[item].add_ch(list(data['second node'][data['first node']==item]))
        
    for item in data['second node']:
        #print(item)
        if item not in totalnode:
            subgraph[item] = Link(item)
            totalnode.append(item)
        subgraph[item].add_pa(list(data['first node'][data['second node']==item]))
    
    return totalnode, subgraph
    
def SimRank(subgraph,totalnode, C=0.9, iteration=10):
    sim = np.identity(len(totalnode))
    old_sim = np.zeros(len(totalnode))
    for itr in range(int(iteration)):
        old_sim = np.copy(sim)
        for a, b in itertools.product(totalnode, totalnode):
            if a is b or subgraph[a].pa == None or subgraph[b].pa == None:
                continue
            s_ab = 0
            for na in subgraph[a].pa:
                for nb in subgraph[b].pa:
                    s_ab += old_sim[int(na)-1][int(nb)-1]
            sim[int(a)-1][int(b)-1] =  s_ab * C / (len(subgraph[a].pa) * len(subgraph[b].pa))

    return sim

data = pd.read_csv('example.txt',header = -1)
data.columns = ['first node', 'second node']

totalnode, subgraph = creategraph(data)

start = time.time()
sim = SimRank(subgraph, totalnode)
end = time.time()

t1 = end - start
print("Using time: ", t1)