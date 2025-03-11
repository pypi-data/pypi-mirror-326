import numpy as np
import pytest
from scipy.stats import norm

from xlviews.dataframes.dist_frame import DistFrame
from xlviews.dataframes.sheet_frame import SheetFrame
from xlviews.testing import is_excel_installed

pytestmark = pytest.mark.skipif(not is_excel_installed(), reason="Excel not installed")


def test_init_data(sf: SheetFrame):
    from xlviews.dataframes.dist_frame import get_init_data

    df = get_init_data(sf, ["a", "b"], ["x", "y"])
    c = ["a_n", "a_v", "a_s", "b_n", "b_v", "b_s"]
    assert df.columns.to_list() == c
    assert df.index.names == ["x", "y"]
    assert len(df) == 14


@pytest.fixture(scope="module")
def sfd(sf: SheetFrame):
    from xlviews.dataframes.dist_frame import DistFrame

    return DistFrame(sf, ["a", "b"], by=["x", "y"])


@pytest.mark.parametrize(
    ("cell", "value"),
    [
        ("G4", 1),
        ("I4", 1),
        ("J4", 1),
        ("I7", 4),
        ("J7", 4),
        ("I17", 2),
        ("J17", 2),
        ("K4", norm.ppf(1 / 6)),
        ("N5", norm.ppf(2 / 6)),
        ("K6", norm.ppf(3 / 6)),
        ("N7", norm.ppf(4 / 6)),
        ("K8", norm.ppf(5 / 6)),
        ("N16", norm.ppf(1 / 3)),
        ("K17", norm.ppf(2 / 3)),
    ],
)
def test_distframe(sfd: DistFrame, cell: str, value: float):
    v = sfd.sheet[cell].value
    assert v is not None
    np.testing.assert_allclose(v, value)
