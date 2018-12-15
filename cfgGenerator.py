import re
from graphviz import Digraph

'''TODO: true or false if mem
     : pq of highest priority instructions'''

class DAGNode:
    def __init__(self,line,consumesDict, producerDict,cost):
        RegFinder = re.compile('%([0-9a-z\.]+)*') 
        self.op = None
        self.prod = None 
        self.consumes = []
        self.consumerStr = []
        self.eatsme = []
        self.rawLine = line
        self.cost=cost
        self.height=0 #TODO: calculate height
        if '=' in line: 
            self.prod = RegFinder.findall(line.split('=')[0])[-1] 
            self.op   = line.split('=')[1].split(' ')[1]
            cStr      = line.split('=')[1]  
            self.consumerStr = RegFinder.findall(cStr)
            producerDict[self.prod] = self
        else:
            self.prod = "" 
            self.op   = line.split()[0] 
            self.consumerStr = RegFinder.findall(line) 
        if 'store' in self.op:
            pass
            #print(self.rawLine)
            #print(self.consumerStr)
        for i in range(len(self.consumerStr)):
            consumed = self.consumerStr[i].strip(',')
            self.consumerStr[i] = consumed
            if consumed in producerDict: 
                producerDict[consumed].eatsme.append(self)
            if consumed in consumesDict:
                consumesDict[consumed].append(self)
            else:
                consumesDict[consumed] = [self]
        
         
            


class DAG:
    def __init__(self, filename):
        f = open(filename)
        cost = open(filename.split('.')[0] +'_cost')
        costReg = re.compile('Found an estimated cost of\ (\d+)')
        costarr=[]
        kflag = False
        for line in cost:
            if kflag == True and 'for function' in line:
                break 
            if kflag == False and 'kernel' not in line:
                pass
            elif 'kernel' in line:
                kflag = True
            else:
                intermediate=costReg.findall(line)
                #print(intermediate)
                val = int(intermediate[-1]) 
                costarr.append(val)
        #print(costarr)
        notInKernel = True
        self.memberList = []
        # Maps SSA assignment to Node 
        self.consumerDict = {}
        self.producerDict = {}
        self.root =  None
        j = 0
        for line in f:
            if notInKernel == True and "kernel" not in line:
                pass
            elif notInKernel == True and "kernel" in line:
                notInKernel=False
            elif notInKernel == False and "}" == line[0]:
                #print(self.consumerDict)
                return 
            if '<label>' not in line and '%' in line: 
                self.memberList.append(DAGNode(line,self.consumerDict, self.producerDict,costarr[j]))  
                #print(j)
                if self.root is None:
                    self.root = self.memberList[0] 
    def dagPop(self):
        for item in self.memberList:
            for cs in item.consumerStr:
                if cs in self.producerDict:
                    item.consumes.append(self.producerDict[cs])
        
def dagPrint(DAG):
    dot = Digraph(comment='DAG')
    for item in DAG.memberList:
        if item.prod == "": 
            dot.node(item.rawLine, item.rawLine)
        else:
            dot.node(item.prod, item.rawLine)
    for item in DAG.memberList: 
        for consumed in item.consumerStr:
            if consumed == "":
                pass 
            elif item.prod == "":
                dot.edge(consumed, item.rawLine)
            else:
                dot.edge(consumed, item.prod)
        print(item.consumes)
        print(item.consumerStr)
    dot.render('DAGv')
    #for item in DAG.memberList:
    #    print('opcode is: ' + str(item.op))
    #    print('produced reg is: ' + str(item.prod))
    #    print('consumed registers are: ' + str(item.consumerStr))
#def dagReduce(DAG):

def dagCompress(DAG):
    suspects = []
    for item in DAG.memberList: 
        if item.op == 'sext':
            if len(item.eatsme) == 1: #only one thing consumes this producer; probably a fake instruction 
                suspects.append(item)
    for suspect in suspects:
        if suspect.eatsme[0].op == 'getelementptr':
            getter = suspect.eatsme[0]
            if len(getter.eatsme) == 1 and getter.eatsme[0].op == 'load':
                #If we get down to this chain, we have detected a chain of instr that should just be one load 
                load = getter.eatsme[0] 
                load.rawLine = getter.rawLine.replace('getelementptr','load')
                load.rawLine = load.rawLine.replace(suspect.prod, suspect.consumerStr[0]) 
                load.rawLine = load.rawLine.replace(getter.prod, load.prod) 
                fixMe = DAG.producerDict[suspect.consumerStr[0]]
                fixMe.eatsme.remove(suspect)
                fixMe.eatsme.append(load) 
                load.consumerStr.append(fixMe.prod)
                DAG.memberList.remove(getter)
                DAG.memberList.remove(suspect)                
    return DAG            
 


if __name__ == "__main__":
    t = DAG('output.ll')  
    t = dagCompress(t)
    t.dagPop()
    dagPrint(t) 


#DFS from a DAG,
#   Start at some node-> iterate through DAG.memberList 
#   From node, DAGNode.eatsme-> List of Nodes that consume value  
#   DAG.producerDict maps produced register (string) to DAG node
#   DAG.producerDict[node.producerStr[0]] --> returns some parent node
