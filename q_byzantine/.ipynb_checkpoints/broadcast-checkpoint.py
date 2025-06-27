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
        for receiver in range(n):   # not list(range(n)) to ensure all processes receive a different random message
            if random.random() < 0.5:   # 50% chance to broadcast a random message, the rest will omit sending the message (data loss)
                msg = BroadcastMessage(process.id, [receiver], epoch, round, random.choice(["0", "1", "X"]))
                broadcasted_messages.append(msg)

    else:
        new_msg = BroadcastMessage(process_id, list(range(n)), epoch, round, message)
        with broadcasting_lock:
            broadcasted_messages.append(new_msg)

    
