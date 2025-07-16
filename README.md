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

- `fail_stop_agreement.ipynb` – Main protocol logic
- `weak_global_coin.ipynb` – Quantum weak coin flip
- `adversary.ipynb` – Faulty node simulation
- `protocol_tests.py` – Validates protocol guarantees
- `globals.py` – Configuration (e.g., number of processes)

---

## Install & Run

```bash
pip install ipynb qiskit qiskit[visualization]
```

Adjust `n` in `globals.py`, then run `benchmmark.py`.

---

## 📖 References

- Ben-Or & Hassidim (2005). *Fast Quantum Byzantine Agreement*, STOC.
- Based on work by Jiménez Moreno (2024), VU Amsterdam.
