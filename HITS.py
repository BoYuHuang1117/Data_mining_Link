#Author: BoYu Huang
#Date: 2018/12/8

import pandas as pd

data = pd.read_csv('graph_4.txt',header = -1)
data.columns = ['first node', 'second node']

class Link:
    def __init__(self, name):
        self.item = name
        self.ch = None
        self.pa = None
        
    def add_ch(self,ch_list):
        self.ch = ch_list
        print(self.ch)
        
    def add_pa(self,pa_list):
        self.pa = pa_list
        
    def pr(self):
        print(self.item)
        print(self.ch)
        print(self.pa)

totalnode = []
subgraph = {}

for item in data['first node']:
    print(item)
    if item not in totalnode:
        subgraph[item] = Link(item)
        totalnode.append(item)
        subgraph[item].add_ch(list(data['second node'][data['first node']==item]))
    
for item in data['second node']:
    print(item)
    if item not in totalnode:
        subgraph[item] = Link(item)
        totalnode.append(item)
    subgraph[item].add_pa(list(data['first node'][data['second node']==item]))

a0 = {}
h0 = {}

for item in totalnode:
    a0[item] = 1
    h0[item] = 1
    
a = {}
h = {}
a[0] = a0;
h[0] = h0;

for t in range(1,20):
    print('Number of Iteration:',t)
    h[t] = {}
    a[t] = {}
    for item in totalnode:
        #print(item)
        s_h = 0 # sum of the previous parent hub value 
        s_a = 0 # sum of the previous children authority value
        for element in subgraph[item].pa:
            #print(element)
            s_h = s_h + h[t-1][element]
            #print(s_h)
        a[t][item] = s_h
        
        for element in subgraph[item].ch:
            s_a = s_a + a[t-1][element]
            #print(s_a)
        h[t][item] = s_a
    for item in h[t]:
        h[t][item] = h[t][item]/sum(h[t].values())
    for item in a[t]:
        a[t][item] = a[t][item]/sum(a[t].values())