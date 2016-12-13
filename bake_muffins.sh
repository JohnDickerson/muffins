#!/bin/bash

outfile=outfile_`date +%s%N`.csv
python=python2.7
verbose=--verbose

for m in {1..10}; do
    for s in {1..10}; do
	echo "Solving for: m=${m}, s=${s} ..."
	cmd="${python} muffins.py -m ${m} -s ${s} ${verbose}"
	echo ${cmd}
	${cmd} >> ${outfile}
	
    done
done

echo "Done!"
