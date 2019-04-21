# -*- coding: utf-8 -*-

"""Console script for pyuwsgimemhog."""
import sys
import click

from .pyuwsgimemhog import uwsgimemhog


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
    with open(logfile, "r") as f:
        hogs = uwsgimemhog(f, threshold * 1_000_000, normalize_nums)
        for path, memory in hogs:
            click.echo('{} {}'.format(path, memory // 1_000_000))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
