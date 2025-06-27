import time
import random
from q_byzantine import broadcast
from q_byzantine import shared_state as shared
from .globals import *
from .weak_coin import quantum_coin_flip

HALF_PLUS_ONE = int(np.floor(n / 2)) + 1

class Process:
    def __init__(self, id, input_val, faulty=False):
        self.id = id
        self.input_val = input_val
        self.round_messages = {}
        self.output = None
        self.decision_epoch = None
        self.faulty = faulty

class BroadcastMessage:
    def __init__(self, sender, receivers, epoch, round, message):
        self.sender = sender
        self.receivers = receivers
        self.epoch = epoch
        self.round = round
        self.message = message
        self.read = [False for _ in range(n)]


def waiting_condition(num_received_messages, round):
    if round == 1 or round == 2:
        actual_alive_processes = [1 for pr in shared.processes if not pr.faulty].count(1)
        return num_received_messages < actual_alive_processes
    elif round == 3:
        return num_received_messages < MAX_ALIVE_PROCESSES


def receive(process, epoch, round, required_val=None):
    start = time.time()
    num_received_messages = 0
    while waiting_condition(num_received_messages, round):
        if time.time() - start > 10:
            print(f"[Process {process.id}] Timeout at round {round}")
            break
        with broadcast.broadcasting_lock:
            for msg in broadcast.broadcasted_messages:
                if (
                    msg.epoch == epoch
                    and msg.round == round
                    and process.id in msg.receivers
                    and not msg.read[process.id]
                ):
                    if round == 3:
                        assert msg.message == required_val
                    process.round_messages[msg.message] = process.round_messages.get(msg.message, 0) + 1
                    num_received_messages += 1
                    msg.read[process.id] = True


def get_majority_value(process):
    for value, count in process.round_messages.items():
        if count >= HALF_PLUS_ONE:
            return value
    return QUESTION_MARK


def get_most_frequent_val(process):
    most_frequent_val = max(process.round_messages, key=process.round_messages.get)
    if most_frequent_val == QUESTION_MARK:
        process.round_messages.pop(most_frequent_val)
        most_frequent_val = None
        if process.round_messages:
            most_frequent_val = max(process.round_messages, key=process.round_messages.get)
    number = process.round_messages.get(most_frequent_val, 0)
    return most_frequent_val, number


def agreement(process):
    current = process.input_val
    next = False
    epoch = 0
    while True:
        epoch += 1
        print(f"[P{process.id}] E{epoch} | current={current}, decided={next}")

        if process.faulty:
            broadcast.broadcast_message(process.id, epoch, 1, random.choice(["0", "1", "?", ""]))  # Malicious
        else:
            broadcast.broadcast_message(process.id, epoch, 1, current)

        if not next:
            receive(process, epoch, 1)
            current = get_majority_value(process)
        process.round_messages.clear()

        broadcast.broadcast_message(process.id, epoch, 2, current)
        if not next:
            receive(process, epoch, 2)
            answer, number = get_most_frequent_val(process)
        process.round_messages.clear()

        broadcast.broadcast_message(process.id, epoch, 3, WAITING_MESSAGE)
        if not next:
            receive(process, epoch, 3, WAITING_MESSAGE)
        process.round_messages.clear()

        coin = quantum_coin_flip(shared.processes, process, epoch)

        if process.faulty:
            current = random.choice(["0", "1", coin, "?"])

        if next:
            break

        if number >= HALF_PLUS_ONE:
            current = answer
            next = True
            process.decision_epoch = epoch
            with broadcast.decision_lock:
                if broadcast.first_to_decide is None:
                    broadcast.first_to_decide = process.id
        elif number >= 1:
            current = answer
        else:
            current = coin

        if process.faulty:
            process.decision_epoch = epoch  
            process.output = random.choice(["0", "1"])  
            break

    process.output = current
    return current
