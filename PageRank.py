#Author: BoYu Huang
#Date: 2018/12/10
#Reference: http://jpndbs.lib.ntu.edu.tw/DB/PageRank.pdf?fbclid=IwAR3z4Sd8znuBezG-q5pTXlAdmtKmLWIDMRq6evNzfFSEjAJ9i3zjUAB8tj8
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

def PageRank(subgraph,totalnode, d = 0.15):
    PR = {}
    PR[0] = {}
    
    for item in totalnode:
        PR[0][item] = 1/len(totalnode)
    
    for i in range(1,10):
        print('Number of Iteration:',i)
        PR[i] = {}
        for item in subgraph:
            s = 0
            for parent in subgraph[item].pa:
                count = len(subgraph[parent].ch)
                s = s + PR[i-1][parent]/count
            PR[i][item] = d/len(totalnode) + (1-d) * s
    return PR