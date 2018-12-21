#Author: BoYu Huang
#Date: 2018/12/8

import pandas as pd
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

def HITS(totalnode, subgraph):
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
            if subgraph[item].pa != None:
                for element in subgraph[item].pa:
                    #print(element)
                    s_h = s_h + h[t-1][element]
                    #print(s_h)
                a[t][item] = s_h
            if subgraph[item].ch != None:
                for element in subgraph[item].ch:
                    s_a = s_a + a[t-1][element]
                    #print(s_a)
                h[t][item] = s_a
        for item in h[t]:
            h[t][item] = h[t][item]/sum(h[t].values())
        for item in a[t]:
            a[t][item] = a[t][item]/sum(a[t].values())
        
        v1 = list(map(lambda x: abs(x[0]-x[1]), zip(list(a[t].values()), list(a[t-1].values()))))
        v2 = list(map(lambda x: abs(x[0]-x[1]), zip(list(h[t].values()), list(h[t-1].values()))))
        a_value = sum(i**2 for i in v1)**0.5
        h_value = sum(i**2 for i in v2)**0.5
        if (a_value + h_value) < 0.0001:
            break;
    
    return h,a
    
def show_auth(authority,iteration):
    top_key = sorted(authority[iteration], key=authority[iteration].get, reverse=True)[:10]
    for key in top_key:
        print(key,": ",authority[iteration][key])

def show_hub(hub,iteration):
    top_key = sorted(hub[iteration], key=hub[iteration].get, reverse=True)[:10]
    for key in top_key:
        print(key,": ",hub[iteration][key])
        
data = pd.read_csv('graph_6.txt',header = -1)
data.columns = ['first node', 'second node']

totalnode, subgraph = creategraph(data)

start = time.time()
hub, authority = HITS(totalnode, subgraph)
end = time.time()

t6 = end - start
print("Using time: ", t6)

show_auth(hub,10)
show_auth(hub,20)

show_hub(hub,10)
show_hub(hub,20)