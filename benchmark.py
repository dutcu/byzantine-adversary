# run_trials.py

from q_byzantine.agreement import Process, agreement
from q_byzantine import shared_state as state
from q_byzantine import broadcast
from protocol_tests import test_all
from q_byzantine.globals import n

import threading
import random
import time
import statistics

# 
def main():
    TRIALS = 10
    timings = []
    avg_epochs = []

    for trial in range(TRIALS):
        print(f"\n--- Trial {trial + 1} ---")

        state.processes.clear()
        state.threads.clear()
        state.expected_senders.clear()
        broadcast.broadcasted_messages.clear()

        for i in range(n):
            pr = Process(i, str(random.choice([0, 1])))
            state.processes.append(pr)
            thr = threading.Thread(target=agreement, args=(pr,))
            state.threads.append(thr)

        start = time.time()

        for thr in state.threads:
            thr.start()
        for thr in state.threads:
            thr.join()

        duration = time.time() - start
        timings.append(duration)

        for pr in state.processes:
            print(f"process({pr.id}) = {pr.output} @epoch: {pr.decision_epoch} | input: {pr.input_val} | faulty: {pr.faulty}")

        first = broadcast.first_to_decide
        if first is not None:
            decided_proc = next((p for p in state.processes if p.id == first), None)
            if decided_proc:
                print(f"[First to decide] Process({first}) decided at epoch {decided_proc.decision_epoch}")

        epochs = [pr.decision_epoch for pr in state.processes if pr.decision_epoch is not None]
        avg_epoch = sum(epochs) / len(epochs) if epochs else 0
        avg_epochs.append(avg_epoch)

        test_all(state.processes, broadcast.first_to_decide, broadcast.broadcasted_messages)

    # Final stats
    overall_avg_time = statistics.mean(timings)
    overall_std_time = statistics.stdev(timings) if len(timings) > 1 else 0.0
    overall_avg_epoch = statistics.mean(avg_epochs)
    overall_std_epoch = statistics.stdev(avg_epochs) if len(avg_epochs) > 1 else 0.0

    print(f"\n--- Summary over {TRIALS} trials ---")
    print(f"Average time per trial: {overall_avg_time:.2f}s ± {overall_std_time:.2f}s")
    print(f"Average decision epoch: {overall_avg_epoch:.2f} ± {overall_std_epoch:.2f}")


if __name__ == "__main__":
    main()
