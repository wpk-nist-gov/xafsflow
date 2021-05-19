"""
core functionality
"""

from functools import lru_cache
from pathlib import Path

import pandas as pd

# import numpy as np
# import pandas as pd
import xarray as xr
from sklearn.linear_model import LassoCV


def read_nor_file(
    path, sample_dim="sample_name", path_dim=None, ignore_index=True, **kws
):
    """
    reader of nor files(s)

    Parameters
    ----------
    path : str or path or sequence of str or path
        Path to be read in.  If sequence, read in all paths and concat results
    sample_dim : str, optional
        if not note, add basename of path to output with headers `sample_dim`
    path_dim : str, optional
        if present, add path to output frame with column name `path_dim`
    kws : dict : optional arguments to read_csv
        default is comment="#", usecols=[0, 3], names = ['energy','flat']

    """

    kws = dict(
        dict(comment="#", sep=r"\s+", usecols=[0, 3], names=["energy", "flat"]), **kws
    )

    if not isinstance(path, (Path, str)):
        out = pd.concat(
            (read_nor_file(p, sample_dim=sample_dim, path_dim=path_dim) for p in path),
            ignore_index=ignore_index,
        )
    else:
        if not isinstance(path, Path):
            path = Path(path)

        out = pd.read_csv(path, **kws)

        if sample_dim is not None:
            out = out.assign(**{sample_dim: path.with_suffix("").name})
        if path_dim is not None:
            out = out.assign(**{path_dim: path})
    return out


def sample_name_to_sample_number(
    df, sample_name="sample_name", sample_number="sample_number", split="."
):
    """
    transfrom column `sample_name` of form {name}.{number} to
    `sample_name` = {name}, `sampe_number` = {number}
    """

    tmp = df[sample_name].str.split(split).str

    df = df.assign(
        **{sample_name: tmp.get(0), sample_number: tmp.get(1).fillna(-1).astype(int)}
    )

    return df


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


def setup_Xempirical(
    da,
    energy_name="energy",
    sample_name="sample_name",
    sample_class="sample_class",
    standard_name="standard_name",
    standard_class="standard_class",
):
    """
    create a xr.DataArray for Lasso analysis

    Parameters
    ----------
    da : xr.DataArray
        input array
    energy_name : str
        name of energy dimension
    sample_name : str
        name of sample_name dimensions
    sample_class : str
        name of sample_class dimension
    standard_name : str
        rename `sample_name` to `standard_name`
    standard_class : str
        rename `sample_class` to `standard_class`

    Returns
    -------
    out : xr.DataArray
    """

    return da.transpose(energy_name, ...).rename(
        {sample_name: standard_name, sample_class: standard_class}
    )


@lru_cache
def get_default_LassoCVmodel():
    return LassoCV(cv=5, fit_intercept=False, positive=True, max_iter=10000)


def Lasso_analysis(
    X,
    y,
    model=None,
    random_state=None,
    include_coefs=True,
    include_matrix=False,
    as_dataset=True,
    sample_name="sample_name",
    sample_class="sample_class",
    energy_name="energy",
    standard_class="standard_class",
):
    """
    Perform fit analysis on DataArrays

    Parameters
    ----------
    X : xr.DataArray
        input X array
    y : xr.DataArray
        input y array
    model : LassoCV object
        model to fit.  Defaults to output from `get_default_LassoCVModel`
    random_state : int, optional
        if present, set random state of model to this value
    as_dataset : bool, default=True
        if present, output Dataset with `prediction` and `coefs`
    include_coefs : bool, default=True
        if True, include coefficients in output
    include_matrix : bool, default=False

    sample_name, sample_class, ... : str
        name of dimensions

    Returns
    -------
    out : dict or xr.Dataset
    model : LassoCV model
        fit model

    """

    if model is None:
        model = get_default_LassoCVmodel()

    if random_state is not None:
        model.random_state = random_state

    model.fit(X.values, y.values)

    # get prediction
    ypred = y.copy(data=model.predict(X.values))

    out = {"prediction": ypred}

    # get coefficients
    if include_coefs or include_matrix:
        coefs = (
            X.isel(**{energy_name: 0}, drop=True)
            .copy(data=model.coef_)
            .rename("coefs")
            .assign_coords(sample_name=y.sample_name)
        )
        out["coefs"] = coefs

        if include_matrix:
            matrix = coefs / coefs.sum()
            trunc_matrix = matrix.groupby(
                matrix[standard_class]
            ).sum()  # .sel(sample_class=categories)
            out["matrix"] = matrix
            out["trunc_matrix"] = trunc_matrix

    if as_dataset:
        out = xr.Dataset(out)

    return out, model


def calculate_trunc_matrix(
    coefs, standard_name="standard_name", standard_class="standard_class"
):
    # Calculate trunc_matrix
    return coefs.pipe(lambda x: x / x.sum(standard_name)).pipe(
        lambda x: x.groupby(x[standard_class]).sum()
    )
