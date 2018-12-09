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

def generate_list_visiting_all_boxes():
    '''
    generate a list of all lambdas, one for each box.
    '''
    units = []
    for rr in range(3):
        for cc in range(3):
            units.append(lambda p, rr=rr, cc=cc: visit_box(rr, cc, p))
    return units
            
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
    
def apply_rule_one_number_per_unit(grid):
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
        

def apply_rule_all_instances_in_box_on_one_line_clears_rest_of_line(grid):
    '''
    RULE:
    - when all instances of a number in a box appears on 
      the same line (row or col), that number must be present
      in that box in that line.
    - Remove that number from the rest of the line.
      
      
      for all numbers
        for all boxes
          for rows and counts (ie line)
            count #number for each line in box
            if zero on 2, it must be on the last one
            clear number from rest of line.
    '''
    class Parser:
        '''
        applies to boxes.
        - investigate(r,c) called on each location the given box.
        - effectuate() implements all the effects from this box
        '''
        def __init__(self, grid, val):
            self.grid = grid
            self.val = val
            self.mod = False
            self.row_count = [0]*3
            self.col_count = [0]*3
            self.rb = None
            self.cb = None
        def investigate(self, r, c):
            ''
            #print('investigate (%i, %i) val=%i' % (r, c, self.val))
            self.rb = r/3
            self.cb = c/3
            rr = r%3
            cc = c%3
            candidates = grid.get_candidates(r,c)
            if self.val in candidates:
                self.row_count[rr] = self.row_count[rr] + 1
                self.col_count[cc] = self.col_count[cc] + 1
                            
        def effectuate(self):
            self._effectuate_cols()
            self._effectuate_rows()
                            
        def _get_line_of_number(self, lines):
            ''
            if lines.count(0) != 2:
                return None # no single line with all the hits, -> fail
            for counter, line in enumerate(lines):
                if line>1:
                    return counter
            return None
   
        def _effectuate_rows(self):
            ''
            #print("   ** check box=(%i,%i) val=%i row rc=%s" % (self.rb,self.cb,self.val,self.row_count) )
            if sum(self.row_count)==1:
                return # optimalization: already specified
            rr = self._get_line_of_number(self.row_count)
            if rr is not None:
                #print("!!!!!!!!! found box=(%i,%i) val=%i row rr=%i rc=%s" % (self.rb,self.cb,self.val,rr,self.row_count) )
                # found! clear rest of row
                # clear number from row r=rr+self.rb*3
                r = rr + self.rb*3
                for c in range(9):
                    if c/3 != self.cb:
                        grid.remove_candidate(r,c,self.val)

        def _effectuate_cols(self):
            ''
            if sum(self.col_count)==1:
                return # optimalization: already specified
            cc = self._get_line_of_number(self.col_count)
            if cc is not None:
                #print("!!!!!!!!! found box=(%i,%i) val=%i col cc=%i cc=%s" % (self.rb,self.cb,self.val,cc,self.col_count) )
                # found! clear rest of row
                # clear number from row r=rr+self.rb*3
                c = cc + self.cb*3
                for r in range(9):
                    if r/3 != self.rb:
                        grid.remove_candidate(r,c,self.val)
 
    
    
    boxes = generate_list_visiting_all_boxes()

    for val in range(1,10):
        for box in boxes:
            parser = Parser(grid, val)
            box(parser.investigate)
            parser.effectuate()

def apply_rule_tuple_candidates_repeated_n_times_contain_no_other_candidates(grid):
    '''
    RULE:
    - when an n--sub-tuple of candidates appears exactly n times in 
      a box, and those candidates appears nowhere else in that box, 
      only these candidates can be present in those locations.
    - Remove the other candidates from those locations.
    '''
    class Parser:
        '''
        applies to boxes.
        '''
        def __init__(self, grid):
            self.grid = grid
            self.rb = None
            self.cb = None
            self.pairs = {} # number of appearances of each single candidate in box
            self.singles = {} # number of appearances of each pair in box
            self.found_pair = None
        def investigate(self, r, c):
            ''
            self.rb = r/3
            self.cb = c/3
            candidates = self.grid.get_candidates(r,c)
            self.add_singles(self.singles, candidates)
            self.add_pairs(self.pairs, candidates)    
        def calculate(self):
            for key,val in self.pairs.iteritems():
                n0 = self.singles[key[0]]
                n1 = self.singles[key[1]]
                # if a pair occurs twice, and both numbers appears only in the pair
                if (val==2) and (n0==2) and (n1==2):
                    self.found_pair = key
                    return # let the next iteration deal with the others.
                
        def effectuate(self, r, c):
            f = self.found_pair
            if f is None:
                return
            candidates = self.grid.get_candidates(r,c)
            if (f[0] in candidates) and (f[1] in candidates):
                for cc in candidates:
                    if cc not in f:
                        grid.remove_candidate(r, c, cc)
                            
        def add_singles(self, singles, candidates):
            for c in candidates:
                if c not in singles:
                    singles[c] = 0
                singles[c] = singles[c] +1
        def add_pairs(self, pairs, candidates):
            if len(candidates)<2:
                return
            for c in candidates[1:]:
                new_pair = (candidates[0], c)
                if new_pair not in pairs:
                    pairs[new_pair] = 0
                pairs[new_pair] = pairs[new_pair] + 1
            self.add_pairs(pairs, candidates[1:])
                
    
    boxes = generate_list_visiting_all_boxes()

    for box in boxes:
        parser = Parser(grid)
        box(parser.investigate)
        parser.calculate()
        box(parser.effectuate)

