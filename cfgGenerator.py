import re
from math import ceil
from graphviz import Digraph





'''TODO: true or false if mem
     : pq of highest priority instructions'''

class Latency:
    def __init__(self):
        self.latency_map = {
            'mul'  : 3,
            'load' : 2
        }
    
    def get_latency(self, op):
        if op in self.latency_map:
            return self.latency_map[op]
        return 1


class DAGNode:
    def __init__(self,id,line,consumesDict, producerDict,iL=True):
        RegFinder = re.compile('%([0-9a-z\.]+)*') 
        self.id = id
        self.op = None
        self.prod = None  
        self.consumes = []
        self.consumerStr = []
        self.eatsme = []
        self.rawLine = line
        self.inLoop = iL 
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
            if self.op == 'br':
                self.consumerStr = []
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
        if self.prod in consumesDict:
            self.eatsme = consumesDict[self.prod]

    
    def height(self, visited=None):
        if not visited:
            visited = []
        if self.prod in visited: 
            return 0
        visited.append(self.prod)
        if len(self.eatsme) == 0: 
            return 0
        latency_info = Latency()
        return max([i.height(visited=visited) for i in self.eatsme]) + latency_info.get_latency(self.op)
    def addBrDep(self, depList,consumesDict,producerDict): 
        #print (depList)
        for item in depList: 
            if item.prod != "":
                self.consumerStr.append(item.prod) 
                if item.prod in producerDict:
                    producerDict[item.prod].eatsme.append(self)                    
                if item.prod in consumesDict:
                    consumesDict[item.prod].append(self)
            else:
                self.consumerStr.append(item.rawLine) 
                if item.rawLine in producerDict:
                    producerDict[item.rawLine].eatsme.append(self)                    
                else:
                    producerDict[item.rawLine] = item
                    producerDict[item.rawLine].eatsme.append(self) 
                if item.rawLine in consumesDict:
                    consumesDict[item.rawLine].append(self)
                else:
                    consumesDict[item.rawLine] = [self]
class DAG:
    def __init__(self, filename):
        f = open(filename)
        cost = open(filename.split('.')[0] +'_cost')
        costReg = re.compile('Found an estimated cost of\ (\d+)')
        costarr=[]
        allInLoop = True
        kflag = False
        loopFile = None 
        loopD = {}
        firstIL = None
        try:                                           
           loopFile = open("output.loops")
        except IOError:
            loopFile = None    
        if loopFile is None:
            pass
        else:
            allInLoop=False
            for line in loopFile: 
                loopD[line] = True 
                if firstIL is None:
                    firstIL = line
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
        id = 0
        iLFlag = False
        controlDep = []
        for line in f:
            if line == firstIL:
                iLFlag = True
            if notInKernel == True and "kernel" not in line:
                pass
            elif notInKernel == True and "kernel" in line:
                notInKernel=False
            elif notInKernel == False and "}" == line[0]:
                #print(self.consumerDict)
                break 
            if 'preds' in line:
                controlDep = []
            if 'preds' not in line and '%' in line: 
                iL = allInLoop  
                if iL == False and iLFlag == True and line in loopD:
                    iL = loopD[line] 
                self.memberList.append(DAGNode(id,line,self.consumerDict, self.producerDict, iL))  
                if self.memberList[-1].op != 'br': 
                    controlDep.append(self.memberList[-1]) 
                else:
                    self.memberList[-1].addBrDep(controlDep, self.consumerDict,self.producerDict)
                    controlDep=[]
                id += 1
                if self.root is None:
                    self.root = self.memberList[0]
        self.compress()
        self.populate()
    

    def populate(self):
        nodesToRemove = []
        for item in self.memberList:
            if item.inLoop == False:
                nodesToRemove.append(item)
        for deln in nodesToRemove:
            self.memberList.remove(deln) 
        for item in self.memberList:
            for cs in item.consumerStr:
                if cs in self.producerDict:
                    if(self.producerDict[cs] in self.memberList and self.producerDict[cs].inLoop):
                        item.consumes.append(self.producerDict[cs])

    def compress(self):
        suspects = []
        phisus   = []
        for item in self.memberList: 
            if item.op == 'sext':
                deleter=[]
                for pBr in item.eatsme:
                    if pBr.op == 'br':
                        deleter.append(pBr)
                print(deleter)
                for d in deleter:
                    item.eatsme.remove(d) 
                if len(item.eatsme) == 1: #only one thing consumes this producer; probably a fake instruction 
                    suspects.append(item)
            if item.op == 'phi':
                for child in item.eatsme:
                    if (child.op == 'add'):
                        #print (len(child.consumerStr))
                        pass                                
                    if item in child.eatsme:
                        #print (item.op)
                        phisus.append(item)
                        break
        for ps in phisus:
            for children in ps.eatsme:  
                if ps in children.eatsme:
                    ps.op = children.op
                    ps.rawLine = children.rawLine.replace(children.prod, ps.prod)
                    ps.consumerStr = []
                    children.inLoop = False
                    for gc in children.eatsme:
                        print(gc.op)
                        print(gc.consumerStr)
                        #only instruction in BB is getting deleted
                        if gc.op == 'br' and len(gc.consumerStr) == 1:
                            print(gc.rawLine)
                            gc.inLoop = False 
                    self.memberList.remove(children)
                    break





        for suspect in suspects:
            if suspect.eatsme[0].op == 'getelementptr':
                getter = suspect.eatsme[0] 
                deleter=[]
                for pBr in getter.eatsme:
                    if pBr.op == 'br':
                        deleter.append(pBr)
                for d in deleter:
                    getter.eatsme.remove(d) 
                if len(getter.eatsme) == 1 and getter.eatsme[0].op == 'load':
                    #If we get down to this chain, we have detected a chain of instr that should just be one load 
                    load = getter.eatsme[0] 
                    load.rawLine = getter.rawLine.replace('getelementptr','load')
                    load.rawLine = load.rawLine.replace(suspect.prod, suspect.consumerStr[0]) 
                    load.rawLine = load.rawLine.replace(getter.prod, load.prod) 
                    fixMe = self.producerDict[suspect.consumerStr[0]]
                    fixMe.eatsme.remove(suspect)
                    fixMe.eatsme.append(load) 
                    load.consumerStr.append(fixMe.prod)
                    load.consumerStr.remove(getter.prod)
                    for _cs in getter.consumerStr:
                        if _cs != suspect.prod:
                            load.consumerStr.append(_cs)
                    self.memberList.remove(getter)
                    self.memberList.remove(suspect) 
                elif len(getter.eatsme) == 1 and getter.eatsme[0].op == 'store':  
                    store = getter.eatsme[0]                                                                        
                    address = None 
                    for _cs in getter.consumerStr:               
                        if _cs != suspect.prod:
                            address = _cs
                    
                    fixMe = self.producerDict[suspect.consumerStr[0]]
                    fixMe.eatsme.remove(suspect)
                    fixMe.eatsme.append(store) 
                    store.rawLine = store.rawLine.replace(getter.prod, address)
                    store.rawLine = store.rawLine.replace('align', fixMe.prod+ ' align')  
                    store.consumerStr.append(fixMe.prod) 
                    store.consumerStr.append(address) 
                    store.consumerStr.remove(getter.prod) 
                    self.memberList.remove(getter)
                    self.memberList.remove(suspect) 


    def calculate_MII(self, num_FUs):
        resmii = int(ceil(len(self.memberList) / num_FUs))
        recmii = 0 #TODO FIXME
        return max(resmii, recmii)

        
def dagPrint(DAG):
    dot = Digraph(comment='DAG')
    for item in DAG.memberList:
        if item.inLoop == True:
            if item.prod == "": 
                dot.node(item.rawLine, item.rawLine)
            else:
                dot.node(item.prod, item.rawLine)
    for item in DAG.memberList: 
        for consumed in item.consumes:
            if consumed in DAG.memberList and consumed.inLoop ==True:
                if item.prod == "" and consumed.prod != "":
                    dot.edge(consumed.prod, item.rawLine)
                elif item.prod != "" and consumed.prod != "":
                    dot.edge(consumed.prod, item.prod)
                elif item.prod != "" and consumed.prod == "":
                    dot.edge(consumed.rawLine, item.prod)
                else:
                    dot.edge(consumed.rawLine, item.rawLine)
        #print([i.rawLine for i in item.eatsme])
        #print(item.rawLine)
        #print(item.consumerStr)
        #print(item.height())
    dot.render('DAGv')
    #for item in DAG.memberList:
    #    print('opcode is: ' + str(item.op))
    #    print('produced reg is: ' + str(item.prod))
    #    print('consumed registers are: ' + str(item.consumerStr))
#def dagReduce(DAG):

 


if __name__ == "__main__":
    t = DAG('output.ll') 
    dagPrint(t) 
    print ("MII:", t.calculate_MII(4))
    for node in t.memberList:
        print ("Node:", node.op, node.id, "Height:", node.height(), "inLoop: ", node.inLoop, "Parents:", [n.id for n in node.consumes])


#DFS from a DAG,
#   Start at some node-> iterate through DAG.memberList 
#   From node, DAGNode.eatsme-> List of Nodes that consume value  
#   DAG.producerDict maps produced register (string) to DAG node
#   DAG.producerDict[node.producerStr[0]] --> returns some parent node
