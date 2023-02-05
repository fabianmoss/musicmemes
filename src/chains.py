import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd

N = 5
t_max = 8

scaling = 1.

variants =["#a58d48", "#a670b0"] # optimized for color blindness with iwanthue

_, axes = plt.subplots(2,1, sharex=True)
axes[0].axis("equal")

ps = []

# grid 
for t in range(t_max):
    # draw individuals
    colors = np.random.choice(variants, size=N)
    ps.append(pd.Series(colors).value_counts(normalize=True).sort_index()[0])
    for n, c in zip(range(N), colors):
        circ = plt.Circle(xy=(2 * t,n), radius=.4, 
                facecolor=c, edgecolor="black", linewidth=2., alpha=1)
        axes[0].add_patch(circ)
for t in range(t_max - 1):
    # draw transmissions
    sources = np.random.choice(range(N), replace=True, size=N)
    targets = range(N) # np.random.choice(range(N), replace=True, size=N)
    for src, trg in zip(sources, targets):
        x = 2 * t
        y = src
        dx = (2 * (t + 1) - x ) * scaling
        dy = (trg - y ) * scaling
        axes[0].arrow(x,y,dx,dy, color="k", 
            head_width=0.1, head_length=0.2, overhang=.1,
            length_includes_head=True
        )

axes[0].set_xlim(-1,2 * t_max - 1)
axes[0].set_ylim(0,N - 1)
axes[0].set_ylabel("individuals")

axes[1].plot(range(0,2 * t_max, 2), ps, c="k", lw=2)
axes[1].set_ylim(0,1)
axes[1].set_ylabel("proportion of 'A'")
axes[1].set_xlabel("generations")

plt.tight_layout()
plt.show()