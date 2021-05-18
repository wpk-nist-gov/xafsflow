# import numpy as np
import pandas as pd


def interpolate_frame(
    df,
    x,
    x_dim,
    by=None,
    by_kws=None,
    method="index",
    mask_minmax=True,
    sort_index=True,
    ret_all=False,
    **kwargs
):
    """
    interpolate a dataframe at x

    Parameters
    ----------

    df : DataFrame
      DataFrame to interpolate (all columns other than x_dim
      are interpolated)

    x : array
      values to interpolate at

    x_dim : str
      column to interpolate over

    by : str, or list of strings, optional
        if present, do groupby

    by_kws : dict
        extra arguments to df.groupby

    method : str
      method for interpolation (see pandas.DataFrame.interpolate
      options)

    ret_all: bool
      if True, return all.
      else only at interpolated points "x"

    assumes df is indexed in same way as index_df
    """

    if by:
        if by_kws is None:
            by_kws = {}

        if isinstance(by, str):
            by = [by]

        # exclude = by + [x_dim]
        exclude = by
        cols = [k for k in df.columns if k not in exclude]

        out = df.groupby(by, **by_kws)[cols].apply(
            lambda g: interpolate_frame(
                g,
                x=x,
                x_dim=x_dim,
                by=None,
                method=method,
                mask_minmax=mask_minmax,
                sort_index=sort_index,
                ret_all=ret_all,
                **kwargs
            )
        )

    else:
        # get min/max values along x_dim
        if mask_minmax:
            minx = df[x_dim].min()
            maxx = df[x_dim].max()
            xx = x[(minx <= x) & (x <= maxx)]
        else:
            xx = x

        # set index
        t = df.set_index(x_dim)

        # new index from union of indicies
        idx_df = t.index
        idx_x = pd.Index(xx, name=idx_df.name)
        idx_union = idx_df.union(idx_x).drop_duplicates()

        # reindex
        t = t.reindex(idx_union)
        # end new way

        if sort_index:
            t = t.sort_index()

        # interpolate over index (linear interpolation)
        t = t.interpolate(method=method, **kwargs)

        if not ret_all:
            t = t.reindex(idx_x)

        # t = t.reset_index()#x_dim)

        out = t

    return out


# def interpolate_DataFrame_group(
#     df,
#     x,
#     x_dim,
#     by,
#     y_dims=None,
#     groupby_kws=None,
#     mask_minmax=True,
#     sort_index=True,
#     ret_all=False,
#     **kwargs
# ):
#     """
#     interpolate dataframe along single column with grouping

#     Parameters
#     ----------
#     df : Dataframe

#     x : array-like
#         values to interplate at

#     x_dim : str
#         name of column to interpolate along

#     by : str on list-like
#         column name(s) to group by

#     method : string
#         method for interplation (see pandas.DataFrame.interpolate)

#     ret_all : bool
#         if True, return all,
#         else, return at interpolated points
#     """

#     L = []
#     by = list(np.atleast_1d(by))

#     if groupby_kws is None:
#         groupby_kws = {}

#     for v, g in df.groupby(by, **groupby_kws):

#         # setup values to assign back to frame

#         vv = np.atleast_1d(np.array(v, dtype=np.object))
#         d = dict(zip(by, vv))

#         L.append(
#             interpolate_DataFrame(
#                 df=g.drop(by, axis=1),
#                 x=x,
#                 x_dim=x_dim,
#                 mask_minmax=mask_minmax,
#                 sort_index=sort_index,
#                 ret_all=ret_all,
#                 **kwargs
#             ).assign(**d)
#         )

#     return pd.concat(L)


# from scipy.interpolate import interp1d


# def _apply_interp1d(
#         df,
#         x_dim,
#         y_dim=None,
#         skip_dims=None,
# ):


# def apply_func_over_groups(
#     func,
#     df,
#     by=None,
#     x_dim="Time [Sec]",
#     y_dim=None,
#     drop_unused=False,
#     reduction=True,
#     **kws,
# ):
#     if y_dim is None:
#         if by is None:
#             col_drop = [x_dim]
#         elif isinstance(by, str):
#             col_drop = [x_dim, by]
#         else:
#             col_drop = [x_dim] + list(by)
#         y_dim = [x for x in df.columns if x not in col_drop]
#     elif isinstance(y_dim, str):
#         y_dim = [y_dim]

#     if by is None:
#         if reduction:
#             if drop_unused:
#                 out = df.iloc[[0], :].loc[:, y_dim].copy()
#             else:
#                 out = df.iloc[[0], :].drop(x_dim, axis=1)
#         else:
#             if drop_unused:
#                 if x_dim in df.columns:
#                     out = df.loc[:, [x_dim] + y_dim].copy()
#                 else:
#                     out = df.loc[:, y_dim].copy()
#             else:
#                 out = df.copy()

#         out.loc[:, y_dim] = func(df, x_dim, y_dim, **kws)

#         # xvals = _get_col_or_level(df, x_dim).values
#         # out.loc[:, y_dim] = trapz(y_dim=df.loc[:, y_dim].values, x_dim=xvals, axis=0)
#     else:
#         out = pd.concat(
#             (
#                 apply_func_over_groups(
#                     func=func,
#                     df=g,
#                     by=None,
#                     x_dim=x_dim,
#                     y_dim=y_dim,
#                     drop_unused=drop_unused,
#                     reduction=reduction,
#                     **kws,
#                 )
#                 for _, g in df.groupby(by, sort=False)
#             )
#         )
#     return out


# def _func_interp1d(df, x, y), **kws:
#     xvals = _get_col_or_level(df, x).values
#     out = interp1d(xvals, df.loc[:, y], **kws)
#     return out


# def interp1d_frame(df, x, by=None, x_dim="e", y_dim='flat', drop_unused=False, **kws):
#     """
#     apply interp1d
#     """

#     if y_dim is None:
#         if by is None:
#             col_drop = [x_dim]
#         elif isinstance(by, str):
#             col_drop = [x_dim, by]
#         else:
#             col_drop = [x_dim] + list(by)
#         y_dim = [x for x in df.columns if x not in col_drop]
#     elif isinstance(y_dim, str):
#         y_dim = [y_dim]

#     if by is None:
#         if drop_unused:
#             if x_dim in df.columns:
#                 out = df.loc[:, [x_dim] + y_dim].copy()
#             else:
#                 out = df.loc[:, y_dim].copy()
#         else:
#             out = df.copy()

#         out.loc[:, y_dim] = func(df, x_dim, y_dim, **kws)

#         # xvals = _get_col_or_level(df, x_dim).values
#         # out.loc[:, y_dim] = trapz(y_dim=df.loc[:, y_dim].values, x_dim=xvals, axis=0)
#     else:
#         out = pd.concat(
#             (
#                 interp1d_frame(
#                     func=func,
#                     df=g,
#                     by=None,
#                     x_dim=x_dim,
#                     y_dim=y_dim,
#                     drop_unused=drop_unused,
#                     reduction=reduction,
#                     **kws,
#                 )
#                 for _, g in df.groupby(by, sort=False)
#             )
#         )
#     return out

#     return apply_func_over_groups(
#         func=_func_argmin,
#         df=df,
#         by=by,
#         x_dim=x_dim,
#         y_dim=y_dim,
#         drop_unused=drop_unused,
#         reduction=True,
#     )
