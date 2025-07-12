# globals.py or wherever you define your global constants
import math

n = None
t = None
MAX_ALIVE_PROCESSES = None

QUESTION_MARK = "?"
WAITING_MESSAGE = "waiting"

RANDOM_CHOICE = 1
INVALID_CHOICE = 2
HALF_PLUS_ONE = None  # This will be calculated based on n
adversary_behavior = None

qb_per_process = 3


def configure_globals(num_processes, adv_b):
    global n, t, MAX_ALIVE_PROCESSES, adversary_behavior, HALF_PLUS_ONE
    n = num_processes
    t = int(math.floor(n / 3))
    if n % 3 == 0:
        t -= 1
    MAX_ALIVE_PROCESSES = n - t
    adversary_behavior = adv_b
    HALF_PLUS_ONE = int(math.floor(n / 2)) + 1
