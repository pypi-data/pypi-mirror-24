"""Sample package for demonstrating flit & flonda.

This code is from the matplotlib gallery, used under the matplotlib license.
http://matplotlib.org/examples/images_contours_and_fields/streamplot_demo_features.html
http://matplotlib.org/users/license.html
"""

import numpy as np
import matplotlib.pyplot as plt

__version__ = '0.1'

def make_streamplot():
    Y, X = np.mgrid[-3:3:100j, -3:3:100j]
    U = -1 - X**2 + Y
    V = 1 + X - Y**2
    speed = np.sqrt(U*U + V*V)

    fig0, ax0 = plt.subplots()
    strm = ax0.streamplot(X, Y, U, V, color=U, linewidth=2, cmap=plt.cm.autumn)
    fig0.colorbar(strm.lines)
    return fig0
