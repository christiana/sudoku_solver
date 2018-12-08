#!/usr/bin/env python

#import numpy as np
import boards
import rules

def print_initial_state(grid):
    print("-"*50)
    print("initial board:")
    grid.print_found()
    grid.print_statistics()
    print("-"*50)

def print_end_state(grid):
    print("-"*50)
    print("remaining candidates:")
    grid.print_candidates()
    print("end board:")
    grid.print_found()
    print("-"*50)
    
def apply_rule_pretty(grid, rule):
    print("apply_rule: %s ..." % rule.__name__)
    rule(grid)
    grid.print_statistics()
    
def get_all_rules():
    return [rules.apply_rule_one_number_per_unit,
            rules.apply_rule_sole_candidate_in_unit_clears_others,
            rules.apply_rule_all_instances_in_box_on_one_line_clears_rest_of_line,
            rules.apply_rule_tuple_candidates_repeated_n_times_contain_no_other_candidates
            ]
    
def solve(grid):
    iteration_count = 0
    rule_list = get_all_rules()
    
    while True:
        candidates_pre = grid.get_candidate_count()
        iteration_count = iteration_count + 1
        
        for r in rule_list:
            apply_rule_pretty(grid, r)
            
        print('Iteration %i done.' % iteration_count)
        print("-"*50)
        print("")
        
        if candidates_pre == grid.get_candidate_count():
            break

def solve_pretty(grid):
    print_initial_state(grid)
    solve(grid)
    print_end_state(grid)

if __name__ == "__main__":    
    grid = boards.generate_board_hard_1()    
    solve_pretty(grid)

