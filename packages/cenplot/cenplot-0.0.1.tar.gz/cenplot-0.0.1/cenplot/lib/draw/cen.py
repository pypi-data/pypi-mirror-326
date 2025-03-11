import os
import sys
import numpy as np

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .settings import SinglePlotSettings
from .hor import draw_hor, draw_hor_ort
from .label import draw_label
from .self_ident import draw_self_ident
from .bar import draw_bars
from .legend import draw_legend
from .utils import create_subplots, format_ax, set_both_labels
from ..io.utils import get_min_max_track
from ..track.types import Track, TrackOption, TrackPosition, LegendPosition


def plot_one_cen(
    dfs_track: list[Track],
    outdir: str,
    chrom: str,
    settings: SinglePlotSettings,
) -> tuple[Figure, np.ndarray, str]:
    # Show chrom trimmed of spaces for logs and filenames.
    print(f"Plotting {chrom}...", file=sys.stderr)

    if not settings.xlim:
        # Get min and max position of all tracks for this cen.
        _, min_st_pos = get_min_max_track(dfs_track, typ="min")
        _, max_end_pos = get_min_max_track(
            dfs_track, typ="max", default_col="chrom_end"
        )
    else:
        min_st_pos = settings.xlim[0]
        max_end_pos = settings.xlim[1]

    width, height = settings.dim

    # # Scale height based on track length.
    # adj_height = height * (trk_max_end / max_end_pos)
    # height = height if adj_height == 0 else adj_height

    fig, axes, track_indices = create_subplots(
        dfs_track,
        width,
        height,
        settings.legend_pos,
        settings.legend_prop,
        layout=settings.layout,
    )
    if settings.legend_pos == LegendPosition.Left:
        track_col, legend_col = 1, 0
    else:
        track_col, legend_col = 0, 1

    track_labels: list[str] = []

    def get_track_label(chrom: str, track: Track, all_track_labels: list[str]) -> str:
        if not track.title:
            return ""
        try:
            fmt_track_label = track.title.format(chrom=chrom)
        except KeyError:
            fmt_track_label = track.title

        track_label = fmt_track_label.encode("ascii", "ignore").decode("unicode_escape")

        # Update track label for each overlap.
        if track.pos == TrackPosition.Overlap:
            try:
                track_label = f"{all_track_labels[-1]}\n{track_label}"
            except IndexError:
                pass

        return track_label

    num_hor_split = 0
    for idx, track in enumerate(dfs_track):
        track_row = track_indices[idx]
        track_label = get_track_label(chrom, track, track_labels)

        try:
            track_ax: Axes = axes[track_row, track_col]
        except IndexError:
            print(f"Cannot get track ({track_row, track_col}) for {track}.")
            continue
        try:
            legend_ax: Axes = axes[track_row, legend_col]
        except IndexError:
            legend_ax = None

        # Set xaxis limits
        track_ax.set_xlim(min_st_pos, max_end_pos)

        if track.opt == TrackOption.Legend:
            draw_legend(track_ax, axes, track, dfs_track, track_row, track_col)
        elif track.opt == TrackOption.Position:
            # Hide everything but x-axis
            format_ax(
                track_ax,
                grid=True,
                yticks=True,
                spines=("right", "left", "top"),
            )
        elif track.opt == TrackOption.Spacer:
            # Hide everything.
            format_ax(
                track_ax,
                grid=True,
                xticks=True,
                yticks=True,
                spines=("right", "left", "top", "bottom"),
            )
        else:
            # Switch track option. {bar, label, ident, hor}
            # Add legend.
            if track.opt == TrackOption.HOR or track.opt == TrackOption.HORSplit:
                draw_fn = draw_hor
            elif track.opt == TrackOption.HOROrt:
                draw_fn = draw_hor_ort
            elif track.opt == TrackOption.Label:
                draw_fn = draw_label
            elif track.opt == TrackOption.SelfIdent:
                draw_fn = draw_self_ident
            elif track.opt == TrackOption.Bar:
                draw_fn = draw_bars

            else:
                raise ValueError("Invalid TrackOption. Unreachable.")

            draw_fn(
                ax=track_ax,
                legend_ax=legend_ax,
                track=track,
                zorder=idx,
            )

        # Store label if more overlaps.
        track_labels.append(track_label)

        # Set labels for both x and y axis.
        set_both_labels(track_label, track_ax, track)

        if not legend_ax:
            continue

        # Make legend title invisible for HORs split after 1.
        if track.opt == TrackOption.HORSplit:
            legend_ax_legend = legend_ax.get_legend()
            if legend_ax_legend and num_hor_split != 0:
                legend_title = legend_ax_legend.get_title()
                legend_title.set_alpha(0.0)
            num_hor_split += 1

        # Minimalize all legend cols except self-ident
        if track.opt != TrackOption.SelfIdent or (
            track.opt == TrackOption.SelfIdent and not track.options.legend
        ):
            format_ax(
                legend_ax,
                grid=True,
                xticks=True,
                xticklabel_fontsize=track.options.legend_fontsize,
                yticks=True,
                yticklabel_fontsize=track.options.legend_fontsize,
                spines=("right", "left", "top", "bottom"),
            )
        else:
            format_ax(
                legend_ax,
                grid=True,
                xticklabel_fontsize=track.options.legend_fontsize,
                yticklabel_fontsize=track.options.legend_fontsize,
                spines=("right", "top"),
            )

    # Add title
    if settings.title:
        title = settings.title.format(chrom=chrom)
        fig.suptitle(
            title, x=0.02, y=0.98, horizontalalignment="left", fontsize="xx-large"
        )

    outfile = os.path.join(outdir, f"{chrom}.{settings.format}")

    # Pad between axes.
    fig.get_layout_engine().set(h_pad=settings.axis_h_pad)
    fig.savefig(outfile, dpi=settings.dpi, transparent=settings.transparent)

    return fig, axes, outfile
