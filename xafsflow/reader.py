from pathlib import Path

import pandas as pd


def read_nor_file(path, sample_dim="sample_name", ignore_index=True, **kws):
    """
    reader of nor files(s)

    Parameters
    ----------
    path : str or path or sequence of str or path
        Path to be read in.  If sequence, read in all paths and concat results
    sample_dim : str, optional
        if not note, add basename of path to output with headers `sample_dim`
    kws : dict : optional arguments to read_csv
        default is comment="#", usecols=[0, 3], names = ['energy','flat']

    """

    kws = dict(
        dict(comment="#", sep=r"\s+", usecols=[0, 3], names=["energy", "flat"]), **kws
    )

    if not isinstance(path, (Path, str)):
        out = pd.concat((read_nor_file(p) for p in path), ignore_index=ignore_index)
    else:
        if not isinstance(path, Path):
            path = Path(path)

        out = pd.read_csv(path, **kws)

        if sample_dim is not None:
            out = out.assign(**{sample_dim: path.with_suffix("").name})
    return out
