#!/usr/bin/env python

import numpy as np
from grid import Grid
import rules

grid = Grid()

suv = grid.set_user_value

suv(2,2, 1);
suv(2,3, 8);
suv(3,4, 8);
suv(3,6, 4);
suv(1,8, 3);
suv(1,9, 2);
suv(3,9, 6);

suv(5,2, 8);
suv(6,1, 3);
suv(6,2, 7);
suv(4,4, 1);
suv(4,5, 4);
suv(5,5, 7);
suv(6,4, 2);
suv(5,7, 4);

suv(7,3, 1);
suv(8,1, 6);
suv(9,2, 2);
suv(8,7, 2);
suv(8,8, 5);
suv(8,9, 7);
suv(9,7, 6);
suv(9,9, 3);

#grid.print_self()
print("-"*50)
#print("candidates :")
#grid.print_candidates()
print("initial condition:")
grid.print_found()
grid.print_statistics()
print("-"*50)
iteration_count = 0

while True:
    candidates_pre = grid.get_candidate_count()
    iteration_count = iteration_count + 1

    print("apply_rule: one_number_per_unit...")
    #rules.apply_rule_one_number_per_unit(grid)
    rules.apply_rule_one_number_per_unit_one_pass(grid)
    grid.print_statistics()
    print("apply_rule: sole_candidate_in_unit_clears_others...")
    rules.apply_rule_sole_candidate_in_unit_clears_others(grid)
    grid.print_statistics()
    print("apply_rule: all_instances_in_box_on_one_line_clears_rest_of_line...")
    rules.apply_rule_all_instances_in_box_on_one_line_clears_rest_of_line(grid)
    grid.print_statistics()
    print('Iteration %i done' % iteration_count)
    print("-"*50)
    print("")
    
    if candidates_pre == grid.get_candidate_count():
        break

print("-"*50)
print("candidates:")
grid.print_candidates()
print("found:")
grid.print_found()
print("-"*50)

