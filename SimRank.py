#Author: BoYu Huang
#Date: 2018/12/21
#Reference: 
import pandas as pd

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
    
def 