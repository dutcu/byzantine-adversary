import threading
import random
from . import globals as g
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
        self.read = [False for _ in range(g.n)]

    def __str__(self):
        return f"sender: {self.sender} | epoch: {self.epoch} | round: {self.round} | message: {self.message}"

def broadcast_message(process_id, epoch, round, message):
    process = shared.processes[process_id]
    if process.faulty and round < 3:
        for receiver in range(g.n):   # not list(range(n)) to ensure all processes receive a different random message
            if g.adversary_behavior == g.RANDOM_CHOICE:
                    new_msg = BroadcastMessage(process.id, [receiver], epoch, round, random.choice(["0", "1", "?"]))
            elif g.adversary_behavior == g.INVALID_CHOICE:
                    new_msg = BroadcastMessage(process.id, [receiver], epoch, round, random.choice(["X", message]))
    else:
        new_msg = BroadcastMessage(process_id, list(range(g.n)), epoch, round, message)
    with broadcasting_lock:
        broadcasted_messages.append(new_msg)

    
