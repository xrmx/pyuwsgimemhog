# -*- coding: utf-8 -*-

"""Console script for pyuwsgimemhog."""
import sys
import click

from .pyuwsgimemhog import normalize_path, normalize_path_with_nums, uwsgimemhog


@click.command()
@click.option('--logfile', help='uWSGI log path', required=True)
@click.option('-m', '--memory-threshold', 'threshold',
              type=int, default=10, show_default=True,
              help='Memory threshold in MegaBytes')
@click.option('--normalize-nums/--no-normalize-nums', 'normalize_nums',
              default=True, show_default=True,
              help='Normalize numbers in urls')
def main(logfile, threshold, normalize_nums):
    """Console script for pyuwsgimemhog."""
    normalize = normalize_path_with_nums if normalize_nums else normalize_path
    with open(logfile, "r") as f:
        hogs = uwsgimemhog(f, threshold * 1_000_000, normalize)
        for path, memory, count in hogs:
            click.echo('{} {} {} {:.1f}'.format(
                path, memory // 1_000_000, count, memory / count / 1_000_000
            ))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
