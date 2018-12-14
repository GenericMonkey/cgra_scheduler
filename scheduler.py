from itertools import product, combinations
from math import inf as infinity
'''
Based on a 3 x 3 CGRA with 3 memory FUs
MFU0 FU1 FU2
MFU3 FU4 FU5
MFU6 FU7 FU8
'''


DIMENSION = 3
WP = 0
Waff = 0


class Slot:
    def __init__(self, is_mem):
        self.scheduled = False
        self.inst = None
        self.is_mem = is_mem
        self.static_cost = 10 if is_mem else 1

class Scheduler:
    '''
    Constructor. Takes ii and dag for thing to schedule
    '''
    def __init__(self, ii, dag):
        self.ii = ii
        self.dag = dag
        time_slice = [Slot(i % DIMENSION == 0) for i in range(DIMENSION * DIMENSION)]
        #TODO make dag output numops
        self.schedule = [[i for i in time_slice] for j in range(ii * dag.numops)]
        self.placed_ops = []
        self.placed_ops_fu_ids = []
    '''
    Prints current state of schedule
    #TODO: Nice way to display inst if scheduled
    '''
    def print(self):
        print ("CGRA")
        print ('''
        |0(M)| 1 | 2 |
        |3(M)| 4 | 5 |
        |6(M)| 7 | 8 |
        ''')
        print ('T  |0||1||2||3||4||5||6||7||8|')
        for time in range(len(self.schedule)):
            print('   ' + '-' * 3 * DIMENSION * DIMENSION)
            print('{}'.format(time).ljust(3),end='')
            for i in range(DIMENSION * DIMENSION):
                val = 'X' if self.schedule[time][i].scheduled else ' '
                print('|' + val + '|',end='')
            print()
    '''
    returns the list of FU neighbors. Useful for route searching
    '''
    def neighbors(self, fu_id):
        row = fu_id // DIMENSION
        col = fu_id % DIMENSION
        neighbor_rows = [row]
        if row - 1 >= 0:
            neighbor_rows.append(row - 1)
        if row + 1 < DIMENSION:
            neighbor_rows.append(row + 1)
        neighbor_cols = [col]
        if col - 1 >= 0:
            neighbor_cols.append(col - 1)
        if col + 1 < DIMENSION:
            neighbor_cols.append(col + 1)
        neighbors = [r * DIMENSION + c for r,c in list(product(neighbor_rows, neighbor_cols))]
        return neighbors[1:]

    '''
    Raw grid distance used in the affinity heuristic. Every node is either dist 1 or 2 apart.
    '''
    def grid_distance(self, fu1, fu2):
        if fu2 in self.neighbors(fu1):
            return 1
        return 2

    '''
    formula to combine n many probability values
    '''
    def combine(self, prob_list):
        P = 0
        n = len(prob_list)
        for k in range(1, n + 1):
            term = 0
            for combo in combinations(range(n), k):
                prod = 1
                for idx in combo:
                    prod *= prob_list[idx]
                term += prod
            term *= (-1) ** (k - 1)
            P += term
        return P
            

    '''
    function to compute cost per slot. Should only be called on available (and reachable?) slots
    ''' 
    def routing_cost(self, time, fu_id, inst_to_schedule):
        max_dist = 5 #TODO: what is this?
        static_cost = self.schedule[time][fu_id].static_cost
        affinity_cost = 0
        for i,j in zip(self.placed_ops, self.placed_ops_fu_ids):
            affinity = 0
            for d in range(1,max_dist + 1):
                affinity += 2 ** (max_dist - d) * dag.num_shared_consumers(inst_to_schedule, i, d)
            if affinity != 0:
                dist = self.grid_distance(fu_id, j)
                affinity_cost += dist / affinity
        probability_cost = 0
        if probability_cost == 1:
            return infinity
        else:
            return static_cost + Waff * affinity_cost + WP * probability_cost



class mock_dag:
    def __init__(self):
        self.numops = 5
    
    def num_shared_consumers(self, op1, op2, distance):
        return 1 if distance < 2 else 2
    
    def is_mem_inst(self, inst):
        return 


if __name__ == '__main__':
    dag = mock_dag()
    s = Scheduler(2, dag)
    #for i in range(9):
    #    print (s.neighbors(i))
    s.print()
    #for i in combinations(range(6), 6):
    #    for j in i:
    #        print(j, end='')
    #    print()
    #print(s.combine([0.2, 0.5]))
    
