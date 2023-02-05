import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 

rng = np.random.default_rng()

N = 20
t_max = 30

population = pd.Series(
    rng.choice(["A", "B"], size=N, replace=True), name="trait"
)

ps = pd.Series([np.nan] * t_max, name="p")
ps[0] = population.value_counts(normalize=True,dropna=False).sort_index()[0]

colors = {"A" : "darkgrey", 
            "B": "salmon"}

_, axes = plt.subplots(2,1, sharex=True)
axes[0].axis("equal")

circle_kws = dict(
    edgecolor="black", 
    linewidth=1., 
    alpha=1, 
    radius=.2)

# first generation
for idx, indv in population.items():
    circ = plt.Circle(xy=(0,idx),
            facecolor=colors[indv], **circle_kws)
    axes[0].add_patch(circ)

# transmission
for t in range(1, t_max):
    # draw individuals
    new_population = population.sample(N,replace=True)
    for n, (idx, indv) in enumerate(new_population.items()):
        circ = plt.Circle(xy=(t,n), 
                facecolor=colors[indv], **circle_kws)
        axes[0].add_patch(circ)

    # draw arrows
    # for src, tgt in zip(population.index, range(N)):
    #     x = 2 * t # population.index[n]
    #     y = src
    #     dx = 2 * (t + 1) - x
    #     dy = tgt - src
    #     axes[0].arrow(x,y,dx,dy, color="k", 
    #         head_width=0.1, head_length=0.1, #overhang=2,
    #         length_includes_head=True,
    #         alpha=.6, lw=1, zorder=3
    #     )
    ps[t] = new_population.value_counts(
        normalize=True,dropna=False).sort_index()[-1]
    population = new_population

axes[0].set_xlim(-1,t_max)
axes[0].set_ylim(-1,N + 1)
axes[0].set_ylabel("individuals")

axes[1].plot(range(0, t_max), ps, c="salmon", lw=3)
axes[1].set_ylim(0,1)
axes[1].set_ylabel("proportion of 'A'")
axes[1].set_xlabel("generations")

plt.tight_layout()
plt.savefig("img/chains.png", dpi=300)