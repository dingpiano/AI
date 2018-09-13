'''
This file will contain different constraint propagators to be used within 
bt_search.

---
A propagator is a function with the following header
    propagator(csp, newly_instantiated_variable=None)

csp is a CSP object---the propagator can use this to get access to the variables 
and constraints of the problem. The assigned variables can be accessed via 
methods, the values assigned can also be accessed.

newly_instantiated_variable is an optional argument. SEE ``PROCESSING REQUIRED''
if newly_instantiated_variable is not None:
    then newly_instantiated_variable is the most
    recently assigned variable of the search.
else:
    propagator is called before any assignments are made
    in which case it must decide what processing to do
    prior to any variables being assigned. 

The propagator returns True/False and a list of (Variable, Value) pairs, like so
    (True/False, [(Variable, Value), (Variable, Value) ...]

Propagators will return False if they detect a dead-end. In this case, bt_search 
will backtrack. Propagators will return true if we can continue.

The list of variable value pairs are all of the values that the propagator 
pruned (using the variable's prune_value method). bt_search NEEDS to know this 
in order to correctly restore these values when it undoes a variable assignment.

Propagators SHOULD NOT prune a value that has already been pruned! Nor should 
they prune a value twice.

---

PROCESSING REQUIRED:
When a propagator is called with newly_instantiated_variable = None:

1. For plain backtracking (where we only check fully instantiated constraints)
we do nothing...return true, []

2. For FC (where we only check constraints with one remaining 
variable) we look for unary constraints of the csp (constraints whose scope 
contains only one variable) and we forward_check these constraints.

3. For GAC we initialize the GAC queue with all constaints of the csp.

When a propagator is called with newly_instantiated_variable = a variable V

1. For plain backtracking we check all constraints with V (see csp method
get_cons_with_var) that are fully assigned.

2. For forward checking we forward check all constraints with V that have one 
unassigned variable left

3. For GAC we initialize the GAC queue with all constraints containing V.

'''

def prop_BT(csp, newVar=None):
    '''
    Do plain backtracking propagation. That is, do no propagation at all. Just 
    check fully instantiated constraints.
    '''
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    # TODO! IMPLEMENT THIS!
    #pass
    values_pruned = [] #list of pruned values, so we don't need to prune a value twice
    constraints = []
    if(newVar == None):
        #no specific variable specifies, get all contraints
        constraints = csp.get_all_cons()
    else:
        #get constraints associated with pass in variable
        constraints = csp.get_cons_with_var(newVar)
    for c in constraints:
        if c.get_n_unasgn() == 1:
            #get the constraint who only has 1 unassigned variable
            var = c.get_unasgn_vars()[0]
            for d in var.cur_domain():
                if not c.has_support(var, d):
                    #setup for prunning since no support
                    prune_tuple = (var, d)
                    if(prune_tuple not in values_pruned):
                        #remember the pruned value and prune it from var's domain
                        values_pruned.append(prune_tuple)
                        var.prune_value(d)         
            if var.cur_domain_size() == 0:
                #DWO, return immediately
                return False, values_pruned
    return True, values_pruned

def prop_GAC(csp, newVar=None):
    '''
    Do GAC propagation. If newVar is None we do initial GAC enforce processing 
    all constraints. Otherwise we do GAC enforce with constraints containing 
    newVar on GAC Queue.
    '''
    # TODO! IMPLEMENT THIS!
    #pass
    values_pruned = [] #helps maintain a list of pruned values so we know whether a values has been removed already from a variable's domain
    GACQueue = []
    if(newVar == None):
        constraints = csp.get_all_cons()
        #get all constraints if no variable specified
    else:
        constraints = csp.get_cons_with_var(newVar)
        #getting constraints associated with variable newVar
    for c in constraints:
        #pushing all constraints into the end of GACQueue, a pseudo queue
        GACQueue.append(c)
    while len(GACQueue) != 0:
        c = GACQueue.pop()
        #get the last item in GACQueue (last item i.e. most recent item so the list behaves like a queue)
        for var in c.get_scope():
            for d in var.cur_domain():
                if not c.has_support(var, d):
                    #does not have support, so d must be pruned from var's domain
                    prune_tuple = (var, d)
                    if(prune_tuple not in values_pruned):
                        # if not pruned, add to prune list and prune it from var's domain
                        values_pruned.append(prune_tuple)
                        var.prune_value(d)
                    if var.cur_domain_size() == 0:
                        #no remaining value left for variable, DWO return immediately
                        GACQueue.clear()
                        return False, values_pruned
                    else:
                        for c_prime in csp.get_cons_with_var(var):
                            #since domain of var has been modified, we need to check contraints with var in its scope again
                            if (c_prime not in GACQueue):
                                #adding constraints with var in scope that isn't already in GACQueue
                                GACQueue.append(c_prime)
    return True, values_pruned