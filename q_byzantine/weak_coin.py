import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import threading
from q_byzantine import shared_state as shared
from .globals import *
from .adversary import adversary_take_over

class QuantumFactory:
    def __init__(self):
        self.generate_coin_circuit()
        self.generate_leader_circuit()

    def generate_coin_circuit(self):
        qc = QuantumCircuit(n)
        qc.h(0)
        qc.cx(0, range(1, n))
        qc.measure_all()
        self.coin = qc

    def generate_leader_circuit(self):
        total_qubits = n * qb_per_process
        qc = QuantumCircuit(total_qubits)
        qc.h(range(0, qb_per_process))
        for j in range(1, n):
            for i in range(qb_per_process):
                qc.cx(i, i + j * qb_per_process)
        qc.measure_all()
        self.leader = qc

    def get_coin_circuit(self):
        return self.coin.copy()

    def get_leader_circuit(self):
        return self.leader.copy()

class Circuit:
    def __init__(self, system):
        self.system = system
        self.memory = None
        self.measured = False

    def measure_circuit(self):
        aer_sim = AerSimulator(method="stabilizer")
        pm = generate_preset_pass_manager(backend=aer_sim, optimization_level=1)
        transpiled = transpile(pm.run(self.system), backend=aer_sim)
        job = aer_sim.run(transpiled, shots=1)
        result = job.result()
        counts = result.get_counts()
        self.memory = list(counts.keys())[0]
        self.measured = True

class CircuitMessage:
    def __init__(self, sender, receivers, system):
        self.sender = sender
        self.receivers = receivers
        self.circuit = Circuit(system)

quantum_factory = QuantumFactory()
coin_msgs = []
leader_msgs = []
waiting_num_of_msgs = []
msg_quantity_lock = threading.Lock()

def get_msgs_for_process(pid, msgs):
    return sum(1 for m in msgs if pid in m.receivers)

def init_waiting_num_of_msgs(epoch):
    with msg_quantity_lock:
        if len(waiting_num_of_msgs) < epoch:
            min_val = min(waiting_num_of_msgs[epoch - 2]) if epoch > 1 else n
            actual_alive = [1 for pr in shared.processes if not pr.faulty].count(1)
            waiting_num_of_msgs.append([min(min_val, actual_alive)] * n)

def update_waiting_num_of_msgs(epoch, new_receivers):
    with msg_quantity_lock:
        for pr in shared.processes:
            if pr.id not in new_receivers:
                waiting_num_of_msgs[epoch - 1][pr.id] -= 1

def get_waiting_msgs(pid, epoch):
    with msg_quantity_lock:
        return waiting_num_of_msgs[epoch - 1][pid]

def notify_condition(epoch, msgs):
    return all(get_msgs_for_process(pr.id, msgs) == get_waiting_msgs(pr.id, epoch)
               for pr in shared.processes if not pr.faulty)

def send_coin(process_id, epoch):
    qc = quantum_factory.get_coin_circuit()
    msg = CircuitMessage(process_id, list(range(n)), qc)
    with shared.coin_lock:
        while len(coin_msgs) < epoch:
            coin_msgs.append([])
        coin_msgs[epoch - 1].append(msg)
    with shared.coin_condition:
        if notify_condition(epoch, coin_msgs[epoch - 1]):
            shared.coin_condition.notify_all()

def send_leader(process_id, epoch):
    qc = quantum_factory.get_leader_circuit()
    msg = CircuitMessage(process_id, list(range(n)), qc)
    with shared.leader_lock:
        while len(leader_msgs) < epoch:
            leader_msgs.append([])
        leader_msgs[epoch - 1].append(msg)
    with shared.leader_condition:
        if notify_condition(epoch, leader_msgs[epoch - 1]):
            shared.leader_condition.notify_all()

def check_condition(process, epoch, msgs, condition):
    while get_msgs_for_process(process.id, msgs[epoch - 1]) < get_waiting_msgs(process.id, epoch):
        with condition:
            condition.wait()

def get_coin_result(pid, msgs):
    for msg in msgs:
        if msg.sender == pid:
            if not msg.circuit.measured:
                msg.circuit.measure_circuit()
            return msg.circuit.memory

def get_highest_leader_id(process, epoch):
    leader_results = {}
    for msg in leader_msgs[epoch - 1]:
        if process.id in msg.receivers:
            if not msg.circuit.measured:
                msg.circuit.measure_circuit()
            outcome = int(msg.circuit.memory[:qb_per_process], 2)
            leader_results.setdefault(outcome, []).append(msg.sender)
    max_outcome = max(leader_results)
    return sorted(leader_results[max_outcome])[0]

def quantum_coin_flip(processes, process, epoch):
    while len(coin_msgs) < epoch:
        coin_msgs.append([])
    while len(leader_msgs) < epoch:
        leader_msgs.append([])

    init_waiting_num_of_msgs(epoch)
    send_coin(process.id, epoch)
    send_leader(process.id, epoch)

    new_receivers = adversary_take_over(process, coin_msgs[epoch - 1], leader_msgs[epoch - 1])

    if process.faulty:
        update_waiting_num_of_msgs(epoch, new_receivers)
        return get_coin_result(process.id, coin_msgs[epoch - 1])[process.id]

    check_condition(process, epoch, leader_msgs, shared.leader_condition)
    leader_id = get_highest_leader_id(process, epoch)
    check_condition(process, epoch, coin_msgs, shared.coin_condition)
    return get_coin_result(leader_id, coin_msgs[epoch - 1])[process.id]

