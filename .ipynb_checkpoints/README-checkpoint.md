# Description
This is the implementation for the distributed quantum consensus protocol from Ben-Or and Hassidim [1] for the synchronous model that can reach agreement in a constant expected time even in the presence of a full information, adaptive, and computationally unbounded fail-stop adversary that stops up to $t < \frac{n}{3}$ processes. This protocol is simulated under Qiskit runtime local testing mode with Qiskit Aer (V2) Sampler. 

# Set up
In order to run this implementation you must install the following libraries in the environment that will run it:

```pip install ipynb qiskit qiskit[visualization]```

# Organization
The agreement protocol is the main program to run and can be found under ```fail_stop_agreement.ipynb```. This protocol uses the weak global coin protocol implemented under ```weak_global_coin.ipynb```. After an execution of the whole agreement protocol the tests of agreement, validity, and termination that must be fulfilled by a consensus algorithm (and a lemma that is used to prove the above properties) will be run. These tests are found in ```protocol_tests.py```. The processes taking part of the protocols can be stopped by an adversary, its implementation can be found in ```adversary.ipynb```. Finally, the only parameter that might be changed is the number of processes _n_[^*], which can be found in the ```globals.py``` file, together with other global variables. 

The ```visualization.ipynb``` file contains the neccesary code to plot the circuits and histograms used in this implementation.

### References
 [1] *Ben-Or, M., & Hassidim, A.* (2005, May). **Fast quantum Byzantine agreement**. In Proceedings of the thirty-seventh annual ACM symposium on Theory of computing (pp. 481-485).

[^*]: Note that _n_ cannot excede 384 and with $n = 244$ processes it already takes on average 40 min to execute the whole agreement protocol.