import re


'''TODO: true or false if mem
     : pq of highest priority instructions'''

class DAGNode:
    def __init__(self,line,consumesDict, producerDict,cost):
        RegFinder = re.compile('%(.*?) ')
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
            self.op   = [line.split('=')[1].split(' ')[1]]
            cStr      = line.split('=')[1]  
            self.consumerStr = RegFinder.findall(cStr)
            producerDict[self.prod] = self
        else:
            self.prod = "" 
            self.op   = line.split()[0] 
            self.consumerStr = RegFinder.findall(line) 
        for i in range(len(self.consumerStr)):
            consumed = self.consumerStr[i].strip(',')
            self.consumerStr[i] = consumed
            if consumed in producerDict: 
                producerDict[consumed].eatsme.append(consumed)
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
        print(costarr)
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
                j+=1
                print(j)
                if self.root is None:
                    self.root = self.memberList[0]
                
        
def dagPrint(DAG):
    root =  
    print('opcode is: ' + str(item.op))
    print('produced reg is: ' + str(item.prod))
    print('consumed registers are: ' + str(item.consumerStr))
#def dagReduce(DAG):
    
 
if __name__ == "__main__":
    t = DAG('output.ll') 
    dagPrint(t) 
