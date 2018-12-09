import numpy as np

class Grid:
    '''
    Define a 9x9x9 binary grid,
    The first 9x9 is the sudoku board,
    the last 9 is booleans showing the possibility
    of the 9 values being present in that position.
    '''
    def __init__(self):
        'initialize a grid with all unknowns'        
        self.values = np.ones((9,9,9), dtype=np.int8)
        
    def set_value(self, r, c, val):
        self.values[r][c][0:9] = 0
        self.values[r][c][val-1] = 1 

    def set_user_value(self, r, c, val):
        self.set_value(r-1, c-1, val);
        
    def print_self(self):
        print(self.values)
        
    def print_found_compact(self):
        print(self.get_found())
        
    def get_candidates(self, r, c):
        'return a list of candidates for (r,c)'
        return [ n+1 for n in range(9) if self.values[r][c][n]==1 ]
    
    def get_value(self, r, c):
        'return the exact value in (r,c), return None if uncertain'
        candidates = self.get_candidates(r, c)
        if len(candidates)==1:
            return candidates[0]
        else:
            return None
        
    def get_found(self):
        'return all exact values'
        found = np.zeros((9,9), dtype=np.int8)
        for r in range(9):
            for c in range(9):
                found[r][c] = self.get_value(r, c)
        return found
    
    def _print_grid(self, element_printer, element_width=1, spacing=1):
        width = 9*element_width + spacing*12 + 4
        for r in range(9):
            if (r%3==0):
                print('-'*width)        
            line = ''
            for c in range(9):
                if (c%3==0):
                    line = line + '|' + ' '*spacing
                line = line + element_printer(r,c) + ' '*spacing
            print('%s|' % line) 
        print('-'*width)   

    def print_found(self):
        def foo(self, r, c):
            found = self.get_value(r,c)
            if found is None:
                return ' '
            else:
                return str(found) 
        bind = lambda r,c : foo(self, r, c)
        self._print_grid(bind, element_width=1)

    def print_candidates(self):
        def foo(self, r, c):
            val = [str(n+1) if self.values[r][c][n]==1 else ' ' for n in range(9)]
            val = ''.join(val);
            return '%9s' % val
        bind = lambda r,c : foo(self, r, c)
        self._print_grid(bind, element_width=9, spacing=5)
        
    def get_found_count(self):
        count = 0
        for r in range(9):
            for c in range(9):
                if self.get_value(r, c):
                    count = count + 1 
        return count
    
    def get_candidate_count(self):
        count = 0
        for r in range(9):
            for c in range(9):
                count = count + len(self.get_candidates(r, c))
        return count
        
    def print_statistics(self):
        found = self.get_found_count()
        candidates = self.get_candidate_count()
        print('found: %s/%s. candidates: %s/%s' % (found, 81, candidates, 81*9))
        
    def remove_candidate(self, r, c, val):
        n = val-1
        modified = self.values[r][c][n] == 1 
        self.values[r][c][n] = 0
        return modified

def load_grid(data):
    '''
    Generate a grid based on text input like this:
    
    |64 | 3 |  7|
    |5 1| 7 |9  |
    |   |   | 1 |
    -------------
    |  4|9 8| 6 |
    | 8 |  3| 2 |
    |   |4  |   |
    -------------
    |4  |157| 3 |
    |2 8|3  | 4 |
    |75 |   | 96|
    '''
    lines = data.split('\n')
    lines = [l.strip() for l in lines if len(l.strip())>0]
    lines = [l for l in lines if l.count('-')==0]
    
#    for l in lines:
#        print("L:[%s]" % l)
        
    c_indexes = [1,2,3, 5,6,7, 9,10,11]

    grid = Grid()    
        
    for r,line in enumerate(lines):
#        print(line)
        for c,i in enumerate(c_indexes):
            try:
#                print("%i%i: %s" % (r,c,line[i]))
                grid.set_value(r, c, int(line[i]))        
            except:
                pass
        
    return grid

