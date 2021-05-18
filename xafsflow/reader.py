from pathlib import Path

import pandas as pd


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

    tmp = df[sample_name].str.split(split).str

    df = df.assign(
        **{sample_name: tmp.get(0), sample_number: tmp.get(1).fillna(-1).astype(int)}
    )

    return df
