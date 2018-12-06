#!/usr/bin/env python

import numpy as np
from grid import Grid
import rules

print("hello sudokus")
grid = Grid()
#grid.set_user_value(0,2, 4)
#grid.set_user_value(4,4, 6)
#grid.set_user_value(6,5, 3)

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
print("candidates:")
grid.print_candidates()
print("found:")
grid.print_found()

print("apply_rule_one_number_per_unit...")
rules.apply_rule_one_number_per_unit(grid)
print("apply_rule_sole_candidate_in_unit_clears_others...")
rules.apply_rule_sole_candidate_in_unit_clears_others(grid)

print("candidates:")
grid.print_candidates()
print("found:")
grid.print_found()

