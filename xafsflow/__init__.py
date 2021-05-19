"""

"""

from .core import (
    Lasso_analysis,
    bound_xvalues,
    calculate_trunc_matrix,
    read_nor_file,
    sample_name_to_sample_number,
    setup_Xempirical,
)
from .utils import interpolate_frame

try:
    import pkg_resources

    __version__ = pkg_resources.get_distribution("xafsflow").version
except Exception:
    # Local copy or not installed with setuptools.
    # Disable minimum version checks on downstream libraries.
    __version__ = "999"

__author__ = """William P. Krekelberg"""
__email__ = "wpk@nist.gov"


__all__ = [
    "bound_xvalues",
    "Lasso_analysis",
    "calculate_trunc_matrix",
    "setup_Xempirical",
    "read_nor_file",
    "sample_name_to_sample_number",
    "interpolate_frame",
]
