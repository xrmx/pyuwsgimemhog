#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pyuwsgimemhog` package."""

import pytest

from click.testing import CliRunner

from pyuwsgimemhog import pyuwsgimemhog
from pyuwsgimemhog import cli

@pytest.fixture
def invalid_sample_log():
    return ['invalid']


@pytest.fixture
def normalization_log():
    return """{address space usage: 806559744 bytes/769MB} {rss usage: 342519808 bytes/326MB} [pid: 4193|app: 0|req: 990967/3250990] 127.0.0.2 () {48 vars in 984 bytes} [Thu Apr 11 20:57:06 2019] POST /api/12 => generated 192 bytes in 71 msecs (HTTP/1.1 201) 5 headers in 153 bytes (1 switches on core 0)
{address space usage: 806559744 bytes/769MB} {rss usage: 352321536 bytes/336MB} [pid: 4193|app: 0|req: 990967/3250990] 127.0.0.2 () {48 vars in 984 bytes} [Thu Apr 11 20:57:06 2019] POST /api/12/ => generated 192 bytes in 71 msecs (HTTP/1.1 201) 5 headers in 153 bytes (1 switches on core 0)
{address space usage: 806559744 bytes/769MB} {rss usage: 354418688 bytes/336MB} [pid: 4193|app: 0|req: 990967/3250990] 127.0.0.2 () {48 vars in 984 bytes} [Thu Apr 11 20:57:06 2019] POST /api/11/ => generated 192 bytes in 71 msecs (HTTP/1.1 201) 5 headers in 153 bytes (1 switches on core 0)""".split('\n')


@pytest.fixture
def memory_reduction_log():
    return """{address space usage: 806559744 bytes/769MB} {rss usage: 342519808 bytes/326MB} [pid: 4193|app: 0|req: 990962/3250981] 127.0.0.1 () {36 vars in 573 bytes} [Thu Apr 11 20:57:06 2019] GET / => generated 23111 bytes in 2 msecs (HTTP/1.1 200) 5 headers in 165 bytes (1 switches on core 0)
{address space usage: 806559744 bytes/769MB} {rss usage: 283852800 bytes/270MB} [pid: 4193|app: 0|req: 990963/3250982] 127.0.0.1 () {36 vars in 573 bytes} [Thu Apr 11 20:57:06 2019] GET / => generated 23111 bytes in 1 msecs (HTTP/1.1 200) 5 headers in 165 bytes (1 switches on core 0)""".split('\n')


@pytest.fixture
def sample_log():
    return """{address space usage: 806559744 bytes/769MB} {rss usage: 342519808 bytes/326MB} [pid: 4193|app: 0|req: 990962/3250981] 127.0.0.1 () {36 vars in 573 bytes} [Thu Apr 11 20:57:06 2019] GET / => generated 23111 bytes in 2 msecs (HTTP/1.1 200) 5 headers in 165 bytes (1 switches on core 0)
{address space usage: 806559744 bytes/769MB} {rss usage: 346030080 bytes/330MB} [pid: 4193|app: 0|req: 990963/3250982] 127.0.0.1 () {36 vars in 573 bytes} [Thu Apr 11 20:57:06 2019] GET / => generated 23111 bytes in 1 msecs (HTTP/1.1 200) 5 headers in 165 bytes (1 switches on core 0)
{address space usage: 745689088 bytes/711MB} {rss usage: 282902528 bytes/269MB} [pid: 30820|app: 0|req: 592444/3250988] 127.0.0.1 () {36 vars in 573 bytes} [Thu Apr 11 20:57:06 2019] GET / => generated 23111 bytes in 2 msecs (HTTP/1.1 200) 5 headers in 165 bytes (1 switches on core 0)
{address space usage: 745689088 bytes/711MB} {rss usage: 283115520 bytes/270MB} [pid: 30820|app: 0|req: 592444/3250988] 127.0.0.1 () {36 vars in 573 bytes} [Thu Apr 11 20:57:06 2019] GET / => generated 23111 bytes in 2 msecs (HTTP/1.1 200) 5 headers in 165 bytes (1 switches on core 0)""".split('\n')


def test_uwsgimemhog_skips_invalid_lines(invalid_sample_log):
    data = pyuwsgimemhog.uwsgimemhog(invalid_sample_log, threshold=1, normalize_nums=True)
    with pytest.raises(StopIteration):
        next(data)


def test_uwsgimemhog_normalize_paths_correctly(normalization_log):
    data = pyuwsgimemhog.uwsgimemhog(normalization_log, threshold=1, normalize_nums=False)
    assert next(data) == ('/api/12', 9801728)
    assert next(data) == ('/api/11', 2097152)
    with pytest.raises(StopIteration):
        next(data)


def test_uwsgimemhog_normalize_nums_correctly(normalization_log):
    data = pyuwsgimemhog.uwsgimemhog(normalization_log, threshold=1, normalize_nums=True)
    assert next(data) == ('/api/0', 11898880)
    with pytest.raises(StopIteration):
        next(data)


def test_uwsgimemhog_ignores_negative_rss_diffs(memory_reduction_log):
    data = pyuwsgimemhog.uwsgimemhog(memory_reduction_log, threshold=1, normalize_nums=True)
    with pytest.raises(StopIteration):
        next(data)


def test_uwsgimemhog_sum_same_path_on_different_pids_correctly(sample_log):
    data = pyuwsgimemhog.uwsgimemhog(sample_log, threshold=1, normalize_nums=True)
    assert next(data) == ('/', 3723264)
    with pytest.raises(StopIteration):
        next(data)


def test_uwsgimemhog_threshold_works_correctly(sample_log):
    data = pyuwsgimemhog.uwsgimemhog(sample_log, threshold=10_000_000, normalize_nums=True)
    with pytest.raises(StopIteration):
        next(data)


def test_command_line_interface_renders_help():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output
