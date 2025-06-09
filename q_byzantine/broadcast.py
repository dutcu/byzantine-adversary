import threading
from .globals import *

broadcasted_messages = []
first_to_decide = None
broadcasting_lock = threading.Lock()
decision_lock = threading.Lock()

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

def broadcast(process_id, epoch, round, message):
    new_msg = BroadcastMessage(process_id, list(range(n)), epoch, round, message)
    with broadcasting_lock:
        broadcasted_messages.append(new_msg)
