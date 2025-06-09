import threading

coin_lock = threading.Lock()
leader_lock = threading.Lock()

coin_condition = threading.Condition()
leader_condition = threading.Condition()

processes = []
threads = []
