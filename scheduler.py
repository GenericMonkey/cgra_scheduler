from itertools import product
'''
Based on a 3 x 3 CGRA with 3 memory FUs
MFU0 FU1 FU2
MFU3 FU4 FU5
MFU6 FU7 FU8
'''


DIMENSION = 3


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
    '''
    Prints current state of schedule
    #TODO: Nice way to display inst if scheduled
    '''
    def print(self):
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
    function to compute cost per slot
    ''' 
    def routing_cost(self):
        pass


class mock_dag:
    def __init__(self):
        self.numops = 5


if __name__ == '__main__':
    dag = mock_dag()
    s = Scheduler(2, dag)
    #for i in range(9):
    #    print (s.neighbors(i))
    s.print()
