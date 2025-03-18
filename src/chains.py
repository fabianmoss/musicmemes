import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=12123)

N = 5
t_max = 11

population = pd.Series(
    rng.choice(["A", "B"], size=N, replace=True), name="trait"
).sort_index()

ps = pd.Series([np.nan] * t_max, name="p")
ps[0] = population.value_counts(normalize=True, dropna=False).sort_index().get("A", 0)

colors = {
    "A": "#eb6864",
    "B": "lightgrey",  # colors from Quarto template
}


def shorten(x, y, dx, dy):
    # TODO
    return x, y, dx, dy


_, axes = plt.subplots(
    2, 1, sharex=False, figsize=(t_max, N * 1.5), height_ratios=[3, 1]
)

circle_kws = dict(edgecolor="black", linewidth=1.0, alpha=1, radius=0.2)

# first generation
for idx, indv in population.items():
    circ = plt.Circle(xy=(0, idx), facecolor=colors[indv], **circle_kws)
    axes[0].add_patch(circ)

# transmission
for t in range(1, t_max):
    # draw individuals
    new_population = population.sample(N, replace=True)
    for n, (idx, indv) in enumerate(new_population.items()):
        circ = plt.Circle(xy=(t, n), facecolor=colors[indv], **circle_kws)
        axes[0].add_patch(circ)

    # draw arrows
    for src, tgt in zip(new_population.index, range(N)):
        x = t - 1
        y = src
        dx = t - x
        dy = tgt - src

        x, y, dx, dy = shorten(x, y, dx, dy)
        axes[0].arrow(
            x,
            y,
            dx,
            dy,
            color="k",
            head_width=0.1,
            head_length=0.1,
            overhang=0.3,
            length_includes_head=True,
            alpha=0.6,
            lw=1,
            zorder=3,
        )

    ps[t] = (
        new_population.value_counts(normalize=True, dropna=False)
        .sort_index()
        .get("A", 0)
    )
    population = new_population.reset_index(drop=True)

# axes[0].axis("equal")
axes[0].set_aspect("equal")  # should be "datalim"
# axes[1].set_aspect(2,adjustable="box") # should be "datalim"
# axes[0].set_xlim(-1,t_max)
# axes[0].set_ylim(-2, N + 1)
axes[0].set_ylabel("individuals")
axes[0].set_xticks([])

axes[1].plot(range(t_max), ps, c=colors["A"], lw=3, marker="o", markersize=5)
# axes[1].fill_between(np.arange(t_max),ps, color="salmon")
# axes[1].fill_between(np.arange(t_max),ps,1, color="grey")
axes[1].set_ylim(0, 1)
axes[1].set_ylabel("proportion of 'A'")
axes[1].set_xlabel("generations")

plt.tight_layout()
plt.savefig("img/chains.png", dpi=300)
