#!/bin/bash

ns=(2 4 10 28 82)

behaviors=(1 2)
GLOBALS_FILE="q_byzantine/globals.py"

pids=()
mkdir -p logs

for n in "${ns[@]}"; do
    for behavior in "${behaviors[@]}"; do
        echo "Starting benchmark for n=$n, adversary_behavior=$behavior..."

        python3 -u benchmark.py --n ${n} --adv ${behavior} >logs/${n}_${behavior}.log 2>&1

        pids+=($!)
    done
done

echo "All pids: ${pids[@]}"
