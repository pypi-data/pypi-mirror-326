import os
import sys
import argparse
import multiprocessing

import polars as pl

from typing import Any, Iterable, TYPE_CHECKING, TextIO
from concurrent.futures import ProcessPoolExecutor

from cenplot import (
    plot_one_cen,
    merge_plots,
    read_one_cen_tracks,
    Track,
    SinglePlotSettings,
)

if TYPE_CHECKING:
    SubArgumentParser = argparse._SubParsersAction[argparse.ArgumentParser]
else:
    SubArgumentParser = Any


def get_draw_args(
    input_tracks: str, chroms: TextIO, share_xlim: bool, outdir: str
) -> list[tuple[list[Track], str, str, SinglePlotSettings]]:
    all_chroms: Iterable[str] = [line.strip() for line in chroms.readlines()]

    inputs = []
    tracks_settings = [
        (chrom, *read_one_cen_tracks(input_tracks, chrom=chrom)) for chrom in all_chroms
    ]
    xmin_all, xmax_all = sys.maxsize, 0
    if share_xlim:
        for *_, settings in tracks_settings:
            if settings.xlim:
                xmin, xmax = settings.xlim
                xmin_all = min(xmin_all, xmin)
                xmax_all = max(xmax_all, xmax)

    for chrom, tracks_summary, plot_settings in tracks_settings:
        if share_xlim:
            plot_settings.xlim = (xmin_all, xmax_all)

        inputs.append(
            (
                [
                    Track(
                        trk.title,
                        trk.pos,
                        trk.opt,
                        trk.prop,
                        trk.data.filter(pl.col("chrom") == chrom)
                        if isinstance(trk.data, pl.DataFrame)
                        else None,
                        trk.options,
                    )
                    for trk in tracks_summary.tracks
                ],
                outdir,
                chrom,
                plot_settings,
            )
        )
    return inputs


def add_draw_cli(parser: SubArgumentParser) -> None:
    ap = parser.add_parser(
        "draw",
        description="Draw centromere tracks.",
    )
    ap.add_argument(
        "-t",
        "--input_tracks",
        required=True,
        type=str,
        help=(
            "TOML file with headerless BED files to plot. "
            "Specify under tracks the following fields: {name, position, type, proportion, path, or options}."
        ),
    )
    ap.add_argument(
        "-c",
        "--chroms",
        type=argparse.FileType("rt"),
        help="Names to plot in this order. Corresponds to 1st col in BED files.",
        default=None,
    )
    ap.add_argument(
        "-d",
        "--outdir",
        help="Output dir to plot multiple separate figures.",
        type=str,
        default=".",
    )
    ap.add_argument(
        "-o",
        "--outfile",
        help="Output file merging all figures. Either pdf of png.",
        type=str,
        default=None,
    )
    ap.add_argument("--share_xlim", help="Share x-axis limits.", action="store_true")
    ap.add_argument("-p", "--processes", type=int, default=4, help="Processes to run.")

    return None


def draw(
    input_tracks: str,
    chroms: TextIO,
    outdir: str,
    outfile: str,
    share_xlim: bool,
    processes: int,
):
    draw_args = get_draw_args(
        input_tracks=input_tracks, chroms=chroms, share_xlim=share_xlim, outdir=outdir
    )

    os.makedirs(outdir, exist_ok=True)
    if processes == 1:
        plots = [plot_one_cen(*draw_arg) for draw_arg in draw_args]
    else:
        with ProcessPoolExecutor(
            max_workers=processes, mp_context=multiprocessing.get_context("spawn")
        ) as pool:
            plots = pool.map(plot_one_cen, *zip(*draw_args))  # type: ignore[assignment]

    if outfile:
        merge_plots(plots, outfile)
