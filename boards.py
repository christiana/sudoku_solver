import grid

def generate_board_medium_1():
    'generate a board from sodoku app, difficulty -medium-'
    
    data = \
    '''
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
    return grid.load_grid(data)    

def generate_board_medium_2():
    'generate a board from sodoku app, difficulty -medium-'
    data = \
    '''
    ||||
    ||||
    ||||
    -------------
    ||||
    ||||
    ||||
    -------------
    ||||
    ||||
    ||||
    '''
    data = \
    '''
    |   |   |6 9|
    |1  |  4|   |
    |  5|3 6|821|
    -------------
    |  4|67 | 5 |
    |  7|   |9  |
    |   |54 |   |
    -------------
    |37 |4 5|2 6|
    |   |   |51 |
    | 6 | 2 | 37|
    '''
    return grid.load_grid(data)    

def generate_board_hard_1():
    'generate a board from sodoku app, difficulty -hard-'
    data = \
    '''
    |984|5 1| 72|
    | 57|  9| 3 |
    |6  |  7|   |
    -------------
    |   |  2| 1 |
    |   |   |7  |
    |561|   | 28|
    -------------
    |   |4  |   |
    |   |2  |  6|
    |19 |  3|2  |
    '''
    return grid.load_grid(data)    

def generate_board_expert_1():
    'generate a board from sodoku app, difficulty -expert-'
    grid = grid.Grid()    
    suv = grid.set_user_value
    
    suv(1,8, 3); suv(1,9, 2);
    suv(2,2, 1); suv(2,3, 8);
    suv(3,4, 8); suv(3,6, 4); suv(3,9, 6);
    
    suv(4,4, 1); suv(4,5, 4);
    suv(5,2, 8); suv(5,5, 7); suv(5,7, 4);
    suv(6,1, 3); suv(6,2, 7); suv(6,4, 2);
    
    suv(7,3, 1);
    suv(8,1, 6); suv(8,7, 2); suv(8,8, 5); suv(8,9, 7);
    suv(9,2, 2); suv(9,7, 6); suv(9,9, 3);
    
    return grid

def generate_board_expert_2():
    'generate a board from sodoku app, difficulty -expert-'
    data = \
    '''
    |   |  1|3  |
    |76 |4  |1  |
    |  5| 7 | 6 |
    -------------
    |6  |   | 3 |
    |   |  7| 49|
    |5  | 1 |   |
    -------------
    |   | 32|   |
    | 9 |   |  8|
    | 84|   |   |
    '''
    return grid.load_grid(data)    
