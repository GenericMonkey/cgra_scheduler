#!/usr/bin/env python3.6
from itertools import product, combinations, chain
from math import ceil
from queue import PriorityQueue
from argparse import ArgumentParser

import cfgGenerator

'''
Based on a 2 x 2 CGRA with homogeneous cores
FU0 FU1 
FU2 FU3 
'''


DIMENSION = 2
DEBUG = True
#DEBUG = False
VERBOSE = True
#VERBOSE = False



class Scheduler:
    '''
    Constructor. Takes ii and dag for thing to schedule
    '''
    def __init__(self, dag):
        self.dag = dag



    '''
    starting at MII, repeatedly tries to compute a working schedule till success
    '''
    def find_schedule(self):
        success = False
        ii = self.dag.calculate_MII(DIMENSION * DIMENSION) - 1
        while not success:
            ii += 1
            success = self.calculate_schedule(ii)
            if not success and VERBOSE:
                print ("Scheduling Failed for II: {}".format(ii))
        
        print ("Schedule Found for II: {}".format(ii))
        self.ii = ii
        self.print_schedule()


    '''
    the main logic for scheduling, given an ii
    '''
    def calculate_schedule(self, ii):
        TIME = 0
        FU_ID = 1
        OP = 2
        slot_lookup = {}
        time_slice = [None for i in range(DIMENSION * DIMENSION)]
        self.schedule = [[i for i in time_slice] for j in range(ii * ceil(len(self.dag.memberList) // ii))]
        self.printable_schedule = [[i for i in time_slice] for j in range(ii * ceil(len(self.dag.memberList) // ii))]
        insts_to_schedule = sorted([d for d in self.dag.memberList], key=lambda x: x.height(),reverse=True)
        for inst in insts_to_schedule:
            #check for parents
            if VERBOSE:
                print ("Now scheduling {} (inst {})".format(inst.op, inst.id))
            if DEBUG:
                self.print_schedule()
                input()
            if len(inst.consumes) == 0:
                #no parents. put in earliest time slot available
                time, fu_ids = self.get_earliest_slots()
                if time == None:
                    return False
                slot_lookup[inst.id] = (time, fu_ids[0], inst.op)
                self.printable_schedule[time][fu_ids[0]] = inst
                for i in range(len(self.schedule))[time % ii::ii]:
                    self.schedule[i][fu_ids[0]] = inst
            else:
                #parents exist. Find when/where they were scheduled
                #print ([i.rawLine for i in inst.consumes])
                parent_slots = [slot_lookup[i.id] for i in inst.consumes]
                #print ("Parent slots", parent_slots)
                #find the most recent parents. (compare parent_slots[0])
                #TODO: latency calculation
                latency_info = cfgGenerator.Latency()
                latest_parent_time = max([p[TIME] + latency_info.get_latency(p[OP]) - 1  for p in parent_slots])
                search_time = latest_parent_time + 1
                scheduled = False
                while not scheduled:
                    time, fu_ids = self.get_earliest_slots(start_time=search_time)
                    if time == None or time - latest_parent_time >= ii:
                        #if all slots full for II many iterations, then fail (return false)
                        if VERBOSE:
                            print("Scheduling failed due to no slots left")
                        return False
                    #find fu in closest time that can minimize travel
                    if time - latest_parent_time > 1:
                        #we can get anywhere in 2 steps, so may choose any available FU
                        #TODO: maybe make this smarter?
                        slot_lookup[inst.id] = (time, fu_ids[0], inst.op)
                        self.printable_schedule[time][fu_ids[0]] = inst
                        for i in range(len(self.schedule))[time % ii::ii]:
                            self.schedule[i][fu_ids[0]] = inst
                        scheduled = True
                    else:
                        latest_fus = [p[FU_ID] for p in parent_slots if p[TIME] + latency_info.get_latency(p[OP]) - 1 == latest_parent_time]
                        #compute max norm for routing distance
                        max_dist = [max([self.fu_dist(f, l) for l in latest_fus]) for f in fu_ids]
                        if min(max_dist) > 1:
                            #if max norm > 1, then run again with latest_time += 1
                            search_time += 1
                        else:
                            #else, pick minimal max_norm
                            fu_choice = fu_ids[max_dist.index(min(max_dist))]
                            slot_lookup[inst.id] = (time, fu_choice, inst.op)
                            self.printable_schedule[time][fu_choice] = inst
                            for i in range(len(self.schedule))[time % ii::ii]:
                                self.schedule[i][fu_choice] = inst
                            scheduled = True
                            #if single parent and curr fu not used, take that (time + 1)
        return True

    '''
    Finds the earliest time with an available FU
    '''
    def get_earliest_slots(self, start_time=0):
        for time, i in zip(self.schedule[start_time:], range(len(self.schedule))[start_time:]):
            for fu_id in range(len(time)):
                if time[fu_id] == None:
                    return i, [j for j in range(len(time)) if time[j] == None]
        return None, None

    '''
    Prints current state of schedule
    '''
    def print_schedule(self):
        print ("CGRA")
        print ('''
        | 0 | 1 |
        | 2 | 3 |
        ''')
        scheduled_insts = []
        for time in self.printable_schedule:
            for fu in time:
                if fu:
                    scheduled_insts.append(fu.rawLine)
        scheduled_insts = list(set(scheduled_insts))
        #print (scheduled_insts)
        print ("Unrolled Schedule:")
        print ('T  |0||1||2||3|')
        print ('===============')
        num_insts = 0
        for time in range(len(self.printable_schedule)):
            print('   ' + '-' * 3 * DIMENSION * DIMENSION)
            print('{}'.format(time).ljust(3),end='')
            for i in range(DIMENSION * DIMENSION):
                if self.printable_schedule[time][i]:
                    num_insts += 1
                val = self.printable_schedule[time][i].id if self.printable_schedule[time][i] else ' '
                print('|' + str(val) + '|',end='')
            print()
            if num_insts == len(self.dag.memberList):
                break
        print ("\nRolled Schedule")
        print ('T  |0||1||2||3|')
        print ('===============')
        for time in range(self.ii):
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
            return [0,3]
        elif fu_id == 2:
            return [0,3]
        elif fu_id == 3:
            return [1,2]
        else:
            return []
    
    '''
    returns manhattan distance
    '''
    def fu_dist(self, fu1, fu2):
        if fu1 == fu2:
            return 0
        if fu1 in self.neighbors(fu2):
            return 1
        return 2

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
    parser = ArgumentParser(description='specify output verbosity for scheduler')
    parser.add_argument('-v', '--verbose', 
        action='store_true',
        dest='verbose',
        help='Whether or not to turn on verbose printing')
    parser.add_argument('-d', '--debug',
        action='store_true', 
        dest='debug',
        help='Whether or not to turn on step by step debug visualizer')
    info = vars(parser.parse_args())
    DEBUG = info['debug']
    VERBOSE = info['verbose']
    dag = cfgGenerator.DAG('output.ll')
    s = Scheduler(dag)
    s.find_schedule()
    #result = s.calculate_schedule(5)
    #print("Schedule Succeeded:", result)
    #if result:
    #    s.print_schedule()
    #print(s.get_earliest_slots()) #0, [0,1,2,3] 
    #if s.schedule(2):
    #    s.print()
    #for i in combinations(range(6), 6):
    #    for j in i:
    #        print(j, end='')
    #    print()
    # print(s.combine([0.2, 0.5, 0.1, 0.4]))
    # print(s.combine([s.combine([s.combine([0.2, 0.5]), 0.1]), 0.4]))

