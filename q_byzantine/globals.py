import numpy as np
n = 2
t = int(np.floor(n/3))
if n%3 == 0:
    t -= 1
MAX_ALIVE_PROCESSES = n - t

QUESTION_MARK = "?"
WAITING_MESSAGE = "waiting"

qb_per_process = 3  # usually calculated based on n


