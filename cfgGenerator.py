import re



class DAGNode:
    def __init__(self,line,consumesDict, producerDict):
        RegFinder = re.compile('%(.*?) ')
        self.op = None
        self.prod = None 
        self.consumes = []
        self.consumerStr = []
        self.eatsme = []
        self.rawLine = line
        if '=' in line:
            print(line)
            self.prod = RegFinder.findall(line.split('=')[0])[0]
            print(self.prod)
            self.op   = line.split('=')[1].split(' ')[0]
            cStr      = line.split('=')[1]  
            self.consumerStr = RegFinder.findall(cStr)
            producerDict[self.prod] = self
        else:
            self.prod = "" 
            self.op   = line.split()[0] 
            self.consumerStr = RegFinder.findall(line) 
        for consumed in self.consumerStr:
            if consumed in producerDict: 
                producerDict[consumed].eatsme.append(consumed)
            if consumed in consumesDict:
                consumesDict[consumed].append(self)
            else:
                consumesDict[consumed] = [self]
            
            


class DAG:
    def __init__(self, filename):
        f = open(filename)
        notInKernel = True
        self.memberList = []
        # Maps SSA assignment to Node 
        self.consumerDict = {}
        self.producerDict = {}
        self.root =  None
        for line in f:
            if notInKernel == True and "kernel" not in line:
                pass
            elif notInKernel == True and "kernel" in line:
                notInKernel=False
            elif notInKernel == False and "}" == line[0]:
                print(self.consumerDict)
                return 
            if '<label>' not in line and '%' in line:
                self.memberList.append(DAGNode(line,self.consumerDict, self.producerDict)) 
                if self.root is None:
                    self.root = self.memberList[0]
        


if __name__ == "__main__":
    DAG('output.ll') 
