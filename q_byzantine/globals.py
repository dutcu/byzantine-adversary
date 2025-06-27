import math
n = 10  # 4 , 10, 28, 82, 244
t = int(math.floor(n/3))
if n%3 == 0:
    t -= 1
MAX_ALIVE_PROCESSES = n - t

QUESTION_MARK = "?"
WAITING_MESSAGE = "waiting"

RANDOM_CHOICE = 1
INVALID_CHOICE = 2
LOST_MESSAGE = 3

adversary_behavior = 1

qb_per_process = 3  # usually calculated based on n


