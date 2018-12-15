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



class Scheduler:
    '''
    Constructor. Takes ii and dag for thing to schedule
    '''
    def __init__(self, dag):
        self.dag = dag


    '''
    Finds the earliest time with an available FU
    '''
    def get_earliest_slots(self, start_time=0):
        for time, i in zip(self.schedule, range(len(self.schedule)))[start_time:]:
            for fu_id in range(len(time)):
                if not time[fu_id]:
                    return i, [j for j in range(len(time)) if not time[j]]
        raise Exception("No slots available")

    '''
    the main logic for scheduling
    '''
    def schedule(self, ii):
        TIME = 0
        FU_ID = 1
        slot_lookup = {}
        time_slice = [None for i in range(DIMENSION * DIMENSION)]
        self.schedule = [[i for i in time_slice] for j in range(ii * ceil(len(self.dag.memberList) // ii))]
        insts_to_schedule = sorted([d for d in self.dag.memberList], key=lambda x: x.height(visited=[]),reverse=True)
        print ([x.id for x in insts_to_schedule])
        for inst in insts_to_schedule:
            #check for parents
            if len(inst.consumes) == 0:
                #no parents. put in earliest time slot available
                time, fu_ids = self.get_earliest_slots()
                slot_lookup[inst.id] = (time, fu_ids[0])
                for i in range(len(self.schedule))[time::ii]:
                    self.schedule[i][fu_ids[0]] = inst
            else:
                #parents exist. Find when/where they were scheduled
                parent_slots = [slot_lookup[i.id] for i in inst.consumes]
                #find the most recent parents. (compare parent_slots[0])
                latest_time = max([p[TIME] for p in parent_slots])
                scheduled = False
                while not scheduled:
                    time, fu_ids = self.get_earliest_slots(start_time=latest_time + 1)
                    if time - latest_time >= ii:
                        print("Scheduling failed due to no slots left")
                        return False
                    #find fu in closest time that can minimize travel
                    if time - latest_time > 1:
                        #we can get anywhere in 2 steps, so may choose any available FU
                        #TODO: maybe make this smarter?
                        slot_lookup[inst.id] = (time, fu_ids[0])
                        for i in range(len(self.schedule))[time::ii]:
                            self.schedule[i][fu_ids[0]] = inst
                    else:
                        latest_fus = [p[FU_ID] for p in parent_slots if p[TIME] == latest_time]
    
    
                #if single parent and curr fu not used, take that (time + 1)
                #if all slots full for II many iterations, then fail (return false)
                pass
        return True


    '''
    Prints current state of schedule
    #TODO: Nice way to display inst if scheduled
    '''
    def print_schedule(self):
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
                val = self.schedule[time][i].id if self.schedule[time][i] else ' '
                print('|' + str(val) + '|',end='')
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
    s.print_schedule()
    print(s.get_earliest_slots()) #0, [0,1,2,3] 
    #if s.schedule(2):
    #    s.print()
    #for i in combinations(range(6), 6):
    #    for j in i:
    #        print(j, end='')
    #    print()
    # print(s.combine([0.2, 0.5, 0.1, 0.4]))
    # print(s.combine([s.combine([s.combine([0.2, 0.5]), 0.1]), 0.4]))

