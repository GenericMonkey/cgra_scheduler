from itertools import product, combinations, chain
from math import ceil
from queue import PriorityQueue

import cfgGenerator
'''
Based on a 3 x 3 CGRA with 3 memory FUs
MFU0 FU1 FU2
MFU3 FU4 FU5
MFU6 FU7 FU8
'''


DIMENSION = 2


class Inst:
    def __init__(self, dagNode=None):
        if dagNode:
            self.id = dagNode.prod
            self.node = dagNode
        else:
            self.id = None
            self.node = None

class Scheduler:
    '''
    Constructor. Takes ii and dag for thing to schedule
    '''
    def __init__(self, dag):
        self.dag = dag

    '''
    the main logic for scheduling
    '''
    def schedule(self, ii):
        time_slice = [Inst() for i in range(DIMENSION * DIMENSION)]
        #TODO make dag output numops
        self.schedule = [[i for i in time_slice] for j in range(ii * ceil(len(self.dag.memberList) // ii))]
        insts_to_schedule = sorted([Inst(d) for d in self.dag.memberList], key=lambda x: x.node.height(visited=[]),reverse=True)
        print ([x.node.op for x in insts_to_schedule])
        return True

    '''
    Prints current state of schedule
    #TODO: Nice way to display inst if scheduled
    '''
    def print(self):
        print ("CGRA")
        print ('''
        | 0 | 1 |
        | 2 | 3 |
        ''')
        print ('T  |0||1||2||3|')
        for time in range(len(self.schedule)):
            print('   ' + '-' * 3 * DIMENSION * DIMENSION)
            print('{}'.format(time).ljust(3),end='')
            for i in range(DIMENSION * DIMENSION):
                val = self.schedule[time][i].id if self.schedule[time][i].id else ' '
                print('|' + val + '|',end='')
            print()
    '''
    returns the list of FU neighbors. Useful for route searching
    '''
    def neighbors(self, fu_id):
        if fu_id == 0:
            return [1,2]
        elif fu_id == 1:
            return [2,3]
        elif fu_id == 2:
            return [0,3]
        elif fu_id == 3:
            return [1,2]
        else:
            return []

    def top_down(self):
        self.chainlists = []
        visited = {}
        for node in self.dag.memberList:
            new_chain_candidate = node.prod not in visited
            if new_chain_candidate:
                for parent in node.consumes:
                    if parent.prod not in visited:
                        new_chain_candidate = False
            if len(node.consumes) == 0 or new_chain_candidate:
                cl = [node.prod]
                visited[node.prod] = True
                candidate_children = [c for c in node.eatsme if c.prod not in visited]
                while len(candidate_children) != 0:
                    to_add = candidate_children[0]
                    if to_add.op == 'br':
                        cl.append(to_add.prod)
                    visited[to_add.prod] = True
                    candidate_children = [c for c in to_add.eatsme if c.prod not in visited]
                self.chainlists.append(cl)
        print(self.chainlists)








if __name__ == '__main__':
    dag = cfgGenerator.DAG('output.ll')
    s = Scheduler(dag)
    s.schedule(4)
    #if s.schedule(2):
    #    s.print()
    #for i in combinations(range(6), 6):
    #    for j in i:
    #        print(j, end='')
    #    print()
    # print(s.combine([0.2, 0.5, 0.1, 0.4]))
    # print(s.combine([s.combine([s.combine([0.2, 0.5]), 0.1]), 0.4]))

