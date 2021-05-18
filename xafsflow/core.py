"""
core functionality
"""

# import numpy as np
# import pandas as pd
# import xarray as xr


def bound_xvalues(frame, x, x_dim, by):
    """
    bound `x` to be within min/max of frame[x_dim]

    Parameters
    ----------
    frame : dataframe
    x : array
    x_dim : str
    by : str or sequence of str
    """

    t = frame.groupby(by)[x_dim].agg(["min", "max"])
    lb = t["min"].max()
    ub = t["max"].min()

    return x[(x >= lb) & (x <= ub)]
