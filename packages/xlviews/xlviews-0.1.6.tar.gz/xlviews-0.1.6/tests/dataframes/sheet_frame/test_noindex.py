import numpy as np
import pytest
from pandas import DataFrame, Series
from xlwings import Sheet

from xlviews.dataframes.groupby import groupby
from xlviews.dataframes.sheet_frame import SheetFrame
from xlviews.testing import FrameContainer, is_excel_installed
from xlviews.testing.sheet_frame import NoIndex

pytestmark = pytest.mark.skipif(not is_excel_installed(), reason="Excel not installed")


@pytest.fixture(scope="module")
def fc(sheet_module: Sheet):
    return NoIndex(sheet_module, 2, 3)


@pytest.fixture(scope="module")
def df(fc: FrameContainer):
    return fc.df


@pytest.fixture(scope="module")
def sf(fc: FrameContainer):
    return fc.sf


def test_expand(sf: SheetFrame):
    v = [[None, "a", "b"], [0, 1, 5], [1, 2, 6], [2, 3, 7], [3, 4, 8]]
    assert sf.cell.expand().options(ndim=2).value == v


def test_attrs(sf: SheetFrame, fc: FrameContainer):
    assert sf.row == fc.row
    assert sf.column == fc.column
    assert sf.index_level == 1
    assert sf.columns_level == 1


def test_set_data_from_sheet(sf: SheetFrame):
    sf.set_data_from_sheet(index_level=1, number_format="0")
    assert sf.has_index is True
    assert sf.index_level == 1


def test_len(sf: SheetFrame):
    assert len(sf) == 4


def test_columns(sf: SheetFrame):
    assert sf.columns == [None, "a", "b"]


def test_value_columns(sf: SheetFrame):
    assert sf.value_columns == ["a", "b"]


def test_index_columns(sf: SheetFrame):
    assert sf.index_columns == [None]


def test_index_false(sheet: Sheet):
    df = DataFrame({"a": [1, 2], "b": [2, 4]})
    sf = SheetFrame(2, 3, data=df, index=False, style=False, sheet=sheet)
    assert sf.columns == ["a", "b"]
    assert sf.index_level == 0


def test_row_one(sheet: Sheet):
    df = DataFrame({"a": [1], "b": [2]})
    sf = SheetFrame(2, 2, data=df, style=False, sheet=sheet)
    assert len(sf) == 1
    np.testing.assert_array_equal(sf["a"], [1])


def test_column_one(sheet: Sheet):
    df = DataFrame({"a": [1, 2, 3]})
    sf = SheetFrame(2, 2, data=df, style=False, index=False, sheet=sheet)
    assert len(sf) == 3
    assert sf.columns == ["a"]
    np.testing.assert_array_equal(sf["a"], [1, 2, 3])


def test_contains(sf: SheetFrame):
    assert "a" in sf
    assert "x" not in sf


@pytest.mark.parametrize(
    ("column", "relative", "index"),
    [
        ("a", True, 2),
        ("a", False, 4),
        ("b", True, 3),
        ("b", False, 5),
        (["a", "b"], True, [2, 3]),
        (["a", "b"], False, [4, 5]),
    ],
)
def test_index(sf: SheetFrame, column, relative, index):
    assert sf.index(column, relative=relative) == index


def test_data(sf: SheetFrame, df: DataFrame):
    df_ = sf.data
    np.testing.assert_array_equal(df_.index, df.index)
    np.testing.assert_array_equal(df_.index.names, df.index.names)
    np.testing.assert_array_equal(df_.columns, df.columns)
    np.testing.assert_array_equal(df_.columns.names, df.columns.names)
    np.testing.assert_array_equal(df_, df)
    assert df_.index.name == df.index.name
    assert df_.columns.name == df.columns.name


def test_range_all(sf: SheetFrame):
    assert sf._range_all(True).get_address() == "$C$2:$E$6"
    assert sf.range().get_address() == "$C$2:$E$6"


def test_range_all_index_false(sf: SheetFrame):
    assert sf._range_all(False).get_address() == "$D$3:$E$6"
    assert sf.range(index=False).get_address() == "$D$3:$E$6"


@pytest.mark.parametrize(
    ("start", "end", "address"),
    [
        (False, None, "$C$2:$C$6"),
        (-1, None, "$C$2"),
        (0, None, "$C$3"),
        (None, None, "$C$3:$C$6"),
        (10, None, "$C$10"),
        (10, 100, "$C$10:$C$100"),
    ],
)
def test_range_index(sf: SheetFrame, start, end, address):
    assert sf._range_index(start, end).get_address() == address
    assert sf.range("index", start, end).get_address() == address


@pytest.mark.parametrize(
    ("column", "start", "end", "address"),
    [
        ("a", -1, None, "$D$2"),
        ("b", -1, None, "$E$2"),
        ("a", 1, None, "$D$1"),
        ("a", 2, None, "$D$2"),
        ("b", 100, None, "$E$100"),
        ("a", None, None, "$D$3:$D$6"),
        ("a", False, None, "$D$2:$D$6"),
        ("b", False, None, "$E$2:$E$6"),
        ("a", 2, 100, "$D$2:$D$100"),
    ],
)
def test_range_column(sf: SheetFrame, column, start, end, address):
    assert sf._range_column(column, start, end).get_address() == address
    assert sf.range(column, start, end).get_address() == address


def test_repr(sf: SheetFrame):
    assert repr(sf).endswith("!$C$2:$E$6>")


def test_str(sf: SheetFrame):
    assert str(sf).endswith("!$C$2:$E$6>")


def test_rename(sheet: Sheet):
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    sf = SheetFrame(2, 2, data=df, style=False, sheet=sheet)
    sf.rename({"a": "A", "b": "B"})
    assert sf.columns == [None, "A", "B"]


def test_drop_duplicates(sheet: Sheet):
    df = DataFrame({"a": [1, 1, 2, 2, 3, 3], "b": [4, 4, 4, 5, 5, 5]})
    sf = SheetFrame(2, 2, data=df, style=False, sheet=sheet)
    sf.drop_duplicates(["a", "b"])
    x = sf["a"]
    assert x[::2].to_list() == [1, 2, 3]
    assert x[1::2].isna().all()
    x = sf["b"]
    assert x[::3].to_list() == [4, 5]
    assert x[1::3].isna().all()
    assert x[2::3].isna().all()


def test_add_column(sheet: Sheet):
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    sf = SheetFrame(2, 2, data=df, style=False, sheet=sheet)
    rng = sf.add_column("c")
    assert rng.get_address() == "$E$3:$E$5"
    assert sf.columns == [None, "a", "b", "c"]


def test_add_column_value(sheet: Sheet):
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    sf = SheetFrame(2, 2, data=df, style=False, sheet=sheet)
    sf.add_column("c", [7, 8, 9])
    np.testing.assert_array_equal(sf["c"], [7, 8, 9])


def test_getitem_str(sf: SheetFrame):
    s = sf["a"]
    assert isinstance(s, Series)
    assert s.name == "a"
    np.testing.assert_array_equal(s, [1, 2, 3, 4])


def test_getitem_list(sf: SheetFrame):
    df = sf[["a", "b"]]
    assert isinstance(df, DataFrame)
    assert df.columns.to_list() == ["a", "b"]
    x = [[1, 5], [2, 6], [3, 7], [4, 8]]
    np.testing.assert_array_equal(df, x)


def test_setitem(sheet: Sheet):
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    sf = SheetFrame(2, 2, data=df, style=False, sheet=sheet)
    x = [10, 20, 30]
    sf["a"] = x
    np.testing.assert_array_equal(sf["a"], x)


def test_setitem_new_column(sheet: Sheet):
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    sf = SheetFrame(2, 2, data=df, style=False, sheet=sheet)
    x = [10, 20, 30]
    sf["c"] = x
    assert sf.columns == [None, "a", "b", "c"]
    np.testing.assert_array_equal(sf["c"], x)


@pytest.mark.parametrize(
    ("a", "b", "sel"),
    [
        (1, None, [True, False, False, False]),
        (3, None, [False, False, True, False]),
        ([2, 4], None, [False, True, False, True]),
        ((2, 4), None, [False, True, True, True]),
        (1, 5, [True, False, False, False]),
        (1, 6, [False, False, False, False]),
        ((1, 3), (6, 8), [False, True, True, False]),
    ],
)
def test_select(sf: SheetFrame, a, b, sel):
    if b is None:
        np.testing.assert_array_equal(sf.select(a=a), sel)
    else:
        np.testing.assert_array_equal(sf.select(a=a, b=b), sel)


def test_address(sf: SheetFrame):
    s = sf.get_address("a")
    assert isinstance(s, Series)
    assert s.to_list() == ["$D$3", "$D$4", "$D$5", "$D$6"]
    assert s.name == "a"


def test_address_formula(sf: SheetFrame):
    s = sf.get_address("a", formula=True)
    assert s.to_list() == ["=$D$3", "=$D$4", "=$D$5", "=$D$6"]


@pytest.mark.parametrize("columns", [["a", "b"], ["b", "a"], None])
def test_address_list_or_none(sf: SheetFrame, columns):
    df = sf.get_address(columns)
    assert isinstance(df, DataFrame)
    assert df.shape == (4, 2)
    assert df["a"].to_list() == ["$D$3", "$D$4", "$D$5", "$D$6"]
    assert df["b"].to_list() == ["$E$3", "$E$4", "$E$5", "$E$6"]
    assert df.index.to_list() == list(range(4))
    assert df.index.name is None


def test_groupby(sheet: Sheet):
    df = DataFrame({"a": [1, 1, 1, 2, 2, 1, 1], "b": [1, 2, 3, 4, 5, 6, 7]})
    sf = SheetFrame(2, 2, data=df, style=False, index=False, sheet=sheet)

    g = groupby(sf, "a")
    assert len(g) == 2
    assert g[(1,)] == [(3, 5), (8, 9)]
    assert g[(2,)] == [(6, 7)]

    assert len(groupby(sf, ["a", "b"])) == 7

    g = groupby(sf, "::b")
    assert len(g) == 2
    assert g[(1,)] == [(3, 5), (8, 9)]
    assert g[(2,)] == [(6, 7)]

    assert len(groupby(sf, ":b")) == 7


def test_groupby_range(sheet: Sheet):
    df = DataFrame({"a": [1, 1, 1, 2, 2, 1, 1], "b": [3, 3, 4, 4, 3, 3, 4]})
    sf = SheetFrame(2, 2, data=df, style=False, index=False, sheet=sheet)

    g = groupby(sf, "a")
    assert sf.range("a", g[(1,)]).get_address() == "$B$3:$B$5,$B$8:$B$9"
    assert sf.range("a", g[(2,)]).get_address() == "$B$6:$B$7"

    g = groupby(sf, "b")
    assert sf.range("b", g[(3,)]).get_address() == "$C$3:$C$4,$C$7:$C$8"
    assert sf.range("b", g[(4,)]).get_address() == "$C$5:$C$6,$C$9"

    g = groupby(sf, ["a", "b"])
    assert sf.range("a", g[(1, 3)]).get_address() == "$B$3:$B$4,$B$8"
    assert sf.range("a", g[(1, 4)]).get_address() == "$B$5,$B$9"
    assert sf.range("a", g[(2, 3)]).get_address() == "$B$7"
    assert sf.range("a", g[(2, 4)]).get_address() == "$B$6"
