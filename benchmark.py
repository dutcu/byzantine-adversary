import argparse
import threading
import random
import time
import statistics
from datetime import datetime

from q_byzantine.agreement import Process, agreement
from q_byzantine import shared_state as state
from q_byzantine import broadcast
from q_byzantine import globals as g
from protocol_tests import test_all


def parse_args():
    parser = argparse.ArgumentParser(description="Run Quantum Byzantine Agreement trials.")
    parser.add_argument("--n", type=int, default=244, help="Number of processes")
    parser.add_argument("--adv", type=int, default=1, help="Adversary behavior (1 = RANDOM_CHOICE, 2 = INVALID_CHOICE)")
    return parser.parse_args()


def print_trial_header(trial_num, total_trials, n_processes, adv_behavior):
    print(f"\n{'='*50}")
    print(f"TRIAL {trial_num}/{total_trials} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Processes: {n_processes} | Adversary: {adv_behavior}")
    print(f"{'='*50}")


def main():
    args = parse_args()
    g.configure_globals(args.n, args.adv)
    TRIALS = 5
    timings = []
    avg_epochs = []
    print(f"\n{'#'*50}")
    print(f"Starting benchmark with {g.n} processes and adversary behavior {g.adversary_behavior}")
    print(f"Total trials: {TRIALS}")
    print(f"{'#'*50}\n")
    


    for trial in range(TRIALS):
        print_trial_header(trial+1, TRIALS, g.n, g.adversary_behavior)
        from q_byzantine.adversary import adversary_reset
        adversary_reset()
        # Initialize timing markers
        init_time = time.time()
        state.processes.clear()
        state.threads.clear()
        broadcast.broadcasted_messages.clear()
        broadcast.first_to_decide = None

        # Process creation
        create_start = time.time()
        for i in range(g.n):
            pr = Process(i, str(random.choice(["0", "1"])))
            state.processes.append(pr)
            thr = threading.Thread(target=agreement, args=(pr,))
            state.threads.append(thr)
        create_end = time.time()

        # Run agreement protocol
        agreement_start = time.time()
        for thr in state.threads:
            thr.start()
        for thr in state.threads:
            thr.join()
        agreement_end = time.time()

        # Calculate timings
        duration = agreement_end - agreement_start
        timings.append(duration)
        
        # Print detailed timing info
        print(f"\nTiming breakdown:")
        print(f"- Initialization: {(create_start-init_time):.4f}s")
        print(f"- Process creation: {(create_end-create_start):.4f}s")
        print(f"- Agreement protocol: {duration:.4f}s")
        print(f"- Total trial time: {(agreement_end-init_time):.4f}s")

        # Process results
        for pr in state.processes:
            print(f"process({pr.id}) = {pr.output} @epoch: {pr.decision_epoch} | input: {pr.input_val} | faulty: {pr.faulty}")

        first = broadcast.first_to_decide
        if first is not None:
            decided_proc = next((p for p in state.processes if p.id == first), None)
            if decided_proc:
                print(f"\n[First to decide] Process({first}) decided at epoch {decided_proc.decision_epoch}")

        epochs = [pr.decision_epoch for pr in state.processes if pr.decision_epoch is not None]
        avg_epoch = sum(epochs) / len(epochs) if epochs else 0
        avg_epochs.append(avg_epoch)

        test_all(state.processes, broadcast.first_to_decide, broadcast.broadcasted_messages)

    # Final summary
    overall_avg_time = statistics.mean(timings)
    overall_std_time = statistics.stdev(timings) if len(timings) > 1 else 0.0
    overall_avg_epoch = statistics.mean(avg_epochs)
    overall_std_epoch = statistics.stdev(avg_epochs) if len(avg_epochs) > 1 else 0.0

    print(f"\n{'#'*50}")
    print(f"SUMMARY OVER {TRIALS} TRIALS")
    print(f"{'#'*50}")
    print(f"Average time per trial: {overall_avg_time:.2f}s ± {overall_std_time:.2f}s")
    print(f"Average decision epoch: {overall_avg_epoch:.2f} ± {overall_std_epoch:.2f}")
    print(f"\nDetailed timings:")
    for i, t in enumerate(timings, 1):
        print(f"Trial {i}: {t:.4f}s")


if __name__ == "__main__":
    main()