# muffins
Given *m* homogeneous muffins and *s* hungry students, how can we divide the muffins in such a way such that each student receives *m/s* total weight of muffins, and that the minimum size of a muffin slice is maximized?

## Installation

This codebase uses the Python API for [IBM ILOG CPLEX](https://en.wikipedia.org/wiki/CPLEX), an optimization toolkit that is freely available for academic use.  The IBM website is awful, but here's a semi-reliable way to get the academic version of CPLEX:
0.  Make an IBM Academic Initiative account by registering [here](https://developer.ibm.com/academic/).
1.  Google "IBM ILOG CPLEX Academic" -- this will send you to an IBM website (like [this](https://www-304.ibm.com/ibm/university/academic/pub/jsps/assetredirector.jsp?asset_id=1070), but that link will likely break someday).
2.  Follow the "Software Download Catalog" link on that site -- you'll be required to log in with an Academic Initiative account.
3.  Search explicitly for "IBM ILOG CPLEX Optimization Studio" -- this should return some links to CPLEX installers for different OSes.

Once you install CPLEX, you'll also need to explicitly set up the Python API.  To do that, navigate to wherever you installed CPLEX, go to `<cplex-directory>/cplex/python/<architecture>/`, and run `python setup.py`.

From here, you should be good to go.  This will add the right things to `PYTHONPATH`, etc.  If you run into trouble, use this [website](https://www.ibm.com/support/knowledgecenter/SSSA5P_12.6.1/ilog.odms.cplex.help/CPLEX/GettingStarted/topics/set_up/Python_setup.html).

## Running the Code

For specific nonnegative values of *m* and *s*, just run the Python code directly with:
    `python muffins.py -m *m* -s *s*`
For example, to solve this problem for *m=5* and *s=3*, one would run:
    `python muffins.py -m 5 -s 3`
This will output some debug text to STDERR, along with a single line of output to STDOUT, formatted as a CSV.  That latter line is the solution.

To loop over many values of *m* and *s*, edit `bake_muffins.sh` to reflect the values of *m* and *s* that you care about, run `chmod u+x bake_muffins.sh`, and then `./bake_muffins.sh`.  This will output debug text to STDERR, but will store all STDOUT in a single CSV file in the same directory as the Python code.

The Python script can also be told to print incremental updates about the current best solution found before CPLEX proves optimality for a particular *m* and *s* pair.  This is useful for harder problems, and can be turned on using `--verbose`.  For example, for *m=24* and *s=11*, a hard problem, one would run:
    `python muffins.py -m 24 -s 11 --verbose`
