# (C) Datadog, Inc. 2018-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datetime import datetime

from datadog_checks.base import to_string
from datadog_checks.base.utils.common import round_value
from datadog_checks.base.utils.time import get_timestamp


def sanitize_strings(s):
    """
    Sanitize strings from pymqi responses
    """
    s = to_string(s)
    found = s.find('\x00')
    if found >= 0:
        s = s[:found]
    return s.strip()


def calculate_elapsed_time(datestamp, timestamp, current_time=None):
    if current_time is None:
        current_time = get_timestamp()
    else:
        current_time = current_time

    if datestamp and timestamp:
        timestamp_str = sanitize_strings(datestamp) + ' ' + sanitize_strings(timestamp)
        timestamp_epoch = datetime.strptime(timestamp_str, '%Y-%m-%d %H.%M.%S').timestamp()
    else:
        return

    elapsed = round_value(current_time - timestamp_epoch)

    return elapsed
