#!/bin/bash

outfile=outfile_`date +%s%N`.csv
python=python2.7
verbose=--verbose
timeout=300    # max optimization time for one solve, in seconds

for s in {7..25}; do
    for m in {1..50}; do
	echo "Solving for: m=${m}, s=${s}, timeout=${timeout} ..."
	cmd="timeout ${timeout}s ${python} muffins.py -m ${m} -s ${s} -t ${timeout} ${verbose}"
	echo ${cmd}
	${cmd} >> ${outfile}
	
    done
done

echo "Done!"
