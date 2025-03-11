"""DataFrame on an Excel sheet."""

from __future__ import annotations

import re
from functools import partial
from itertools import chain, takewhile
from typing import TYPE_CHECKING, TypeAlias, overload

import numpy as np
import xlwings as xw
from pandas import DataFrame, Index, MultiIndex, Series
from xlwings import Range, Sheet

from xlviews.chart.axes import set_first_position
from xlviews.decorators import turn_off_screen_updating
from xlviews.element import Bar, Plot, Scatter
from xlviews.grid import FacetGrid
from xlviews.range.address import iter_addresses
from xlviews.range.formula import aggregate
from xlviews.range.range_collection import RangeCollection
from xlviews.range.style import set_alignment

from . import modify
from .groupby import GroupBy
from .style import set_frame_style, set_wide_column_style
from .table import Table

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator, Sequence
    from typing import Any, Literal

    from numpy.typing import ArrayLike, NDArray

    from .dist_frame import DistFrame
    from .stats_frame import StatsFrame

Func: TypeAlias = str | Range | None


class SheetFrame:
    """Data frame on an Excel sheet."""

    sheet: Sheet
    cell: Range
    name: str | None
    has_index: bool
    index_level: int
    columns_level: int
    columns_names: list[str] | None = None
    table: Table | None = None
    parent: SheetFrame | None
    children: list[SheetFrame]
    head: SheetFrame | None
    tail: SheetFrame | None = None
    stats: StatsFrame | None = None
    dist: DistFrame | None = None

    @turn_off_screen_updating
    def __init__(
        self,
        *args,
        name: str | None = None,
        sheet: Sheet | None = None,
        parent: SheetFrame | None = None,
        head: SheetFrame | None = None,
        data: DataFrame | Series | None = None,
        index: bool = True,
        index_level: int = 1,
        columns_level: int = 1,
        style: bool = True,
        gray: bool = False,
        autofit: bool = True,
        number_format: str | None = None,
        font_size: int | None = None,
        table: bool = False,
        **kwargs,
    ) -> None:
        """Create a DataFrame on an Excel sheet.

        Args:
            sheet (Sheet): The sheet object.
            row, column (int): The position of the top-left cell.
            cell (Range): The Range of the top-left cell.
            data (DataFrame, optional): The DataFrame to write to the sheet.
            index (bool): Whether to output the index of the DataFrame.
            index_level (int): The depth of the index when importing data
                from the sheet.
            column_level (int): The depth of the columns when importing data
                from the sheet.
            parent (SheetFrame): The parent SheetFrame.
                The child SheetFrame is placed to the right of the parent SheetFrame.
                The parent SheetFrame represents the information extracted
                from the parent.
            head (SheetFrame): The upper SheetFrame.
                The child SheetFrame is placed below the upper SheetFrame.
                The upper SheetFrame represents the additional information
                of the parent.
            style (bool): Whether to decorate the SheetFrame.
            gray (bool): Whether to decorate the SheetFrame in gray.
            autofit (bool): Whether to autofit the SheetFrame.
            number_format (str): The number format of the SheetFrame.
            font_size (int): The font size of the SheetFrame.
        """
        self.name = name
        self.parent = parent
        self.children = []
        self.head = head

        if self.parent:  # Locate the child frame to the right of the parent frame.
            self.cell = self.parent.get_child_cell()
            self.parent.add_child_frame(self)

        elif self.head:  # Locate the child frame below the head frame.
            row_offset = len(self.head) + self.head.columns_level + 1
            self.cell = self.head.cell.offset(row_offset, 0)
            self.head.tail = self

        else:
            sheet = sheet or xw.sheets.active
            self.cell = sheet.range(*args)

        self.sheet = self.cell.sheet

        if data is not None:
            self.set_data(
                data,
                index=index,
                number_format=number_format,
                style=style,
                gray=gray,
                autofit=autofit,
                font_size=font_size,
                **kwargs,
            )
        else:
            self.set_data_from_sheet(
                index_level=index_level,
                columns_level=columns_level,
                number_format=number_format,
            )

        if table and not self.table:
            self.table = self.as_table()

    def set_data(
        self,
        data: DataFrame | Series,
        *,
        index: bool = True,
        number_format: str | None = None,
        style: bool = True,
        gray: bool = False,
        autofit: bool = True,
        font_size: int | None = None,
        **kwargs,
    ) -> None:
        if isinstance(data, Series):
            data = data.to_frame()

        self.has_index = index
        self.index_level = len(data.index.names) if index else 0
        self.columns_level = len(data.columns.names)

        self.cell.options(DataFrame, index=index).value = data

        if index and data.columns.nlevels > 1 and data.index.nlevels == 1:
            self.columns_names = list(data.columns.names)
            self.cell.options(transpose=True).value = self.columns_names

        if number_format:
            self.set_number_format(number_format)

        if style:
            self.set_style(gray=gray, autofit=autofit, font_size=font_size, **kwargs)

        if self.name:
            book = self.sheet.book
            refers_to = "=" + self.cell.get_address(include_sheetname=True)
            book.names.add(self.name, refers_to)

    def set_data_from_sheet(
        self,
        *,
        index_level: int = 1,
        columns_level: int = 1,
        number_format: str | None = None,
    ) -> None:
        if self.name:
            book = self.sheet.book
            self.cell = book.names[self.name].refers_to_range
            self.sheet = self.cell.sheet

        self.has_index = bool(index_level)
        self.index_level = index_level
        self.columns_level = columns_level

        if self.columns_level > 1 and index_level == 1:
            start = self.cell
            end = start.offset(self.columns_level - 1)
            self.columns_names = self.sheet.range(start, end).value

        if number_format:
            self.set_number_format(number_format)

        for api in self.sheet.api.ListObjects:
            if api.Range.Row == self.row and api.Range.Column == self.column:
                self.table = Table(api=api, sheet=self.sheet)
                break

    def __len__(self) -> int:
        start = self.cell.offset(self.columns_level)
        cell = start

        while cell.value is not None:
            cell = cell.expand("down")[-1].offset(1)

        return cell.row - start.row

    def _update_cell(self) -> None:  # important
        self.cell = self.cell.offset(0, 0)

    def expand(self, mode: str = "table") -> Range:
        self._update_cell()
        return self.cell.expand(mode)

    @property
    def row(self) -> int:
        """Return the row of the top-left cell."""
        self._update_cell()
        return self.cell.row

    @property
    def column(self) -> int:
        """Return the column of the top-left cell."""
        self._update_cell()
        return self.cell.column

    @property
    def columns(self) -> list:
        """Return the column names."""
        if self.columns_level == 1:
            return self.expand("right").options(ndim=1).value or []

        if self.columns_names:
            idx = [tuple(self.columns_names)]
        elif self.has_index:
            start = self.cell.offset(self.columns_level - 1)
            end = start.offset(0, self.index_level - 1)
            idx = self.sheet.range(start, end).value or []
        else:
            idx = []

        cs = []
        for k in range(self.columns_level):
            rng = self.cell.offset(k, self.index_level).expand("right")
            cs.append(rng.options(ndim=1).value)
        cs = [tuple(c) for c in zip(*cs, strict=True)]

        return [*idx, *cs]

    @property
    def value_columns(self) -> list:
        return self.columns[self.index_level :]

    @property
    def index_columns(self) -> list[str | tuple[str, ...] | None]:
        return self.columns[: self.index_level]

    @property
    def wide_columns(self) -> list[str]:
        start = self.cell.offset(-1, self.index_level)
        end = start.offset(0, len(self.columns) - self.index_level - 1)
        cs = self.sheet.range(start, end).value or []
        return [c for c in cs if c]

    def __contains__(self, item: str | tuple) -> bool:
        return item in self.columns

    def __iter__(self) -> Iterator[str | tuple[str, ...] | None]:
        return iter(self.columns)

    @overload
    def index(
        self,
        columns: str | tuple,
        *,
        relative: bool = False,
    ) -> int | tuple[int, int]: ...

    @overload
    def index(
        self,
        columns: list[str | tuple],
        *,
        relative: bool = False,
    ) -> list[int] | list[tuple[int, int]]: ...

    def index(
        self,
        columns: str | tuple | list[str | tuple],
        *,
        relative: bool = False,
    ) -> int | tuple[int, int] | list[int] | list[tuple[int, int]]:
        """Return the column index (1-indexed).

        If the column is a hierarchical index and the column name is specified,
        return the row index. If relative is True, return the relative position
        from `self.cell`.
        """
        if isinstance(columns, str | tuple):
            return self.index([columns], relative=relative)[0]

        if self.columns_names:
            columns_str = [c for c in columns if isinstance(c, str)]
            if len(columns_str) == len(columns):
                return self._index_row(columns_str, relative=relative)

        idx = []
        columns_ = self.columns
        offset = 1 if relative else self.column

        for column in columns:
            if column in columns_:
                idx.append(columns_.index(column) + offset)
            else:
                idx.append(self._index_wide(column, relative=relative))

        return idx

    def _index_row(
        self,
        columns: list[str],
        *,
        relative: bool = False,
    ) -> list[int]:
        if not self.columns_names:
            raise ValueError("columns names are not specified")

        columns_names = self.columns_names
        offset = 1 if relative else self.row
        return [columns_names.index(c) + offset for c in columns]

    def _index_wide(
        self,
        column: str | tuple[str, str | float],
        *,
        relative: bool = False,
    ) -> tuple[int, int] | int:
        value_columns = self.value_columns

        cell_start = self.cell.offset(-1, self.index_level)
        cell_end = cell_start.offset(0, len(value_columns) - 1)
        names = self.sheet.range(cell_start, cell_end).options(ndim=1).value or []

        name = column[0] if isinstance(column, tuple) else column
        start = names.index(name)
        end = len(list(takewhile(lambda n: n is None, names[start + 1 :]))) + start

        offset = self.index_level + (1 if relative else self.cell.column)

        if isinstance(column, str):
            return start + offset, end + offset

        values = value_columns[start : end + 1]
        return values.index(column[1]) + start + offset

    @property
    def data(self) -> DataFrame:
        """Return the data as a DataFrame."""
        if self.cell.value is None and self.columns_level > 1:
            rng = self.cell.offset(self.columns_level - 1).expand()
            rng = rng.options(DataFrame, index=self.index_level, header=1)
            df = rng.value
            df.columns = MultiIndex.from_tuples(self.value_columns)
            return df

        rng = self.expand().options(
            DataFrame,
            index=self.index_level,
            header=self.columns_level,
        )
        df = rng.value

        if not isinstance(df, DataFrame):
            raise NotImplementedError

        if self.columns_names:
            df.index.name = None
            df.columns.names = self.columns_names

        return df

    @property
    def visible_data(self) -> DataFrame:
        self._update_cell()
        start = self.cell.offset(1, 0)
        end = start.offset(len(self) - 1, len(self.columns) - 1)
        range_ = self.sheet.range(start, end)
        data = range_.api.SpecialCells(xw.constants.CellType.xlCellTypeVisible)
        value = [row.Value[0] for row in data.Rows]
        df = DataFrame(value, columns=self.columns)

        if self.has_index and self.index_level:
            df = df.set_index(list(df.columns[: self.index_level]))

        return df

    def as_table(
        self,
        *,
        const_header: bool = True,
        autofit: bool = True,
        style: bool = True,
    ) -> Table:
        if self.columns_level != 1:
            raise NotImplementedError

        self.set_alignment("left")

        end = self.cell.offset(len(self), len(self.columns) - 1)
        rng = self.sheet.range(self.cell, end)

        table = Table(rng, autofit=autofit, const_header=const_header, style=style)
        self.table = table

        return table

    def unlist(self) -> None:
        if self.table:
            self.table.unlist()
            self.table = None

    @overload
    def range(
        self,
        column: str | tuple | None = None,
        start: int | Literal[False] | None = None,
        end: int | None = None,
        index: bool = True,
    ) -> Range: ...

    @overload
    def range(
        self,
        column: str | tuple,
        start: list[tuple[int, int]],
        end: int | None = None,
        index: bool = True,
    ) -> RangeCollection: ...

    def range(
        self,
        column: str | tuple | None = None,
        start: int | Literal[False] | list[tuple[int, int]] | None = None,
        end: int | None = None,
        index: bool = True,
    ) -> Range | RangeCollection:
        """Return the range of the column.

        If the column is a hierarchical index and the column name is specified,
        return the range of the column.

        Args:
            column (str or tuple, optional): The name of the column.
                If omitted, return the range of the entire SheetFrame.
            start (int, optional):
                - None: entire row data without column row
                - 0: first row
                - -1: column row
                - False: entire row with column row
                - other: specified row
            end (int, optional):
                - None : same as start.
                - other: specified row
        """
        if column is None:
            return self._range_all(index)

        if isinstance(start, list):
            return RangeCollection(self.range(column, s, e) for s, e in start)

        if column == "index":
            return self._range_index(start, end)

        return self._range_column(column, start, end)

    def _range_all(self, index: bool) -> Range:
        start = self.cell
        row_offset = self.columns_level + len(self) - 1
        column_offset = self.index_level + len(self.value_columns) - 1
        end = start.offset(row_offset, column_offset)

        if not index:
            start = start.offset(self.columns_level, self.index_level)

        return self.sheet.range(start, end)

    def _range_index(
        self,
        start: int | Literal[False] | None = None,
        end: int | None = None,
    ) -> Range:
        """Return the range of the index."""
        if not self.index_level:
            raise NotImplementedError

        if self.columns_names and (start in [-1, None] or start is False):
            raise ValueError("index start must be a specific row")

        c = self.index_level - 1
        match start:
            case False:  # entire row with column row
                cell_start = self.cell
                cell_end = cell_start.offset(self.columns_level + len(self) - 1, c)

            case 0:  # first row
                cell_start = self.cell.offset(self.columns_level)
                cell_end = cell_start.offset(0, c)

            case -1:  # column row
                cell_start = self.cell
                cell_end = cell_start.offset(self.columns_level - 1, c)

            case None:  # entire row data without column row
                cell_start = self.cell.offset(self.columns_level)
                cell_end = cell_start.offset(len(self) - 1, c)

            case _:
                column = self.cell.column
                cell_start = self.sheet.range(start, column)
                cell_end = self.sheet.range(end or start, column + c)

        return self.sheet.range(cell_start, cell_end)

    def _range_column(  # noqa: C901
        self,
        column: str | tuple,
        start: int | Literal[False] | None = None,
        end: int | None = None,
    ) -> Range:
        if self.columns_names and isinstance(column, str):
            raise NotImplementedError

        if start is False:  # entire row with column row
            header = self._range_column(column, -1)
            values = self._range_column(column)
            return self.sheet.range(header[0], values[-1])

        index = self.index(column)

        match start:
            case 0:  # first row
                start = self.row + self.columns_level

            case -1:  # column row
                start = end = self.row
                if isinstance(column, tuple) and self.columns_level == 1:
                    start -= 1  # wide column
                else:
                    end += self.columns_level - 1
                    if isinstance(index, tuple):
                        start -= 1

            case None:  # entire row data without column row
                start = self.row + self.columns_level
                end = start + len(self) - 1

        if isinstance(index, tuple):  # wide column
            column_start, column_end = index
        else:
            column_start = column_end = index

        cell_start = self.sheet.range(start, column_start)

        if end is None:
            if not isinstance(index, tuple):
                return cell_start

            # wide column
            cell_end = cell_start.offset(0, column_end - column_start)
            return self.sheet.range(cell_start, cell_end)

        cell_end = self.sheet.range(end, column_end)
        return self.sheet.range(cell_start, cell_end)

    def first_range(self, column: str | tuple) -> Range:
        return self.range(column, 0)

    def __repr__(self) -> str:
        return repr(self.range()).replace("<Range ", "<SheetFrame ")

    def __str__(self) -> str:
        return str(self.range()).replace("<Range ", "<SheetFrame ")

    def rename(self, columns: dict[str, str]) -> None:
        """Rename the columns of the SheetFrame."""
        for old, new in columns.items():
            self.range(old, -1).value = new

    def drop_duplicates(self, column: str | tuple | Iterable[str | tuple]) -> None:
        columns = [column] if isinstance(column, str | tuple) else list(column)

        for column in columns:
            for cell in reversed(self.range(column)[1:]):
                if cell.value == cell.offset(-1).value:
                    cell.value = None

    def add_column(self, column: str, value: Any | None = None) -> Range:
        column_int = self.column + len(self.columns)
        cell = self.sheet.range(self.row, column_int)
        cell.value = column

        rng = self.range(column)

        if value is not None:
            rng.options(transpose=True).value = value

        return rng

    def add_formula_column(
        self,
        rng: Range | str,
        formula: str,
        *,
        number_format: str | None = None,
        autofit: bool = False,
    ) -> None:
        """Add a formula column.

        Args:
            rng (Range): The range of the column.
            formula (str or tuple): The formula.
            number_format (str, optional): The number format.
            autofit (bool): Whether to autofit the width.
        """
        columns = self.columns
        wide_columns = self.wide_columns

        if isinstance(rng, str):
            if rng not in columns + wide_columns:
                rng = self.add_column(rng)
            else:
                rng = self.range(rng)

        refs = {}
        for m in re.finditer(r"{(.+?)}", formula):
            column = m.group(1)

            if column in columns:
                ref = self.range(column, 0)
                addr = ref.get_address(row_absolute=False)

            elif column in wide_columns:
                ref = self.range(column, -1)[0].offset(1)
                addr = ref.get_address(column_absolute=False)

            else:
                ref = self.range(column, 0)[0]
                addr = ref.get_address(column_absolute=False, row_absolute=False)

            refs[column] = addr

        rng.value = formula.format(**refs)

        if number_format:
            rng.number_format = number_format

        if autofit:
            rng = rng.sheet.range(rng[0].offset(-1), rng[-1])
            rng.autofit()

    def add_wide_column(
        self,
        column: str,
        values: Iterable[str | float],
        *,
        number_format: str | None = None,
        autofit: bool = True,
        style: bool = False,
    ) -> Range:
        """Add a wide column.

        Args:
            column (str): The name of the wide column.
            values (iterable): The values to be expanded horizontally.
            number_format (str, optional): The number format.
            autofit (bool): Whether to autofit the width.
            style (bool): Whether to style the column.
        """
        if self.columns_level != 1:
            raise NotImplementedError

        rng = self.cell.offset(0, len(self.columns))
        values_list = list(values)
        rng.value = values_list

        header = rng.offset(-1)
        header.value = column

        set_alignment(header, horizontal_alignment="left")

        rng = rng.sheet.range(rng, rng.offset(0, len(values_list)))
        if number_format:
            rng.number_format = number_format

        if autofit:
            self.range(column, -1).autofit()

        if style:
            self.set_style()

        return rng[0].offset(1)

    @overload
    def __getitem__(self, column: str | tuple) -> Series: ...

    @overload
    def __getitem__(self, column: Sequence[str | tuple]) -> DataFrame: ...

    def __getitem__(
        self,
        column: str | tuple | Sequence[str | tuple],
    ) -> Series | DataFrame:
        """Return the column data.

        If column is a string, return a Series. If column is a list,
        return a DataFrame. The index is ignored.
        """
        if isinstance(column, list):
            return DataFrame({c: self[c] for c in column})

        if isinstance(column, str | tuple):
            row = self.row + self.columns_level
            name, column_index = column, self.index(column)
            start = self.sheet.range(row, column_index)

            if len(self) == 1:
                array = [start.value]
            else:
                end = start.offset(len(self) - 1, 0)
                rng = self.sheet.range(start, end)
                array = rng.options(np.array).value

            return Series(array, name=name)

        raise NotImplementedError

    def __setitem__(self, column: str | tuple, value: ArrayLike) -> None:
        if column in self:
            rng = self.range(column)
        elif isinstance(column, str):
            rng = self.add_column(column)
        else:
            raise NotImplementedError

        if isinstance(value, str) and value.startswith("="):
            self.add_formula_column(rng, value)
        else:
            rng.options(transpose=True).value = value

    def select(self, **kwargs) -> NDArray[np.bool_]:
        """Return the selection of the SheetFrame.

        Keyword arguments are column names and values. The conditions are as follows:
           - list : the specified elements are selected.
           - tuple : the range of the value.
           - other : the value is selected if it matches.
        """

        def filter_(
            sel: NDArray[np.bool_],
            array: Series,
            value: str | list | tuple,
        ) -> None:
            if isinstance(value, list):
                sel &= array.isin(value)
            elif isinstance(value, tuple):
                sel &= (array >= value[0]) & (array <= value[1])
            else:
                sel &= array == value

        if self.columns_names is None:
            # vertical selection
            sel = np.ones(len(self), dtype=bool)

            for key, value in kwargs.items():
                filter_(sel, self[key], value)

            return sel

        # horizontal selection
        columns = self.value_columns
        sel = np.ones(len(columns), dtype=bool)
        df = DataFrame(columns, columns=self.columns_names)

        for key, value in kwargs.items():
            filter_(sel, df[key], value)

        return sel

    @overload
    def get_address(
        self,
        column: str | tuple,
        *,
        formula: bool = False,
        **kwargs,
    ) -> Series: ...

    @overload
    def get_address(
        self,
        column: list[str | tuple] | None = None,
        *,
        formula: bool = False,
        **kwargs,
    ) -> DataFrame: ...

    def get_address(
        self,
        column: str | tuple | list[str | tuple] | None = None,
        *,
        formula: bool = False,
        **kwargs,
    ) -> Series | DataFrame:
        """Return the address list of the column.

        Args:
            column (str or tuple or list): The name of the column.
            formula (bool, optional): Whether to add '=' to the beginning
                of the address.
            kwargs Keyword arguments for the `Range.get_address` method.

        Returns:
            Series or DataFrame: The address list of the column.
        """
        if column is None:
            return self.get_address(self.value_columns, formula=formula, **kwargs)

        if isinstance(column, list):
            values = {c: self.get_address(c, formula=formula, **kwargs) for c in column}
            df = DataFrame(values)

            if self.has_index and self.index_columns[0]:
                index = self._index_frame()
                if len(index.columns) == 1:
                    df.index = Index(index[index.columns[0]])
                else:
                    df.index = MultiIndex.from_frame(index)

            return df

        addresses = iter_addresses(self.range(column), formula=formula, cellwise=True)
        return Series(list(addresses), name=column)

    def _index_frame(self) -> DataFrame:
        start = self.cell.offset(self.columns_level - 1)
        end = start.offset(len(self), self.index_level - 1)
        rng = self.sheet.range(start, end)
        return rng.options(DataFrame).value.reset_index()  # type: ignore

    def ranges(
        self,
        sel: Sequence[bool] | NDArray[np.bool_] | None = None,
        **kwargs,
    ) -> Iterator[Range]:
        if sel is None:
            n = len(self) if self.columns_names is None else len(self.value_columns)
            sel = np.ones(n, dtype=bool)
        elif not isinstance(sel, np.ndarray):
            sel = np.array(sel, dtype=bool)

        if kwargs:
            sel &= self.select(**kwargs)

        if self.columns_names is None:
            yield from self._ranges_row(sel)
        else:
            yield from self._ranges_column(sel)

    def _ranges_row(self, sel: NDArray[np.bool_]) -> Iterator[Range]:
        offset = self.row + self.columns_level
        start = self.column + self.index_level
        end = start + len(self.value_columns) - 1

        for index in range(len(self)):
            if not sel[index]:
                continue

            yield self.sheet.range((index + offset, start), (index + offset, end))

    def _ranges_column(self, sel: NDArray[np.bool_]) -> Iterator[Range]:
        offset = self.column + self.index_level
        start = self.row + self.columns_level
        end = start + len(self) - 1

        for index in range(len(self.value_columns)):
            if not sel[index]:
                continue

            yield self.sheet.range((start, index + offset), (end, index + offset))

    def melt(
        self,
        func: Func = None,
        *,
        formula: bool = False,
        value_name: str = "value",
        **kwargs,
    ) -> DataFrame:
        """Unpivot a SheetFrame from wide to long format."""
        if self.columns_names is None:
            raise NotImplementedError

        columns = self.value_columns
        df = DataFrame(columns, columns=self.columns_names)
        values = [aggregate(func, r, formula=formula, **kwargs) for r in self.ranges()]
        df[value_name] = values
        return df

    @overload
    def agg(self, func: Func | dict, **kwargs) -> Series: ...

    @overload
    def agg(self, func: Sequence[Func], **kwargs) -> DataFrame: ...

    def agg(
        self,
        func: Func | dict | Sequence[Func],
        columns: str | tuple | Sequence[str | tuple] | None = None,
        formula: bool = False,
        **kwargs,
    ) -> str | Series | DataFrame:
        agg = partial(self._agg_column, formula=formula, **kwargs)

        if isinstance(func, dict):
            return Series({c: agg(f, c) for c, f in func.items()})

        if columns is None:
            columns = self.value_columns
        elif isinstance(columns, str | tuple):
            columns = [columns]

        if func is None or isinstance(func, str | Range):
            return Series({c: agg(func, c) for c in columns})

        values = [{c: agg(f, c) for c in columns} for f in func]
        return DataFrame(values, index=list(func))

    def _agg_column(
        self,
        func: str | Range | None,
        column: str | tuple,
        formula: bool = False,
        **kwargs,
    ) -> str:
        if func == "first":
            rng = self.first_range(column)
            func = None
        else:
            rng = self.range(column)

        return aggregate(func, rng, formula=formula, **kwargs)

    def groupby(self, by: str | list[str] | None, *, sort: bool = True) -> GroupBy:
        return GroupBy(self, by, sort=sort)

    def get_number_format(self, column: str | tuple) -> str:
        return self.range(column, 0).number_format

    def set_number_format(
        self,
        number_format: str | dict | None = None,
        *,
        autofit: bool = False,
        **columns_format,
    ) -> None:
        if isinstance(number_format, str):
            start = self.cell.offset(self.columns_level, self.index_level)
            rng = self.sheet.range(start, self.range()[-1])
            rng.number_format = number_format
            if autofit:
                rng.autofit()
            return

        if isinstance(number_format, dict):
            columns_format.update(number_format)

        for column in chain(self.columns, self.wide_columns):
            if not column:
                continue

            for pattern, number_format in columns_format.items():
                column_name = column if isinstance(column, str) else column[0]

                if re.match(pattern, column_name):
                    rng = self.range(column)
                    rng.number_format = number_format
                    if autofit:
                        rng.autofit()
                    break

    def set_style(self, *, gray: bool = False, **kwargs) -> None:
        set_frame_style(self, gray=gray, **kwargs)
        set_wide_column_style(self, gray=gray)

    def set_alignment(self, alignment: str) -> None:
        start = self.cell
        end = start.offset(0, len(self.columns) - 1)
        rng = self.sheet.range(start, end)
        set_alignment(rng, alignment)

    def set_adjacent_column_width(self, width: float) -> None:
        """Set the width of the adjacent empty column."""
        column = self.column + len(self.columns)
        self.sheet.range(1, column).column_width = width

    def add_child_frame(self, child: SheetFrame) -> None:
        """Add a child SheetFrame."""
        self.children.append(child)
        child.parent = self

    def get_child_cell(self) -> Range:
        """Get the cell of the child SheetFrame."""
        offset = len(self.columns) + 1
        offset += sum(len(child.columns) + 1 for child in self.children)
        return self.cell.offset(0, offset)

    def get_adjacent_cell(self, offset: int = 0) -> Range:
        """Get the adjacent cell of the SheetFrame."""
        if self.children:
            return self.get_child_cell()

        return self.cell.offset(0, len(self.columns) + offset + 1)

    def move(self, count: int, direction: str = "down", width: int = 0) -> Range:
        return modify.move(self, count, direction, width)

    def delete(self, direction: str = "up", *, entire: bool = False) -> None:
        return modify.delete(self, direction, entire=entire)

    def dist_frame(self, *args, **kwargs) -> DistFrame:
        from .dist_frame import DistFrame

        self.set_adjacent_column_width(1)

        self.dist = DistFrame(self, *args, **kwargs)
        return self.dist

    def stats_frame(self, *args, **kwargs) -> StatsFrame:
        from .stats_frame import StatsFrame

        self.stats = StatsFrame(self, *args, **kwargs)
        return self.stats

    def set_chart_position(self, pos: str = "right") -> None:
        set_first_position(self, pos=pos)

    def scatter(self, *args, **kwargs) -> Scatter:
        return Scatter(*args, data=self, **kwargs)

    def plot(self, *args, **kwargs) -> Plot:
        return Plot(*args, data=self, **kwargs)

    def bar(self, *args, **kwargs) -> Bar:
        return Bar(*args, data=self, **kwargs)

    def grid(self, *args, **kwargs) -> FacetGrid:
        return FacetGrid(self, *args, **kwargs)
