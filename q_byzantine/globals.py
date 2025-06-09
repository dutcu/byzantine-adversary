import threading

n = 4
t = 1
MAX_ALIVE_PROCESSES = n - t

QUESTION_MARK = "?"
WAITING_MESSAGE = "waiting"

qb_per_process = 3  # usually calculated based on n

coin_lock = threading.Lock()
leader_lock = threading.Lock()

coin_condition = threading.Condition()
leader_condition = threading.Condition()

processes = []
threads = []