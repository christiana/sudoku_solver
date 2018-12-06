import numpy as np
        

def visit_row(r, visitor):
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

#def strip_row_candidates_from_exact_value(grid, r, c, val):
#    mod = False
#    for rr in range(9):
#        if rr!=r:
#            mod = grid.remove_candidate(rr, c, val) or mod        
#    return mod

#def strip_col_candidates_from_exact_value(grid, r, c, val):
#    mod = False
#    for cc in range(9):
#        if cc!=c:
#            mod = grid.remove_candidate(r, cc, val) or mod
#    return mod

#def strip_box_candidates_from_exact_value(grid, r, c, val):
 #   mod = False        
#    rb = r/3
#    cb = c/3;
#    rb = rb*3
#    cb = cb*3
    #print(r, rb)
    #print(c, cb)
        
#    for rr in range(rb, rb+3):        
#        for cc in range(cb, cb+3):
#            print("check", rr, cc, " for", val)
#            if not (rr==r and cc==c):
#                mod = grid.remove_candidate(rr, cc, val) or mod
#    return mod

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
    
#    mod = False
#    mod = strip_row_candidates_from_exact_value(grid, r, c, val) or mod
#    mod = strip_col_candidates_from_exact_value(grid, r, c, val) or mod
#    mod = strip_box_candidates_from_exact_value(grid, r, c, val) or mod
#    return mod

#def strip_candidates_from_exact_value(grid, r, c, val):
#    '''
#    given an exact value in (r,c), remove all occurrences
#    from row, column, box.
#    '''
#    mod = False
#    mod = strip_row_candidates_from_exact_value(grid, r, c, val) or mod
#    mod = strip_col_candidates_from_exact_value(grid, r, c, val) or mod
#    mod = strip_box_candidates_from_exact_value(grid, r, c, val) or mod
#    return mod

def apply_rule_one_number_per_unit_one_pass(grid):
    '''
    RULE:
    - one number occurs once per unit
    - unit can be row, column, box
    '''
    print("apply_rule_one_number_per_unit_one_pass...")
    modified = False
    for r in range(9):
        for c in range(9):
            val = grid.get_value(r, c)
            if val is not None:
                # an exact value found: remove from row
                modified = strip_candidates_from_exact_value(grid, r, c, val) or modified
    return modified

def apply_rule_one_number_per_unit(grid):
    while apply_rule_one_number_per_unit_one_pass(grid):
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
    # for all numbers:
    #      for all rows, cols, boxes: 
    #          if number appears only once in unit, it must be set there.
    #
    for val in range(1,10):
        for r in range(9):
            parser = SoleCandidateParser(grid, val)
            visit_row(r, parser.investigate)
            visit_row(r, parser.effectuate)
        for c in range(9):
            parser = SoleCandidateParser(grid, val)
            visit_col(c, parser.investigate)
            visit_col(c, parser.effectuate)
        for rr in range(3):
            for cc in range(3):
                parser = SoleCandidateParser(grid, val)
                visit_box(rr, cc, parser.investigate)
                visit_box(rr, cc, parser.effectuate)
        


