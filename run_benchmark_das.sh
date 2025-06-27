#!/bin/bash

ns=(4 10 28 82 244)
behaviors=(1 2 3)
GLOBALS_FILE="q_byzantine/globals.py"

# Backup the original globals file
cp "$GLOBALS_FILE" "$GLOBALS_FILE.bak"

pids=()

for n in "${ns[@]}"; do
    for behavior in "${behaviors[@]}"; do
        echo "Starting benchmark for n=$n, adversary_behavior=$behavior..."


        # Update globals.py
        cat > "$GLOBALS_FILE" <<EOF
import math
n = $n  # current n
t = int(math.floor(n/3))
if n%3 == 0:
    t -= 1
MAX_ALIVE_PROCESSES = n - t

QUESTION_MARK = "?"
WAITING_MESSAGE = "waiting"

RANDOM_CHOICE = 1
INVALID_CHOICE = 2
LOST_MESSAGE = 3


adversary_behavior = $behavior

qb_per_process = 3  # usually calculated based on n
EOF

        prun -np 1 bash -c "python3 -u benchmark.py >${n}_${behavior}.log 2>&1" &


        # Save PID
        pids+=($!)
    done
done

echo "All pids: ${pids[@]}"
# Restore original globals.py
mv "$GLOBALS_FILE.bak" "$GLOBALS_FILE"
