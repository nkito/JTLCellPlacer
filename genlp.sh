#!/bin/bash

export PYTHON3=python3
export LPSOLVE=lp_solve

if [ $# -ne 1 ]; then
  echo "Please specify a souce routing file." 1>&2
  exit 1
fi

if [[ ! -f $1 ]]; then
  echo "file \"$1\" not found" 1>&2
  exit 1
fi

$PYTHON3 wire2cell.py $1 | tee wire2cell.log | awk '/^/ {if(on){print($0);}} /CUT HERE/ {on=1}' > wire2cell.lp

if [[ -f $1 ]]; then
  echo "log file \"wire2cell.log\" is generated" 1>&2
  echo "-----------------------------"
  grep "Placed : " wire2cell.log
  echo "-----------------------------"
fi
if [[ -f $1 ]]; then
  echo "lp file \"wire2cell.lp\" is generated" 1>&2
fi


