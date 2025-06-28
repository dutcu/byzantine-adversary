#!/bin/bash

ns=(4 10 28 82 244)
behaviors=(1 2)
GLOBALS_FILE="q_byzantine/globals.py"

# Backup the original globals file
cp "$GLOBALS_FILE" "$GLOBALS_FILE.bak"

pids=()

for n in "${ns[@]}"; do
    for behavior in "${behaviors[@]}"; do
        echo "Starting benchmark for n=$n, adversary_behavior=$behavior..."


        prun -np 1 -t 05:00:00 bash -c "python3 -u benchmark.py --n ${n} --adv ${behavior} >${n}_${behavior}.log 2>&1" &


        # Save PID
        pids+=($!)
    done
done

echo "All pids: ${pids[@]}"
# Restore original globals.p