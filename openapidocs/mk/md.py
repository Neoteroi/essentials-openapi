"""
This module provides common functions to handle Markdown.
These functions apply to any kind of Markdown work.
"""
from typing import Dict, Iterable


def write_row(
    row: Iterable[str],
    columns_widths: Dict[int, int],
    padding: int = 1,
    indent: int = 0,
) -> str:
    """
    Writes a single row for a Markdown table.
    """
    indent_chars = " " * indent
    pad_chars = " " * padding
    return (
        indent_chars
        + "|"
        + "|".join(
            pad_chars + str(cell_value).ljust(columns_widths[i]) + pad_chars
            for i, cell_value in enumerate(row)
        )
        + "|"
    )


def write_table_lines(
    matrix: Iterable[Iterable[str]],
    write_headers: bool = True,
    padding: int = 1,
    indent: int = 0,
) -> Iterable[str]:
    """
    Writes the lines of a Markdown table from a matrix (iterable of string records).
    """
    # TODO: assert that all rows have the same number of cells
    columns_widths = {
        i: max(len(str(value)) for value in column)
        for i, column in enumerate(zip(*matrix))
    }

    for row in matrix:
        yield write_row(row, columns_widths, padding, indent)

        if write_headers:
            # add separator line after headers
            yield write_row(
                ["-" * column_len for column_len in columns_widths.values()],
                columns_widths,
                padding,
                indent,
            )

            write_headers = False


def write_table(
    matrix: Iterable[Iterable[str]],
    write_headers: bool = True,
    padding: int = 1,
) -> str:
    """
    Writes a Markdown table from a matrix (iterable of string records).
    """
    return "\n".join((write_table_lines(matrix, write_headers, padding)))


def normalize_link(value: str) -> str:
    if not value:
        raise ValueError("Missing value")
    return value.replace(".", "")
