#!/usr/bin/env python3.6
from itertools import product
from math import ceil
from queue import PriorityQueue
from argparse import ArgumentParser

import cfgGenerator

'''
Based on a 2 x 2 CGRA with homogeneous cores
FU0 FU1 
FU2 FU3 
'''


DEBUG = True
#DEBUG = False
VERBOSE = True
#VERBOSE = False

'''
The CGRA class represents a square mesh many-core CGRA
'''
class CGRA:
    '''
    Constructor.
    '''
    def __init__(self, dimension):
        self.dimension = dimension

    
    '''
    returns manhattan distance on dim X dim grid
    '''
    def fu_dist(self, fu1, fu2):

        row_fu1, col_fu1 = fu1 // self.dimension, fu1 % self.dimension
        row_fu2, col_fu2 = fu2 // self.dimension, fu2 % self.dimension
        return abs(row_fu1 - row_fu2) + abs(col_fu1 - col_fu2)
    
    '''
    pretty prints the cgra layout
    '''
    def print_cgra(self):
        print ("CGRA Layout")
        for i in range(self.dimension):
            for j in range(self.dimension):
                print('| {} |'.format(self.dimension * i + j), end='')
            print()


class Scheduler:
    '''
    Constructor. Takes ii and dag for thing to schedule
    '''
    def __init__(self, dag, cgra):
        self.dag = dag
        self.cgra = cgra
        self.ii = -1



    '''
    starting at MII, repeatedly tries to compute a working schedule till success
    '''
    def find_schedule(self):
        success = False
        ii = self.dag.calculate_MII(self.cgra.dimension ** 2) - 1
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
        time_slice = [None for i in range(self.cgra.dimension ** 2)]
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
                parent_slots = [slot_lookup[i.id] for i in inst.consumes]
                #find the most recent parents. (compare parent_slots[0])
                latency_info = cfgGenerator.Latency()
                latest_parent_time = max([p[TIME] + latency_info.get_latency(p[OP]) - 1  for p in parent_slots])
                latest_fus = [p[FU_ID] for p in parent_slots if p[TIME] + latency_info.get_latency(p[OP]) - 1 == latest_parent_time]
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
                    #compute max norm for routing distance
                    max_dist = [max([self.cgra.fu_dist(f, l) for l in latest_fus]) for f in fu_ids]
                    if time - latest_parent_time >= 2 * (self.cgra.dimension - 1):
                        #we can get anywhere in 2(DIM - 1)steps, so may choose any available FU
                        slot_lookup[inst.id] = (time, fu_ids[0], inst.op)
                        self.printable_schedule[time][fu_ids[0]] = inst
                        for i in range(len(self.schedule))[time % ii::ii]:
                            self.schedule[i][fu_ids[0]] = inst
                        scheduled = True
                    else:
                        if min(max_dist) > time - latest_parent_time:
                            #if max norm can't be reached in time, then run again with search_time += 1
                            search_time += 1
                        else:
                            #else, pick minimal max_norm
                            fu_choice = fu_ids[max_dist.index(min(max_dist))]
                            slot_lookup[inst.id] = (time, fu_choice, inst.op)
                            self.printable_schedule[time][fu_choice] = inst
                            for i in range(len(self.schedule))[time % ii::ii]:
                                self.schedule[i][fu_choice] = inst
                            scheduled = True
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
        self.cgra.print_cgra()
        scheduled_insts = []
        for time in self.printable_schedule:
            for fu in time:
                if fu:
                    scheduled_insts.append(fu.rawLine)
        scheduled_insts = list(set(scheduled_insts))
        #print (scheduled_insts)
        print ("Unrolled Schedule:")
        print ('T ',end='')
        for i in range(self.cgra.dimension ** 2):
            print('|{}|'.format(i),end='')
        print('\n==',end='')
        for i in range(self.cgra.dimension ** 2):
            print('===',end='')
        print()
        num_insts = 0
        for time in range(len(self.printable_schedule)):
            print('   ' + '-' * 3 * (self.cgra.dimension ** 2))
            print('{}'.format(time).ljust(3),end='')
            for i in range(self.cgra.dimension ** 2):
                if self.printable_schedule[time][i]:
                    num_insts += 1
                val = self.printable_schedule[time][i].id if self.printable_schedule[time][i] else ' '
                if DEBUG:
                    val = self.schedule[time][i].id if self.schedule[time][i] else ' '
                print('|{}|'.format(val),end='')
            print()
            if num_insts == len(self.dag.memberList):
                break
        if self.ii == -1:
            return
        print ("\nRolled Schedule")
        print ('T ',end='')
        for i in range(self.cgra.dimension ** 2):
            print('|{}|'.format(i),end='')
        print('\n==',end='')
        for i in range(self.cgra.dimension ** 2):
            print('===',end='')
        print()
        for time in range(self.ii):
            print('   ' + '-' * 3 * (self.cgra.dimension ** 2))
            print('{}'.format(time).ljust(3),end='')
            for i in range(self.cgra.dimension ** 2):
                val = self.schedule[time][i].id if self.schedule[time][i] else ' '
                print('|{}|'.format(val),end='')
            print()

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
    cgra = CGRA(2)
    s = Scheduler(dag, cgra)
    s.find_schedule()
    #c = CGRA(3)
    #for i,j in product(range(9),range(9)):
    #    print ("Dist between {} and {} is {}".format(i,j,c.fu_dist(i,j)))

