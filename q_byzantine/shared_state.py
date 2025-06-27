import threading
from collections import defaultdict

expected_senders = defaultdict(set)  # key: (epoch, round, receiver_id) => set of sender IDs


coin_lock = threading.Lock()
leader_lock = threading.Lock()

coin_condition = threading.Condition()
leader_condition = threading.Condition()

processes = []
threads = []
