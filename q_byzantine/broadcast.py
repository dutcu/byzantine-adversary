import threading
import random
from .globals import *
from q_byzantine import shared_state as shared

broadcasted_messages = []
broadcasting_lock = threading.Lock()
decision_lock = threading.Lock()
first_to_decide = None  


class BroadcastMessage:
    def __init__(self, sender, receivers, epoch, round, message):
        self.sender = sender
        self.receivers = receivers
        self.epoch = epoch
        self.round = round
        self.message = message
        self.read = [False for _ in range(n)]

    def __str__(self):
        return f"sender: {self.sender} | epoch: {self.epoch} | round: {self.round} | message: {self.message}"

def broadcast_message(process_id, epoch, round, message):
    process = shared.processes[process_id]

    if process.faulty:
        for receiver in range(n):
            send = False
            msg_value = None

            if adversary_behavior == RANDOM_CHOICE:
                msg_value = random.choice(["0", "1", "?"])
                send = True

            elif adversary_behavior == INVALID_CHOICE:
                msg_value = random.choice(["X", message])
                send = True

            elif adversary_behavior == LOST_MESSAGE:
                if random.random() < 0.9:
                    msg_value = message
                    send = True

            if send:
                new_msg = BroadcastMessage(process.id, [receiver], epoch, round, msg_value)
                with broadcasting_lock:
                    broadcasted_messages.append(new_msg)
                    shared.expected_senders[(epoch, round, receiver)].add(process.id)

    else:
        receivers = list(range(n))
        new_msg = BroadcastMessage(process_id, receivers, epoch, round, message)
        with broadcasting_lock:
            broadcasted_messages.append(new_msg)
            for receiver in receivers:
                shared.expected_senders[(epoch, round, receiver)].add(process_id)

    
