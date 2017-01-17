#!/usr/bin/env python

import cplex
from cplex.exceptions import CplexError
from cplex.callbacks import MIPInfoCallback
from fractions import Fraction
from math import fabs
import sys
import time
import argparse
import logging

from bounds import upper_bound

logging.basicConfig(level=logging.DEBUG)

class IncrementalInfoCallback(MIPInfoCallback):
    """ Displays CPLEX incumbent solution as decimal and guessed fraction """
    def __call__(self):
        new_incumbent = False
        has_incumbent = self.has_incumbent()
        if has_incumbent:
            inc_obj = self.get_incumbent_objective_value()
            if fabs(self.last_incumbent - inc_obj) > \
                   1e-5*(1 + fabs(inc_obj)):
                self.last_incumbent = inc_obj
                new_incumbent = True
        else:
            logging.debug("No incumbent found.")

        # Only print if we've found an improvement over the old best objective value
        if new_incumbent:
            logging.debug("Current best: {0}\t\t{1}".format(inc_obj, Fraction(inc_obj).limit_denominator()))
            self.__print_solution(self.get_incumbent_values(), self.num_muffins, self.num_students)
            logging.debug("\n")
            
    def __print_solution(self, arr, num_muffins, num_students):
        """ Prints the assignment of students to muffin chunks """
        for s in range(num_students):
            slice_map = {}
            for m in range(num_muffins):
                slice_size = arr[m*num_students+s]
                if slice_size > 0:
                    slice_map[m] = Fraction(slice_size)
            logging.debug("S{0}, n={1}: {2}".format(s, len(slice_map), ",".join("{0}->{1}".format(_m,_v.limit_denominator()) for _m, _v in slice_map.iteritems())))

            # Sanity check -- makes sure our guessed Fraction slices add up to Fraction m/s, for every student
            assert 0 == sum([_v.limit_denominator() for _v in slice_map.values()]) - Fraction(num_muffins, num_students)

            
            
def __idx_muffin_sliver(m, s):
    """ Returns index for x_ij givens m muffins, s students """
    def inner_idx(i, j):
        return i*s + j
    return inner_idx

def __idx_muffin_binary(m, s):
    """ Returns index for y_ij given m muffins, s students """
    def inner_idx(i, j):
        return m*s + i*s + j
    return inner_idx

def __idx_muffin_min_sliver(m, s):
    """ Returns index for z given m muffins, s students """
    return m*s + m*s

def __build_muffins(p, m, s):
    """ Builds CPLEX model (obj, constraints) for CPLEX object p """

    start = time.time()
    
    # Three variable sets:
    # x_ij \in [0,1]    for each i \in [m], j \in [s]
    # y_ij \in {0,1}    for each i \in [m], j \in [s]
    # z    \in [0,1]
    idx_sliver = __idx_muffin_sliver(m, s)
    idx_binary = __idx_muffin_binary(m, s)
    idx_min_sliver = __idx_muffin_min_sliver(m, s)
    
    # Objective:  maximize z
    p.objective.set_sense(p.objective.sense.maximize)
    obj = [0]*(m*s) + [0]*(m*s) + [1]

    # Bounds:  unit real for the first m*s, binary for the second m*s, unit real for the last
    lb = [0]*len(obj)
    ub = [1]*len(obj)
    types = "C"*(m*s) + "I"*(m*s) + "C"

    p.variables.add(obj   = obj,
                    lb    = lb,
                    ub    = ub,
                    types = types,
                    )

    # Build the constraint matrix
    rows = []
    senses = []
    rhs = []
    
    # Push z against the current minimum sliver of muffin
    # x_ij + (1-y_ij) \geq z    \forall i \in [m], j \in [s]
    # Equiv:  x_ij - y_ij - z \geq -1
    for i in xrange(m):
        for j in xrange(s):
            rows.append([ [idx_sliver(i,j), idx_binary(i,j), idx_min_sliver],
                          [1, -1, -1],
            ])
            senses.append("G")
            rhs.append(-1)


    # Muffins must be completely allocated
    # \sum_j x_ij = 1   \forall i \in [m]
    for i in xrange(m):
        rows.append([ [idx_sliver(i,j) for j in xrange(s) ],
                      [1]*s,
        ])
        senses.append("E")
        rhs.append(1)

    # Each student must get m/s total weight of muffin
    # \sum_i x_ij = m/s   \forall j \in [s]
    for j in xrange(s):
        rows.append([ [idx_sliver(i,j) for i in xrange(m) ],
                      [1]*m,
        ])
        senses.append("E")
        rhs.append(float(m)/float(s))

    # If student j receives any of muffin i, flip binary y_ij to 1
    # x_ij \leq y_ij    \forall i \in [m], j \in [s]
    # Equiv:  x_ij - y_ij \leq 0
    for i in xrange(m):
        for j in xrange(s):
            rows.append([ [idx_sliver(i,j), idx_binary(i,j)],
                          [1, -1],
            ])
            senses.append("L")
            rhs.append(0)

    # Add in the floor-ceiling bound and some other upper bounds
    # from Naveen's codebase
    loose_upper_bound = float( upper_bound(int(m), int(s)) )
    logging.debug("Floor-Ceiling UB: {0}".format(Fraction(loose_upper_bound).limit_denominator()))
    rows.append([ [idx_min_sliver],
                  [1],
              ])
    senses.append("L")
    rhs.append(loose_upper_bound)
    

    # Constraint matrix is COMPLETELY filled by this point; add to model
    p.linear_constraints.add(lin_expr = rows,
                             rhs      = rhs,
                             senses   = senses,
    )

    stop = time.time()
    return stop-start
            
def solve(m, s, verbose=False):
    """ Given m muffins and s students (positive integers), builds an ILP to
    solve the muffin problem, solves it, returns value found """

    try:
        # Initialize CPLEX
        p = cplex.Cplex()

        p.set_results_stream(None)
        if verbose:
            # Send best solution so far (and conversion to fraction) to STDERR
            logging_cb = p.register_callback(IncrementalInfoCallback)
            logging_cb.last_incumbent = 1e+75
            logging_cb.last_log = -1e+75
            logging_cb.num_muffins = m
            logging_cb.num_students = s
            # Also send CPLEX's standard incremental output to STDERR
            #p.set_results_stream(sys.stderr)
        
    
        # Build the model
        build_s = __build_muffins(p, m, s)
        logging.debug("Model build time: {0}".format(build_s))

        # Solve the model
        start = time.time()
        p.solve()
        stop = time.time()
        solve_s = stop - start
        logging.debug("Model solve time: {0}".format(solve_s))

        # Basic analytics
        sol = p.solution

        feasible = True
        if sol.get_status() == 3 or sol.get_status() == 103:
            feasible = False

        opt = sol.get_objective_value()
        return opt
    
    except CplexError as ex:
        logging.critical(ex)
        sys.exit(-1)
        
        
def main():
    
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description='Allocate muffins.')
    parser.add_argument("-m", "--muffins", dest="m", required=True, type=int,
                        help="Number of homogeneous muffins to divide")
    parser.add_argument("-s", "--students", dest="s", required=True, type=int,
                        help="Number of students")
    parser.add_argument("-v", "--verbose", action="store_true", required=False,
                        help="Outputs incremental CPLEX progress to STDERR")
    args = parser.parse_args()

    if args.m < 1 or args.s < 1:
        logging.critical("Need at least one muffin and at least one student.")
        sys.exit(-1)

    # Divide muffins amongst students
    opt = solve(args.m, args.s, args.verbose)

    print("{0},{1},{2},{3}".format(args.m, args.s, opt, Fraction(opt).limit_denominator()))
    
if __name__ == '__main__':
    main()
