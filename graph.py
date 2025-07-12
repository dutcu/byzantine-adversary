import matplotlib.pyplot as plt
import numpy as np

# Number of processes
num_processes = [2, 4, 10, 28, 82]

# Average times (seconds)
times_type1 = [8.88, 25.10, 135.53, 1043.58, 8188.71]
times_type2 = [8.65, 30.19, 153.58, 1264.73, 9949.43]

# Standard deviations (seconds)
errors_type1 = [2.02, 5.97, 36.97, 105.95, 1090.99]
errors_type2 = [2.30, 4.96, 37.76, 283.70, 1140.38]

# X-axis positions
x = np.arange(len(num_processes))
width = 0.35  # width of the bars

fig, ax = plt.subplots(figsize=(10, 6))

# Bar plots with error bars
bar1 = ax.bar(x - width/2, times_type1, width, label='Adversary Type 1', yerr=errors_type1, capsize=5, log=True)
bar2 = ax.bar(x + width/2, times_type2, width, label='Adversary Type 2', yerr=errors_type2, capsize=5, log=True)

# Labeling
ax.set_xlabel('Number of Processes')
ax.set_ylabel('Time to Consensus (seconds, log scale)')
ax.set_title('Consensus Time vs Number of Processes by Adversary Type')
ax.set_xticks(x)
ax.set_xticklabels(num_processes)
ax.legend()

# Annotate bar tops
for bars in [bar1, bar2]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()
