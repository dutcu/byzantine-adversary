# From FailStop
import numpy as np
from threading import Lock

n = 4
t = int(np.floor(n/3))
if n%3 == 0:
    t -= 1

MAX_ALIVE_PROCESSES = n-t
        
class Message:
    def __init__(self, process_id, receivers) -> None:
        self.sender = process_id
        self.receivers = receivers

# From QuantumCoinFlip
coin_lock = Lock()
leader_lock = Lock()
