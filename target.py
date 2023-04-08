import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, ConnectionPatch, Wedge, PathPatch
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

from utils import to_cartesian, to_polar


class Target:
    ANGLE_NUMBER = 18  # Angle pour un secteur de la cible
    R = 170  # mm
    R_INNER_BULL = 0.03735294118 * R
    R_OUTER_BULL = 0.09352941176 * R
    R_INNER_TRIPLE = 0.5847058824 * R
    R_OUTER_TRIPLE = 0.6317647059 * R
    R_INNER_DOUBLE = 0.9529411765 * R
    R_LIMIT_TARGET = 1.35 * R
    WIDTH_MULTI_BAND = 0.04705882353 * R
    NUM_SEQUENCE = [
        6,
        13,
        4,
        18,
        1,
        20,
        5,
        12,
        9,
        14,
        11,
        8,
        16,
        7,
        19,
        3,
        17,
        2,
        15,
        10,
    ]
    COLORS = {"red": "red", "green": "green", "black": "black", "beige": "beige"}

    def __init__(self):
        self.df = pd.DataFrame(
            {"x": [], "y": [], "multi": [], "number": [], "score": []}
        )

        self.return_points = np.vectorize(self.__return_points)
        self.get_number = np.vectorize(self.__get_number)
        self.fig, self.ax = None, None

    def draw(self):
        self.fig, self.ax = plt.subplots()
        thetas = np.arange(0 - Target.ANGLE_NUMBER / 2, 360, Target.ANGLE_NUMBER)
        numbers_angles = np.arange(0, 360, Target.ANGLE_NUMBER)

        alpha = 0.7
        patches = [
            Wedge(
                (0, 0),
                r=self.R_INNER_BULL,
                theta1=0,
                theta2=360,
                color=self.COLORS["red"],
                alpha=alpha,
                ec=None,
            ),
            Wedge(
                (0, 0),
                r=self.R_OUTER_BULL,
                width=self.R_OUTER_BULL - self.R_INNER_BULL,
                theta1=0,
                theta2=360,
                color=self.COLORS["green"],
                alpha=alpha,
                ec=None,
            ),
            Wedge(
                (0, 0),
                r=self.R_LIMIT_TARGET,
                width=self.R_LIMIT_TARGET - self.R,
                theta1=0,
                theta2=360,
                color=self.COLORS["black"],
                alpha=alpha,
                ec=None,
            ),
        ]
        for i in range(len(thetas) - 1):
            patches.append(
                Wedge(
                    (0, 0),
                    r=self.R_INNER_TRIPLE,
                    width=self.R_INNER_TRIPLE - self.R_OUTER_BULL,
                    theta1=thetas[i],
                    theta2=thetas[i + 1],
                    color=self.COLORS["beige"] if i % 2 == 0 else self.COLORS["black"],
                    alpha=alpha,
                    ec=None,
                )
            )
            patches.append(
                Wedge(
                    (0, 0),
                    r=self.R_INNER_DOUBLE,
                    width=self.R_INNER_DOUBLE - self.R_OUTER_TRIPLE,
                    theta1=thetas[i],
                    theta2=thetas[i + 1],
                    color=self.COLORS["beige"] if i % 2 == 0 else self.COLORS["black"],
                    alpha=alpha,
                    ec=None,
                )
            )
            patches.append(
                Wedge(
                    (0, 0),
                    r=self.R_OUTER_TRIPLE,
                    width=self.R_OUTER_TRIPLE - self.R_INNER_TRIPLE,
                    theta1=thetas[i],
                    theta2=thetas[i + 1],
                    color=self.COLORS["green"] if i % 2 == 0 else self.COLORS["red"],
                    alpha=alpha,
                    ec=None,
                )
            )
            patches.append(
                Wedge(
                    (0, 0),
                    r=self.R,
                    width=self.R - self.R_INNER_DOUBLE,
                    theta1=thetas[i],
                    theta2=thetas[i + 1],
                    color=self.COLORS["green"] if i % 2 == 0 else self.COLORS["red"],
                    alpha=alpha,
                    ec=None,
                )
            )

        for patch in patches:
            self.ax.add_patch(patch)
        for i, num_angle in enumerate(numbers_angles):
            x, y = to_cartesian(1.15 * Target.R, num_angle)
            fp = FontProperties(family="Courier New", style="normal", size=25)
            tp = TextPath((x, y), f"{Target.NUM_SEQUENCE[i]}", prop=fp)
            ap = TextPath(
                (x - tp.get_extents().width / 2, y - tp.get_extents().height / 2),
                f"{Target.NUM_SEQUENCE[i]}",
                prop=fp,
            )
            self.ax.add_patch(PathPatch(ap, color="white"))
        self.ax.axis("equal")
        self.ax.axis("off")
        return self.fig, self.ax

    def __get_number(self, t):
        """
        Return the hitted number
        """
        return self.NUM_SEQUENCE[int((t + self.ANGLE_NUMBER / 2) // self.ANGLE_NUMBER)]

    def __get_multiplication_factor(self, r):
        """
        Returns the multiplication factor
        """
        if r < self.R_INNER_TRIPLE:
            return 1
        elif r < self.R_OUTER_TRIPLE:
            return 3
        elif r < self.R_INNER_DOUBLE:
            return 1
        return 2

    def __return_points(self, x, y):
        """
        x,y : x,y coordinates of the dart
        """
        r, t = to_polar(x, y)
        if r > self.R:
            return 1, 0
        elif r < self.R_INNER_BULL:
            return 1, 50
        elif r < self.R_OUTER_BULL:
            return 1, 25
        factor = self.__get_multiplication_factor(r)
        number = self.__get_number(t)
        return factor, number

    def add_darts(self, nb: int = 1, goal: tuple = None, prec=None):
        if goal is not None:
            xs, ys = np.random.normal(
                loc=goal[0], scale=prec[0], size=nb
            ), np.random.normal(loc=goal[1], scale=prec[1], size=nb)
        else:
            rs, ts = np.random.random(nb) * (1.2 * Target.R), np.random.random(nb) * 360
            xs, ys = to_cartesian(rs, ts)
        factors, numbers = self.return_points(xs, ys)

        new_df = pd.DataFrame(
            {
                "x": xs,
                "y": ys,
                "multi": factors,
                "number": numbers,
                "score": factors * numbers,
            }
        )
        self.df = pd.concat([self.df, new_df], ignore_index=True)

    def reset(self):
        self.df = self.df[0:0]
