#
# Copyright 2013 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""

Risk Report
===========

    +-----------------+----------------------------------------------------+
    | key             | value                                              |
    +=================+====================================================+
    | trading_days    | The number of trading days between self.start_date |
    |                 | and self.end_date                                  |
    +-----------------+----------------------------------------------------+
    | benchmark_volat\| The volatility of the benchmark between            |
    | ility           | self.start_date and self.end_date.                 |
    +-----------------+----------------------------------------------------+
    | algo_volatility | The volatility of the algo between self.start_date |
    |                 | and self.end_date.                                 |
    +-----------------+----------------------------------------------------+
    | treasury_period\| The return of treasuries over the period. Treasury |
    | _return         | maturity is chosen to match the duration of the    |
    |                 | test period.                                       |
    +-----------------+----------------------------------------------------+
    | sharpe          | The sharpe ratio based on the _algorithm_ (rather  |
    |                 | than the static portfolio) returns.                |
    +-----------------+----------------------------------------------------+
    | information     | The information ratio based on the _algorithm_     |
    |                 | (rather than the static portfolio) returns.        |
    +-----------------+----------------------------------------------------+
    | beta            | The _algorithm_ beta to the benchmark.             |
    +-----------------+----------------------------------------------------+
    | alpha           | The _algorithm_ alpha to the benchmark.            |
    +-----------------+----------------------------------------------------+
    | excess_return   | The excess return of the algorithm over the        |
    |                 | treasuries.                                        |
    +-----------------+----------------------------------------------------+
    | max_drawdown    | The largest relative peak to relative trough move  |
    |                 | for the portfolio returns between self.start_date  |
    |                 | and self.end_date.                                 |
    +-----------------+----------------------------------------------------+


"""

import numpy as np

import math


def tolerant_equals(a, b, atol=10e-7, rtol=10e-7):
    return math.fabs(a - b) <= (atol + rtol * math.fabs(b))



TREASURY_DURATIONS = [
    '1month', '3month', '6month',
    '1year', '2year', '3year', '5year',
    '7year', '10year', '30year'
]


# check if a field in rval is nan, and replace it with
# None.
def check_entry(key, value):
    if key != 'period_label':
        return np.isnan(value) or np.isinf(value)
    else:
        return False


############################
# Risk Metric Calculations #
############################


def sharpe_ratio(algorithm_volatility, algorithm_return, treasury_return):
    """
    http://en.wikipedia.org/wiki/Sharpe_ratio

    Args:
        algorithm_volatility (float): Algorithm volatility.
        algorithm_return (float): Algorithm return percentage.
        treasury_return (float): Treasury return percentage.

    Returns:
        float. The Sharpe ratio.
    """
    if tolerant_equals(algorithm_volatility, 0):
        return 0.0

    return (algorithm_return - treasury_return) / algorithm_volatility


def sortino_ratio(algorithm_returns, algorithm_period_return, mar):
    """
    http://en.wikipedia.org/wiki/Sortino_ratio

    Args:
        algorithm_returns (np.array-like):
            Returns from algorithm lifetime.
        algorithm_period_return (float):
            Algorithm return percentage from latest period.
        mar (float): Minimum acceptable return.

    Returns:
        float. The Sortino ratio.
    """
    if len(algorithm_returns) == 0:
        return 0.0

    rets = algorithm_returns
    downside = (rets[rets < mar] - mar) ** 2
    dr = np.sqrt(downside.sum() / len(rets))

    if tolerant_equals(dr, 0):
        return 0.0

    return (algorithm_period_return - mar) / dr


def information_ratio(algorithm_returns, benchmark_returns):
    """
    http://en.wikipedia.org/wiki/Information_ratio

    Args:
        algorithm_returns (np.array-like):
            All returns during algorithm lifetime.
        benchmark_returns (np.array-like):
            All benchmark returns during algo lifetime.

    Returns:
        float. Information ratio.
    """
    relative_returns = algorithm_returns - benchmark_returns

    relative_deviation = relative_returns.std(ddof=1)

    if (
        tolerant_equals(relative_deviation, 0)
        or
        np.isnan(relative_deviation)
    ):
        return 0.0

    return np.mean(relative_returns) / relative_deviation


def alpha(algorithm_period_return, treasury_period_return,
          benchmark_period_returns, beta):
    """
    http://en.wikipedia.org/wiki/Alpha_(investment)

    Args:
        algorithm_period_return (float):
            Return percentage from algorithm period.
        treasury_period_return (float):
            Return percentage for treasury period.
        benchmark_period_return (float):
            Return percentage for benchmark period.
        beta (float):
            beta value for the same period as all other values

    Returns:
        float. The alpha of the algorithm.
    """
    return algorithm_period_return - \
        (treasury_period_return + beta *
         (benchmark_period_returns - treasury_period_return))

###########################
# End Risk Metric Section #
###########################


def get_treasury_rate(treasury_curves, treasury_duration, day):
    rate = None

    curve = treasury_curves.ix[day]
    # 1month note data begins in 8/2001,
    # so we can use 3month instead.
    idx = TREASURY_DURATIONS.index(treasury_duration)
    for duration in TREASURY_DURATIONS[idx:]:
        rate = curve[duration]
        if rate is not None:
            break

    return rate




def select_treasury_duration(start_date, end_date):
    td = end_date - start_date
    if td.days <= 31:
        treasury_duration = '1month'
    elif td.days <= 93:
        treasury_duration = '3month'
    elif td.days <= 186:
        treasury_duration = '6month'
    elif td.days <= 366:
        treasury_duration = '1year'
    elif td.days <= 365 * 2 + 1:
        treasury_duration = '2year'
    elif td.days <= 365 * 3 + 1:
        treasury_duration = '3year'
    elif td.days <= 365 * 5 + 2:
        treasury_duration = '5year'
    elif td.days <= 365 * 7 + 2:
        treasury_duration = '7year'
    elif td.days <= 365 * 10 + 2:
        treasury_duration = '10year'
    else:
        treasury_duration = '30year'

    return treasury_duration

