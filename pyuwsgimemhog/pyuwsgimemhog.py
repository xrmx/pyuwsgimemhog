# -*- coding: utf-8 -*-
"""Main module."""
import re
from collections import defaultdict
from operator import itemgetter
from urllib.parse import urlparse


UWSGI_LOG_RE = re.compile(
    r'({rss usage: (?P<rss>\d+) bytes/\d+MB} )?\[pid: (?P<pid>\d+)\|app: .*\|req: .*\] '
    r'(?P<client_ip>\d+.\d+.\d+.\d+) .* \[(?P<date>\w+ \w+\s+\d+ \d+:\d+:\d+ \d+)\] '
    r'(?P<verb>GET|POST|HEAD|PATCH|PUT|DELETE) (?P<path>/.*) => '
    r'generated \d+ bytes in (?P<time>\d+) msecs \(HTTP/\d.\d (?P<status_code>\d+)\)'
)


def uwsgimemhog(logfile, threshold, normalize_nums):
    """Parse a uWSGI logfile and yields the RSS memory usage accumulated by each path"""
    pids_rss = defaultdict(list)
    for line in logfile:
        match = UWSGI_LOG_RE.search(line)
        if not match:
            continue

        # path normalization
        url = urlparse(match.group('path'))
        path = url.path.rstrip('/') if url.path != '/' else url.path
        if normalize_nums:
            path = re.sub(r'\d+', '0', path)

        # store a list of path and rss for each pid
        pid = match.group('pid')
        rss = int(match.group('rss'))
        pids_rss[pid].append((path, rss))

    # accumulate the rss differences per path
    diffs = defaultdict(int)
    for pid, v in pids_rss.items():
        for i in range(1, len(v)):
            _, prev_rss = v[i-1]
            path, rss = v[i]
            # don't track negatives value as we care about leaks
            rss_diff = rss - prev_rss
            if rss_diff < 0:
                continue
            diffs[path] += rss_diff

    # yield all paths that accumulated more than the threshold
    for path, value in sorted(diffs.items(), key=itemgetter(1), reverse=True):
        if value > threshold:
            yield path, value
