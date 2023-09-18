import matplotlib.pyplot as plt
import numpy as np

from .circle import CIRCLE_5


def show_chords(chords, arrow=False, img_path=None):
    fig, ax = plt.subplots(subplot_kw={"polar": True})
    theta = np.asarray([_.angle_5() for _ in chords])
    r = np.asarray([_.harmony() for _ in chords])
    area = 20 * r ** 2
    colors = theta
    ax.scatter(theta, r, c=colors, s=area, cmap='hsv', alpha=0.75)
    ax.set_xticks(np.arange(0, np.pi*2, np.pi/6), labels=CIRCLE_5.keys)
    ax.set_ybound(0, 7)
    ax.set_yticks(range(0, 7, 1), labels=[])
    if img_path:
        # TODO
        pass
    else:
        plt.show()
