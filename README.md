# Quantum Byzantine Consensus Simulator

This repository simulates the **Ben-Or and Hassidim quantum consensus protocol** in a synchronous setting, using Qiskit Aer.

It extends a prior simulator with advanced adversary models to test **termination**, **validity**, and **agreement** under Byzantine conditions.

---

## Key Features

- Protocol runs under **Qiskit Aer Simulator**
- Supports **Random** and **Invalid** adversary behaviors
- Includes **quantum weak coin flip** subprotocol
- Tracks key metrics: execution time, epochs, std. deviation

---

## Files

- `q_byzantine/agreement.py` – Main protocol logic
- `q_byzantine/weak_coin.py` – Quantum weak coin flip
- `q_byzantine/adversary.py` – Faulty node simulation
- `q_byzantine/broadcast.py` - Message exchange logic
- `protocol_tests.py` – Validates protocol guarantees
- `globals.py` – Configuration (e.g., number of processes)

---

## Install & Run

```bash
pip install -r requirements.txt
```

Run `benchmark.py --n [number of processes] --adv [type of adversary]` 

---

## 📖 References

- Ben-Or & Hassidim (2005). *Fast Quantum Byzantine Agreement*, STOC.
- Based on work by Jiménez Moreno (2024), VU Amsterdam.
