import matplotlib.pyplot as plt
import numpy as np
from utils import to_cartesian
from matplotlib.patches import Circle
from target import Target


def draw_target():
    target = Target()
    fig, ax = target.draw()
    fig.tight_layout()
    plt.show()


def graph_prec_scores_numbers(nb_darts: int, r:int):
    """
    Draw a target and performs a specfied number of darts (nb_darts) throws on a full circle with a specified radius (r) for several precisions. 
    Displays the results on a separate graph.
    """
    target = Target()
    fig, ax = plt.subplots()
    means = []
    angles = np.arange(0, 360, Target.ANGLE_NUMBER)
    for prec in [10, 20, 30, 40, 50, 60]:
        means = []
        for angle in angles:
            x, y = to_cartesian(r, t=angle)
            target.add_darts(nb_darts, goal=(x, y), prec=(prec, prec))
            means.append(target.df["score"].mean())
            target.reset()
        ax.plot(
            target.get_number(angles).astype(str),
            means,
            ls="-",
            marker="x",
            label=f"prec : {prec}",
        )
    ax.set(
        xlabel="Région de la cible (sens anti-horaire)",
        ylabel="score moyen",
        title=f"Score moyen pour {nb_darts} fléchettes, visant les triples",
    )
    fig.legend()
    plt.show()


def target_with_bubbles(nb_darts: int, r: int):
    """
    Draw a target and performs a specfied number of darts (nb_darts) throws on a full circle with a specified radius (r)
    Display the results on the target. 
    """
    target = Target()
    fig, ax = target.draw()
    angles = np.arange(0, 360, Target.ANGLE_NUMBER)
    for r in [0, 50, 103, 150]:
        for angle in angles:
            x, y = to_cartesian(r, t=angle)
            target.add_darts(nb_darts, goal=(x, y), prec=(40, 40))
            mean = target.df["score"].mean()
            ax.add_patch(Circle((x, y), radius=mean, alpha=0.7))
            ax.text(x, y, f"{mean:.1f}", va="center", ha="center")
            target.reset()
            if r == 0:
                break
    ax.set(
        title=f"Score moyen en fonction de l'endroit que l'on vise (avec une certaine précision)",
    )
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    draw_target()
    graph_prec_scores_numbers(nb_darts=5000)
    target_with_bubbles(nb_darts=5000, r=100)
