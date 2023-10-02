#!/bin/bash

export PYTHON3=python3
export LPSOLVE=lp_solve

# $PYTHON3 genconst2.py

RESULT_FILE="wire2cell.result"
SKILL_FILE="wire2cell.skill"

if [ $# -ne 1 ]; then
  echo "Please specify a target lp file." 1>&2
  exit 1
fi

if [[ ! -f $1 ]]; then
  echo "lp file \"$1\" no found" 1>&2
  exit 1
fi

$LPSOLVE $1 | tee $RESULT_FILE | \
awk '/[a-zA-Z0-9]*_[0-9]*_[0-9]*_[a-zA-Z]*_[0-9]*/ { if($2==1){ gsub("_"," ", $1); print $1; } }' | \
awk -f genSkillScript.awk > $SKILL_FILE


if [[ -f $1 ]]; then
  echo "lp result file \"$RESULT_FILE\" is generated" 1>&2
  cat $RESULT_FILE | grep objective
  cat $RESULT_FILE | sed -n '/[1-9][0-9]*$/p'
fi
if [[ -f $1 ]]; then
  echo "skill file \"$SKILL_FILE\" is generated" 1>&2
fi
