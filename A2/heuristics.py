'''
This file will contain different variable ordering heuristics to be used within
bt_search.

1. ord_dh(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the DH heuristic.
2. ord_mrv(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the MRV heuristic.
3. val_lcv(csp, var)
    - Takes in a CSP object (csp), and a Variable object (var)
    - Returns a list of all of var's potential values, ordered from best value 
      choice to worst value choice according to the LCV heuristic.

The heuristics can use the csp argument (CSP object) to get access to the 
variables and constraints of the problem. The assigned variables and values can 
be accessed via methods.
'''

import random
from copy import deepcopy

def ord_dh(csp):
    # TODO! IMPLEMENT THIS!
    #pass
    lookup = {} #dictionary to store constraints' number of unassigned variables
    for c in csp.get_all_cons():
        #cycle through all constraints
        for var in c.get_scope():
            #cycle through all variables within each constraint c
            if c.get_unasgn_vars().count(var) != 0:
                #as long as constraint c doesn't have variable var unassigned
                #update number of constraints involved with each variable
                if var not in lookup:
                    lookup[var] = len(c.get_unasgn_vars())
                else:
                    lookup[var] += len(c.get_unasgn_vars())        
    return max(lookup, key=lookup.get) #variable with most number of contraints with other unassigned variables
  
def ord_mrv(csp):
    # TODO! IMPLEMENT THIS!
    #pass
    num_legal_d = 9999999999999999999999999
    min_var = None
    for var in csp.get_all_unasgn_vars():
        #cycle through all variables that are unassigned
        if var.cur_domain_size() < num_legal_d:
            #choosing the variable only if its values remaining is smaller than the current smallest
            num_legal_d = var.cur_domain_size()
            min_var = var
    return min_var    

def val_lcv(csp, var):
    # TODO! IMPLEMENT THIS!
    #pass
    lookup = {} #dictionary to store how constraining each variable is
    for value in var.cur_domain():
        #cycle through all values of variable var
        count = 0
        var.assign(value) #assign it all the values seqentially and then see how constraining it is
        for c in csp.get_cons_with_var(var):
            #cycle through all constraints of variable var
            for unassigned in c.get_unasgn_vars():
                #for the unassigned variables of constraint c under var
                for unassigned_values in unassigned.cur_domain():
                    #check how many support values it has
                    if c.has_support(unassigned, unassigned_values):
                        count += 1
                        #the more support values, the more least constraining it is
        var.unassign()
        #unassigned to reassign another value
        lookup[value] = count
    return sorted(lookup, key=lookup.get, reverse=True) #get the least constraining variable, reverse for the highest value (i.e. LCV)
