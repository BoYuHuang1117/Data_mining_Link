#Author: BoYu Huang
#Date: 2018/12/10
#Reference: http://jpndbs.lib.ntu.edu.tw/DB/PageRank.pdf?fbclid=IwAR3z4Sd8znuBezG-q5pTXlAdmtKmLWIDMRq6evNzfFSEjAJ9i3zjUAB8tj8
import pandas as pd

class Link:
    def __init__(self, name):
        self.item = name
        self.ch = None
        self.pa = None
        
    def add_ch(self,ch_list):
        self.ch = ch_list
        #print(self.ch)
        
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

def PageRank(subgraph,totalnode, d = 0.15):
    PR = {}
    PR[0] = {}
    
    for item in totalnode:
        PR[0][item] = 1/len(totalnode)
    
    for i in range(1,100):
        print('Number of Iteration:',i)
        PR[i] = {}
        for item in subgraph:
            s = 0
            if subgraph[item].pa != None:
                for parent in subgraph[item].pa:
                    count = len(subgraph[parent].ch)
                    s = s + PR[i-1][parent]/count
            PR[i][item] = d/len(totalnode) + (1-d) * s
        v1 = list(map(lambda x: abs(x[0]-x[1]), zip(list(PR[i].values()), list(PR[i-1].values()))))
        abs_value = sum(j**2 for j in v1)**0.5
        if abs_value < 0.0001:
            print('Number of Iteration:',i)
            break; 
    return PR
    
def show_PR(PR,iteration):
    top_key = sorted(PR[iteration], key=PR[iteration].get, reverse=True)[:10]
    for key in top_key:
        print(key,": ", PR[iteration][key])
        
data = pd.read_csv('graph_6.txt',header = -1)
data.columns = ['first node', 'second node']

totalnode, subgraph = creategraph(data)

start = time.time()
PR = PageRank(subgraph, totalnode)
end = time.time()

t6 = end -start
print("Using time: ", t6)

show_PR(PR,10)
show_PR(PR,20)