import random
from .globals import *
from q_byzantine import shared_state as shared

num_faults = 0

def adversary_take_over(process, curr_coin_msgs, curr_leader_msgs):
    global num_faults
    if num_faults < t and not process.faulty:
        if random.choice([0, 1]):
            process.faulty = True
            num_faults += 1
            new_receivers = [i for i in range(n) if random.choice([0, 1])]

            with shared.coin_lock:
                for msg in curr_coin_msgs:
                    if msg.sender == process.id:
                        msg.receivers = new_receivers
                        break
            with shared.leader_lock:
                for msg in curr_leader_msgs:
                    if msg.sender == process.id:
                        msg.receivers = new_receivers
                        break
            return new_receivers
    return list(range(n))
