import os
import re

import click
from loguru import logger

from src.core.downloader import download_files, get_filelist_from_index
from src.updater.parsers import parse_bin, parse_dat


@click.group(name="utils")
def utils_cli():
    pass


@utils_cli.command()
@click.argument("expression", type=click.STRING)
@click.argument(
    "savepath",
    type=click.Path(
        exists=True,
        writable=True,
        resolve_path=True,
    ),
)
def download_regex(expression: str, savepath: str):
    # e.g. "^Data/Actor/Monster/lm00201/.*\.kf$"
    pattern = re.compile(expression)
    filelist = get_filelist_from_index().find_by_regex(pattern)
    download_files(filelist, savepath)


@utils_cli.command()
@click.argument("filepaths", type=click.Path(exists=True), nargs=-1)
@click.argument("savepath", type=click.Path(writable=True))
def to_excel(filepaths: tuple[str], savepath: str):
    """Converts the given files as one excel file with each file representing one sheet.

    >>> python main.py utils as-excel ./tmp/updater/c_ArtifactRes.bin ./tmp/updater/s_ArtifactItem.bin ./out.xlsx

    Args:
        filepaths (tuple[str]): Filepaths to convert into excel.
        savepath (str): Save path for the excel
    """
    try:
        import xlsxwriter as xlsx  # type: ignore
    except ImportError:
        logger.critical("xlsxwriter is not installed")
        return click.Abort()

    wb = xlsx.Workbook(savepath)
    bold_fmt = wb.add_format({"bold": True})
    for fpath in filepaths:
        filename = os.path.basename(fpath)

        rows: list[dict] = []
        if filename.endswith(".dat"):
            rows += parse_dat(fpath)
        elif filename.endswith(".bin"):
            rows += parse_bin(fpath)
        else:
            logger.critical(f"Unknown file extension: {filename}")
            continue

        if not rows:
            logger.warning(f"No data found for {filename}, skipping")
            continue

        sheet = wb.add_worksheet(name=filename[:30])
        headers = rows[0].keys()

        sheet.write_row(0, 0, headers, bold_fmt)
        for row_index, row in enumerate(rows, start=1):
            sheet.write_row(row_index, 0, list(row.values()))

    wb.close()
