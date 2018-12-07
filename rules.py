import numpy as np
        

def visit_row(r, visitor):
#    print('visit_row ', r)
    for c in range(9):
        visitor(r, c)
def visit_col(c, visitor):
    for r in range(9):
        visitor(r, c)
def visit_box(rb, cb, visitor):
    rb = rb*3
    cb = cb*3
    #print(r, rb)
    #print(c, cb)        
    for rr in range(rb, rb+3):        
        for cc in range(cb, cb+3):
            visitor(rr, cc)
            
def generate_list_visiting_all_units():
    '''
    generate a list of all lambdas, one for each unit.
    Each unit
    '''
    units = []
    for r in range(9):
        units.append(lambda p,r=r: visit_row(r, p))
    for c in range(9):
        units.append(lambda p, c=c: visit_col(c, p))
    for rr in range(3):
        for cc in range(3):
            units.append(lambda p, rr=rr, cc=cc: visit_box(rr, cc, p))
    return units

def strip_candidates_from_exact_value(grid, r, c, val):
    '''
    given an exact value in (r,c), remove all occurrences
    from row, column, box.
    '''
    class StripExact:
        def __init__(self, grid, r, c, val):
            self.grid = grid
            self.r = r
            self.c = c
            self.val = val
            self.mod = False
        def visit(self, rr, cc):
            if  (rr==self.r and cc==self.c):
                return
            self.mod = grid.remove_candidate(rr, cc, val) or self.mod
            
    stripper = StripExact(grid, r, c, val)
    visit_row(r, stripper.visit);
    visit_col(c, stripper.visit);
    visit_box(r/3, c/3, stripper.visit);
    return stripper.mod
    
def apply_rule_one_number_per_unit_one_pass(grid):
    '''
    RULE:
    - one number occurs once per unit
    - unit can be row, column, box
    '''
    modified = False
    for r in range(9):
        for c in range(9):
            val = grid.get_value(r, c)
            if val is not None:
                # an exact value found: remove from row
                modified = strip_candidates_from_exact_value(grid, r, c, val) or modified
    return modified

def apply_rule_one_number_per_unit(grid):
    ''
    while apply_rule_one_number_per_unit_one_pass(grid):
        #print("  apply_rule_one_number_per_unit_one_pass...")
        pass

def apply_rule_sole_candidate_in_unit_clears_others(grid):
    '''
    RULE:
    - when a candidate appears only once in a unit, that candidate must be the match.
    - unit can be row, column, box
    '''
    class SoleCandidateParser:
        '''
        '''
        def __init__(self, grid, val):
            self.grid = grid
            self.val = val
            self.mod = False
            self.number_of_hits = 0
        def investigate(self, r, c):
            'count number of occurrences of val'
            #print('investigate (%i, %i) val=%i' % (r, c, self.val))
            if self.val in self.grid.get_candidates(r, c):
                self.number_of_hits = self.number_of_hits + 1
        def effectuate(self, r, c):
            'set the one possible location to val, if only one was found'
            if self.number_of_hits != 1:
                return
            candidates = self.grid.get_candidates(r, c)
            if self.val in candidates and len(candidates)>1:
                self.grid.set_value(r, c, self.val)
                self.mod = True
                
    units = generate_list_visiting_all_units()
                
    for val in range(1,10):
        for unit in units:
            parser = SoleCandidateParser(grid, val)
            unit(parser.investigate)
            unit(parser.effectuate)
        


