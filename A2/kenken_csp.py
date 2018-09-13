'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct perm in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only m-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      m-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''
from cspbase import *
import itertools

def binary_ne_grid(kenken_grid):
    # TODO! IMPLEMENT THIS!
    #pass
    csp = CSP("Kenken")
    domain = []
    for i in range(1, kenken_grid[0][0] + 1):
        #insert all domains according to the kenken grid size
        domain.append(i)
    
    variables = []
    for i in domain:
        row = []
        for j in domain:
            row.append(Variable('Cell{}{}'.format(i, j), domain))
        variables.append(row)
        #variables to become a list of lists, out list holding the rows, inner holding the ith, jth cell
    
    constraints = []
    for i in range(len(domain)): #cycle through each row
        for j in range(len(domain)): #cycle through each element in each row
            for k in range(len(variables[i])):#comparing bne in rows
                if( k <= j):
                    continue
                #binary constraints between two variables in the same row
                first_var = variables[i][j]
                second_var = variables[i][k]
                c = Constraint('Constraint(Cell{}{},Cell{}{})'.format(i+1, j+1, i+1, k+1), [first_var, second_var])
                satisfying_tuples = []
                for permutations in itertools.product(domain, repeat=2):
                    #all permutations of two values within valid domain that has bne values
                    if permutations[0] != permutations[1]:
                        satisfying_tuples.append(permutations)
                c.add_satisfying_tuples(satisfying_tuples)
                constraints.append(c)
            #same process but now for columns, i.e. moving down columns for the second variable to form bne
            for k in range(len(variables[i])):
                if( k <= i):
                    continue
                first_var = variables[i][j]
                second_var = variables[k][j]        
                c = Constraint('Constraint(Cell{}{},Cell{}{})'.format(i+1, j+1, k+1, j+1), [first_var, second_var])
                satisfying_tuples = []
                for permutations in itertools.product(domain, repeat=2):
                    if permutations[0] != permutations[1]:
                        satisfying_tuples.append(permutations)
                c.add_satisfying_tuples(satisfying_tuples)
                constraints.append(c)
    
    for row in variables:
        for var in row:
            csp.add_var(var)
            #pushing variables into csp
    
    for c in constraints:
        csp.add_constraint(c)
        #pushing contraints into csp

    return csp, variables
    
def nary_ad_grid(kenken_grid):
    # TODO! IMPLEMENT THIS!
    #pass
    csp = CSP("Kenken")
    domain = []
    for i in range(1, kenken_grid[0][0] + 1):
        domain.append(i)
        #same domain insertion as bne
        
    variables = []
    for i in domain:
        row = []
        for j in domain:
            row.append(Variable('Cell{}{}'.format(i, j), domain))
        variables.append(row)
        #same variable determination as bne
        
    constraints = []
    for i in range(len(domain)):
        var=[]
        for k in range(len(variables[i])):
            var.append(variables[i][k])
        c = Constraint('Constraint(Row{})'.format(i+1), var)
        satisfying_tuples = []
        var_length=len(var)
        #contraints involve all variables of a row, permutate over all variables and values of a row
        for permutations in itertools.product(domain, repeat=var_length):
            satisfied = True
            for l in range(var_length):
                for m in range(var_length):
                    if l != (var_length-1):
                        #checking that none of the variables in a row are equal
                        if l != m and permutations[l] == permutations[m]:
                            satisfied = False
                if l == (var_length-1) and satisfied:
                    satisfying_tuples.append(permutations)
        c.add_satisfying_tuples(satisfying_tuples)
        constraints.append(c)
    #same process, but now for columns contraints
    constraints_column = []
    for i in range(len(domain)):
        var=[]
        for k in range(len(variables[i])):
            var.append(variables[k][i])
        c = Constraint('Constraint(Column{})'.format(i+1), var)
        satisfying_tuples = []
        var_length=len(var)
        for permutations in itertools.product(domain, repeat=var_length):
            satisfied = True
            for l in range(var_length):
                for m in range(var_length):
                    if l != (var_length-1):
                        if l != m and permutations[l] == permutations[m]:
                            satisfied = False
                if l == (var_length-1) and satisfied:
                    satisfying_tuples.append(permutations)
        c.add_satisfying_tuples(satisfying_tuples)
        constraints_column.append(c)
    
    for row in variables:
        for var in row:
            csp.add_var(var)
            #add variables to csp
    
    for c in constraints:
        csp.add_constraint(c)
        #adding row contraints to csp

    for c in constraints_column:
        csp.add_constraint(c)
        #adding column constraints to csp
        
    return csp, variables

#use binary model, as faster than unary when I checked
def kenken_csp_model(kenken_grid):
    #using binary not equal
    # TODO! IMPLEMENT THIS!
    #pass
    csp = CSP("Kenken")   
    domain = []
    for i in range(1, kenken_grid[0][0] + 1):
        domain.append(i)
        #getting valid domain values from the size of the kenken grid
    
    variables = []
    for i in domain:
        row = []
        for j in domain:
            row.append(Variable('Cell{}{}'.format(i, j), domain))
        variables.append(row)  
        #getting all cell variables as a list of cells inside a list of rows
        
    constraints = []
    for cage in range(1, len(kenken_grid)):
        #cage constraints first
        if(len(kenken_grid[cage]) > 2):
            #case where the cage has more than two values
            var = []
            var_domain = []
            operation = kenken_grid[cage][-1]  
            target = kenken_grid[cage][-2]
            for cell in range(len(kenken_grid[cage]) - 2):
                #determining the ith and jth cell coordinate from the variable name
                i = int(str(kenken_grid[cage][cell])[0]) - 1
                j = int(str(kenken_grid[cage][cell])[1]) - 1
                var.append(variables[i][j])
                var_domain.append(variables[i][j].domain())
            c = Constraint('Constraint(Cage{})'.format(cage), var)
            satisfying_tuples = []
            for permutations in itertools.product(*var_domain): #all permutations of the n values inside a cage
                if(operation == 0):
                    #addition
                    current_value = 0
                    for perm in permutations:
                        current_value += perm
                    if (current_value == target):
                        satisfying_tuples.append(permutations)
                elif(operation == 1):
                    #subtraction
                    for perm in itertools.permutations(permutations):
                        current_value = perm[0]
                        for m in range(1, len(perm)):
                            current_value -= perm[m]
                        if(current_value == target):
                            satisfying_tuples.append(permutations)
                elif(operation == 2):
                    #division
                    for perm in itertools.permutations(permutations):
                        current_value = perm[0]
                        for m in range(1, len(perm)):
                            current_value /= perm[m]
                        if(current_value == target):
                            satisfying_tuples.append(permutations)
                elif(operation == 3):
                    #multiplication
                    current_value = 1
                    for perm in permutations:
                        current_value *= perm
                    if (current_value == target):
                        satisfying_tuples.append(permutations)
            c.add_satisfying_tuples(satisfying_tuples)
            constraints.append(c)
        else:
            #case where each cage has only two values, one for the cell variable and second for the value enforced in that cell
            i = int(str(kenken_grid[cage][0])[0]) - 1 #ith cell coordinate
            j = int(str(kenken_grid[cage][0])[1]) - 1 #jth cell coordinate
            value_enforced = kenken_grid[cage][1] #value assigned to that cell
            variables[i][j] = Variable('Cell{}{}'.format(i, j), [value_enforced])
            
    #using binary constraints developed from the bne function
    for i in range(len(domain)): #cycle through each row
        for j in range(len(domain)): #cycle through each element in each row
            for k in range(len(variables[i])):#comparing bne in rows
                if( k <= j):
                    continue
                #binary constraints between two variables in the same row
                first_var = variables[i][j]
                second_var = variables[i][k]
                c = Constraint('Constraint(Cell{}{},Cell{}{})'.format(i+1, j+1, i+1, k+1), [first_var, second_var])
                satisfying_tuples = []
                for permutations in itertools.product(domain, repeat=2):
                    #all permutations of two values within valid domain that has bne values
                    if permutations[0] != permutations[1]:
                        satisfying_tuples.append(permutations)
                c.add_satisfying_tuples(satisfying_tuples)
                constraints.append(c)
            #same process but now for columns, i.e. moving down columns for the second variable to form bne
            for k in range(len(variables[i])):
                if( k <= i):
                    continue
                first_var = variables[i][j]
                second_var = variables[k][j]        
                c = Constraint('Constraint(Cell{}{},Cell{}{})'.format(i+1, j+1, k+1, j+1), [first_var, second_var])
                satisfying_tuples = []
                for permutations in itertools.product(domain, repeat=2):
                    if permutations[0] != permutations[1]:
                        satisfying_tuples.append(permutations)
                c.add_satisfying_tuples(satisfying_tuples)
                constraints.append(c)
    
    for row in variables:
        for var in row:
            csp.add_var(var)
            #adding variables to csp
    
    for c in constraints:
        csp.add_constraint(c)
        #adding constraints to csp
    
    return csp, variables

#ken ken model using nary model, not to be used as slower than binary model. Same priciples as kenken_csp_model 
def kenken_csp_model_nary(kenken_grid):
    #using nary all diff
    # TODO! IMPLEMENT THIS!
    #pass
    csp = CSP("Kenken")
    domain = []
    for i in range(1, kenken_grid[0][0] + 1):
        domain.append(i)
    
    variables = []
    for i in domain:
        row = []
        for j in domain:
            row.append(Variable('Cell{}{}'.format(i, j), domain))
        variables.append(row)  

    constraints = []
    for cage in range(1, len(kenken_grid)):
        if(len(kenken_grid[cage]) > 2):
            var = []
            var_domain = []
            operation = kenken_grid[cage][-1]  
            target = kenken_grid[cage][-2]
            for cell in range(len(kenken_grid[cage]) - 2):
                i = int(str(kenken_grid[cage][cell])[0]) - 1
                j = int(str(kenken_grid[cage][cell])[1]) - 1
                var.append(variables[i][j])
                var_domain.append(variables[i][j].domain())
            c = Constraint('Constraint(Cage{})'.format(cage), var)
            satisfying_tuples = []
            for permutations in itertools.product(*var_domain):
                if(operation == 0):
                    current_value = 0 
                    for perm in permutations:
                        current_value += perm
                    if (current_value == target):
                        satisfying_tuples.append(permutations)
                elif(operation == 1):
                    for perm in itertools.permutations(permutations):
                        current_value = perm[0]
                        for m in range(1, len(perm)):
                            current_value -= perm[m]
                        if(current_value == target):
                            satisfying_tuples.append(permutations)
                elif(operation == 2):
                    for perm in itertools.permutations(permutations):
                        current_value = perm[0]
                        for m in range(1, len(perm)):
                            current_value /= perm[m]
                        if(current_value == target):
                            satisfying_tuples.append(permutations)
                elif(operation == 3):
                    current_value = 1
                    for perm in permutations:
                        current_value *= perm
                    if (current_value == target):
                        satisfying_tuples.append(permutations)
            c.add_satisfying_tuples(satisfying_tuples)
            constraints.append(c)
        else:
            i = int(str(kenken_grid[cage][0])[0]) - 1
            j = int(str(kenken_grid[cage][0])[1]) - 1
            value_enforced = kenken_grid[cage][1]
            variables[i][j] = Variable('Cell{}{}'.format(i, j), [value_enforced])

    for i in range(len(domain)):
        var=[]
        for k in range(len(variables[i])):
            var.append(variables[i][k])
        c = Constraint('Constraint(Row{})'.format(i+1), var)
        satisfying_tuples = []
        var_length=len(var)
        for permutations in itertools.product(domain, repeat=var_length):
            satisfied = True
            for l in range(var_length):
                for m in range(var_length):
                    if l != (var_length-1):
                        if l != m and permutations[l] == permutations[m]:
                            satisfied = False
                if l == (var_length-1) and satisfied:
                    satisfying_tuples.append(permutations)
        c.add_satisfying_tuples(satisfying_tuples)
        constraints.append(c)
    
    constraints_column = []
    for i in range(len(domain)):
        var=[]
        for k in range(len(variables[i])):
            var.append(variables[k][i])
        c = Constraint('Constraint(Column{})'.format(i+1), var)
        satisfying_tuples = []
        var_length=len(var)
        for permutations in itertools.product(domain, repeat=var_length):
            satisfied = True
            for l in range(var_length):
                for m in range(var_length):
                    if l != (var_length-1):
                        if l != m and permutations[l] == permutations[m]:
                            satisfied = False
                if l == (var_length-1) and satisfied:
                    satisfying_tuples.append(permutations)
        c.add_satisfying_tuples(satisfying_tuples)
        constraints_column.append(c)

    for row in variables:
        for var in row:
            csp.add_var(var)
    
    for c in constraints:
        csp.add_constraint(c)

    for c in constraints_column:
        csp.add_constraint(c)
    
    return csp, variables