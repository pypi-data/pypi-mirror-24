'''
A collection of statistical routines.
'''
import six
import time
import colorsys
import scipy.stats
import collections
import numpy as np
from . import color
import pandas as pd
from datetime import datetime
from dateutil.parser import parse

_NP_EMPTY_INT_ARRAY = np.array([], dtype=int)
_ID = {}

#: An alias for ``pandas.series``
uniq = pd.unique

#: An alias for ``scipy.stats.nanmean``
nanmean = np.nanmean


def sorted(series, reversed=False, **args):
    '''
    Same as series.sort(...), except that it
        - does not sort the original array
        - returns a sorted copy
        - with a ``reversed`` provision

    Parameters
    ----------
    series : Pandas Series or numpy array
        Data to sort
    reversed : boolean, optional
        Data is sorted in ascending order unless ``reversed=True``

    Notes
    -----
    All other arguments accepted by `argsort
    <http://docs.scipy.org/doc/numpy/reference/generated/numpy.argsort.html>`_
    are valid.
    '''
    indices = series.argsort(**args)
    return series[indices[::-1]] if reversed else series[indices]


def _slow_uniq(series):
    '''
    Returns a unique list of elements from a sequence, preserving order.
    [source](http://stackoverflow.com/a/480227/100904)

    If you are using a NumPy array and are OK with sorted return values, use
    `np.unique` instead. It's faster.

    Parameters
    ----------
    series : list or any iterable
        Data to find the unique values of

    Examples
    --------
    Typical usage::

        stats._slow_uniq(['c', 'c', 'b', 'b', 'b', 'a', 'a'])
        # ['c', 'b', 'a']
    '''
    seen = set()
    seen_add = seen.add
    return [val for val in series if val not in seen and not seen_add(val)]


def freq(series):
    '''
    Returns a dictionary containing the number of occurrences of
    each iteq in a sequence. Order is not preserved.
    `source <http://stackoverflow.com/a/4037497/100904>`_

    Parameters
    ----------
    series : list or any iterable
        Data to find the frequency of.

    Returns
    -------
    frequency : a dictionary
        Keys are the items in ``series``.
        Values the the number of occurrences.

    Examples
    --------
    Typical usage::

        stats.freq(['c', 'c', 'b', 'b', 'b', 'a', 'a'])
        # {'a': 2, 'b': 3, 'c': 2}
    '''
    freq = collections.defaultdict(int)
    for item in series:
        freq[item] += 1
    return dict(freq)


def rolling_window(series, window):
    '''
    Returns a rolling window. For example:

    This is useful in computing moving averages.
    For example, this gives you the 7-day moving average:

        np.mean(rolling_window(data, 7))

    Examples
    --------
    Typical usage::

        stats.rolling_window([1, 2, 3, 4], window=3)
        # array([[ nan,  nan,   1.],
        #        [ nan,   1.,   2.],
        #        [  1.,   2.,   3.],
        #        [  2.,   3.,   4.]])

    Notes
    -----
    -  `Rolling statistics
       <http://www.rigtorp.se/2011/01/01/rolling-statistics-numpy.html>`_
    -  `Using strides for an efficient moving average filter
       <http://stackoverflow.com/q/4936620>`_
    '''
    fill = np.empty(window - 1)
    fill.fill(np.nan)
    series = np.concatenate([fill, series, fill])
    shape = series.shape[:-1] + (series.shape[-1] - 2 * window + 2, window)
    strides = series.strides + (series.strides[-1],)
    return np.lib.stride_tricks.as_strided(series, shape, strides)


def movingaverage(series, period):
    '''
    Returns a new ``series`` with the moving average over the same ``period``.

    The length of the new ``series`` is the same as the original.
    If there are any nan values in the past, they're ignored.

    Parameters
    ----------
    series : Pandas Series, numpy array, list or iterable
        Data to compute moving average for
    period : int
        Number of items in ``series`` to use at a time

    Examples
    --------
    Typical usage::

        stats.movingaverage([2, 3, np.nan, np.nan, 6], 2)
        # array([ 2. ,  2.5,  3. ,  nan,  6. ])
    '''
    return nanmean(rolling_window(series, period), -1)


def quantiles(series, quantiles=None, interpolation='lower'):
    '''
    Returns the specified quantiles of a ``series``, ignoring nan.
    In pandas, use ``Series.quantile`` instead.

    Parameters
    ----------
    series : Pandas Series, numpy array
    quantiles : list of float
        List of quantiles to return. By default, returns
        [min, 25%, median, 75%, max]
    interpolation : {'linear', 'lower', 'higher', 'midpoint', 'nearest'}
        Defaults is 'lower'

    Examples
    --------
    Typical usage::

        stats.quantiles(np.arange(1, 999), [0., .33, .67, 1.])
        # array([1, 330, 668, 998])
    '''
    if quantiles is None:
        quantiles = [0, 25, 50, 75, 100]
    else:
        quantiles = [x * 100 for x in quantiles]

    # Ignore nans
    series = series[-np.isnan(series)]
    if len(series) == 0:
        return np.zeros(len(quantiles))

    return np.percentile(series, quantiles, interpolation=interpolation)


def scale(series, lo=None, hi=None):
    '''
    Returns the values linearly scaled from 0 - 1.

    The lowest value becomes 0, the highest value becomes 1, and all other
    values are proportionally multiplied and have a range between 0 and 1.

    Parameters
    ----------
    series : Pandas Series, numpy array, list or iterable
        Data to scale
    lo : float
        Value that becomes 0. Values lower than ``lo`` in ``series``
        will be mapped to negative numbers.
    hi : float
        Value that becomes 1. Values higher than ``hi`` in ``series``
        will be mapped to numbers greater than 1.

    Examples
    --------
    Typical usage::

        stats.scale([1, 2, 3, 4, 5])
        # array([ 0.  ,  0.25,  0.5 ,  0.75,  1.  ])

        stats.scale([1, 2, 3, 4, 5], lo=2, hi=4)
        # array([-0.5,  0. ,  0.5,  1. ,  1.5])
    '''
    series = np.array(series, dtype=float)
    lo = np.nanmin(series) if lo is None or np.isnan(lo) else lo
    hi = np.nanmax(series) if hi is None or np.isnan(hi) else hi
    return (series - lo) / ((hi - lo) or np.nan)


def rank(series):
    '''
    .. deprecated:: 0.1
        Use ``pd.Series.rank(method='min', ascending=False)``

    Returns the `standard competition ranking
    <http://en.wikipedia.org/wiki/Ranking>`_ of each element in a numeric
    array. Differs from ``scipy.stats.mstats.rank`` if the values are
    identical: the lowest (i.e. best) rank is given to all of them.

    Parameters
    ----------
    series : Pandas Series, numpy array, list or iterable
        Data to get ranks of

    Examples
    --------
    Typical usage::

        stats.rank([3, 4, 4, 5, 5, 8])
        # array([6, 4, 4, 2, 2, 1])
    '''
    i, rank = 0, {}
    sorted_series = np.array(series, dtype=float)
    sorted_series.sort()
    for value in sorted_series[~np.isnan(sorted_series)][::-1]:
        if np.isnan(value):
            continue
        if value not in rank:
            rank[value] = i + 1
        i += 1
    return np.array([rank.get(x, np.nan) for x in series])


Cor = collections.namedtuple('Cor', ['cor', 'prob'])


def corrcoef(matrix):
    '''
    Same as ``np.ma.corrcoef``, but returns ``p`` values as well

    Parameters
    ----------
    matrix : 2D numpy array of float

    Examples
    --------
    Typical usage::

        result = stats.corrcoef([
            [1, 2, 3],
            [2, 3, 4],
            [3, np.nan, 5]])
        # result.cor is the correlation matrix
        #       [ 1.,  1.,  1.],
        #       [ 1.,  1.,  1.],
        #       [ 1.,  1.,  1.]
        # result.prob is the significance probability matrix
        #       [ 0.,  0.,  0.],
        #       [ 0.,  0.,  0.],
        #       [ 0.,  0.,  0.]
    '''
    masked = np.ma.masked_array(matrix, np.isnan(matrix))
    corr = r = np.ma.corrcoef(masked)
    degrees = masked.shape[1] - 2
    t = np.abs(r) * (degrees / (1 - r * r)) ** 0.5
    prob = 2 * (1 - scipy.stats.t.cdf(t, degrees))
    prob[corr == 1.] = 0.
    return Cor(corr.filled(0.), prob)


Crosstab = collections.namedtuple(
    'Crosstab', ['rows', 'cols', 'mean', 'diff', 'prob'])


def crosstab(row, col, val):
    '''
    Checks how significantly cell averages differ from column averages.

    TODO: Handle ``nan``. Add ``rowsum=`` and ``colsum=``

    Parameters
    ----------
    row : Pandas Series, numpy array, list or iterable
        values to group by into rows
    col : Pandas Series, numpy array, list or iterable
        values to group by into columns
    val : Pandas Series, numpy array, list or iterable
        values to aggregate into crosstabs

    Returns
    -------
    rows : numpy array
        row headers -- unique values of the ``row`` values
    cols : numpy array
        column headers -- unique values of the ``col`` values
    mean[row, col] : 2D numpy array
        mean of ``val`` values for each combination of ``row``, ``col``
    diff[row, col] : 2D numpy array
        deviation of crosstab from total row
    prob[row, col] : 2D array
        significance of the deviation. Smaller is more significant
    '''
    row, col, val = np.array(row), np.array(col), np.array(val)
    rows, cols = uniq(row), uniq(col)
    shp = (len(rows), len(cols))
    mean, diff, prob = np.zeros(shp), np.zeros(shp), np.ones(shp)
    row_indices = {row_name: row == row_name for row_name in rows}
    col_indices = {col_name: col == col_name for col_name in cols}
    for col_index, col_name in enumerate(cols):
        col_value = col_indices[col_name]
        row_mean = nanmean(val[col_value])
        for row_index, row_name in enumerate(rows):
            value = val[row_indices[row_name] & col_value]
            mean[row_index, col_index] = nanmean(value)
            diff[row_index, col_index] = mean[row_index, col_index] - row_mean
            prob[row_index, col_index] = scipy.stats.ttest_1samp(
                value, row_mean)[1]
    return Crosstab(rows, cols, mean, diff, prob)


Timeseries = collections.namedtuple('Timeseries', ['dates', 'series'])


def timeseries(dates, *value, **args):
    '''
    Given a set of ``dates`` and one or more array values,
    adds ``nan`` to the values for all missing days.

    Takes an optional ``start_date=datetime.datetime(...)``
    to override the start date.

    Returns a ``Timeseries`` object that has two attributes:

    Parameters
    ----------
    - dates : Pandas Series, numpy array, list or iterable of datetime strings
        List of datetime values
    - value1, value2, ... : one or more Series/array/list/iterable

    Returns
    -------
    start: start date (min) of the ``dates``
    result: 2D numpy array
        1 row for each ``value`` array,
        1 column for each *consecutive* day.

    Examples
    --------
    Typical usage::

        result = stats.timeseries(
            ['10 Aug 2012', '12 Aug 2012', '13 Aug 2012'],
            [3, 4, 5],
            [4, 5, 6])
        # result.dates is the starting date
        #       datetime.datetime(2012, 8, 10, 0, 0)
        # result.series is the 2D array of
        #       [3., nan, 4., 5.],
        #       [4., nan, 5., 6.]
    '''
    dates = [parse(date) for date in dates]
    start = args.get('start_date', min(dates))
    max_date = max(dates)
    num_days = (max_date - start).days + 1 if max_date >= start else 0
    result = np.empty([len(value), num_days])
    result.fill(np.nan)
    if num_days > 0:
        for i, array in enumerate(value):
            for index, value in enumerate(array):
                result[i, (dates[index] - start).days] = value
    return Timeseries(start, result)


def growth(series, period, ratio=True):
    '''
    Returns the growth of a ``series`` over a ``period``.

    Parameters
    ----------
    series : Pandas Series, numpy array, list or iterable
        Data to find the growth of.
    period : int
        Number of periods over which to find growth. For example, ``period=7``
        averages the last 7 values, and compares it with *previous 7 values*
    ratio : boolean, optional
        By default, growth is calculated by taking the ratio of the period
        average with the previous period average. Set ``ratio=False`` to use
        the *difference* instead of the ratio.

    Examples
    --------
    Typical usage::

        stats.round(growth([1, 2, 3, 4], 2), 5)
        # 1.33333   == mean(4,3)/mean(2,1) - 1

        stats.growth([1, 2, 3, 4], 2, ratio=False)
        # 2.0       == 3.5 - 1.5
    '''
    end = nanmean(series[-period:])
    start = nanmean(series[-2 * period:-period])
    return end / start - 1 if ratio else end - start


def rising(series, period):
    '''
    Returns whether a ``series`` has been steadily rising or falling over
    the last ``period`` periods.
    +1 indicates steadily rising,
    -1 indicates steadily falling,
    0 indicates neither.

    Parameters
    ----------
    series : Pandas Series, numpy array, list or iterable
        Data to find the growth of
    period : int
        Number of periods over which to detect rising behaviour. For example,
        ``period=7`` returns ``1`` if every one of the last 7 values of the
        ``series`` is higher than its immediate previous value.

    Examples
    --------
    Typical usage::

        stats.rising(np.array([0, 1, 2, 3, 4]), 4)    # +1: increasing
        stats.rising(np.array([5, 4, 3, 2, 1]), 4)    # -1: decreasing
        stats.rising(np.array([0, 1, 2, 1, 2]), 4)    #  0: erratic
    '''
    if len(series) < period + 1:
        return 0
    present, past = series[-period:], series[-period - 1:-1]
    if (present > past).all():
        return +1
    if (present < past).all():
        return -1
    return 0


def smooth(points, precision=6, start='M'):
    '''
    Returns the ``d`` attibute of a smooth bezier path through the ``points``.
    Creates a Catmull-Rom spline.

    A typical usage is::

        <path d="{{! stats.smooth([(10,10), (20,20), (10,30), (30,40)]) }}"/>

    Parameters
    ----------
    points : list of (x: float, y: float) tuples
        Points through which the curve must pass through
    precision : int
        Number of decimal places to display in the returned path string
    start : {'M', 'L'}
        By default, path strings start by Moving to the first point. To
        concatenate multiple path strings, you can use ``start=L`` (for
        Line) instead.

    Examples
    --------
    Typical usage::

        <path d="{{! stats.smooth([(10, 10), (20, 20), (10, 30)]) }}"/>
        <path d="{{! stats.smooth([(10, 10), (20, 20),
                                   (10, 30)], precision=1, start='L') }}"/>
    '''
    npoints = len(points)
    if npoints < 2:
        return ''

    formatstring = '%0.'.format(precision) + 'f %0.'.format(precision) + 'f'

    # fmt = lambda x, y: formatstring % (x, y)

    def fmt(x, y):
        """Format function."""
        return formatstring % (x, y)

    path = [start, fmt(points[0][0], points[0][1])]
    if npoints == 2:
        path += ['L', fmt(points[1][0], points[1][1])]
        return ' '.join(path)

    last_but_two = npoints - 2
    for i in range(len(points) - 1):
        if i == 0:
            offsets = [0, 0, 1, 2]
        elif i == last_but_two:
            offsets = [-1, 0, 1, 1]
        else:
            offsets = [-1, 0, 1, 2]

        p = [points[i + offset] for offset in offsets]

        path += [
            'C' + fmt((-p[0][0] + 6 * p[1][0] + p[2][0]) / 6.0,
                      (-p[0][1] + 6 * p[1][1] + p[2][1]) / 6.0),
            fmt((p[1][0] + 6 * p[2][0] - p[3][0]) / 6.0,
                (p[1][1] + 6 * p[2][1] - p[3][1]) / 6.0),
            fmt(p[2][0], p[2][1]),
        ]

    return ' '.join(path)


def decimals(series):
    '''
    Given a ``series`` of numbers, returns the number of decimals
    *just enough* to differentiate between most numbers.

    Parameters
    ----------
    series : Pandas Series, numpy array, list or iterable
        Data to find the required decimal precision for

    Returns
    -------
    decimals : int
        The minimum number of decimals required to differentiate
        between most numbers

    Examples
    --------
    Typical usage::

        stats.decimals([1, 2, 3])       # 0: All integers. No decimals needed
        stats.decimals([.1, .2, .3])    # 1: 1 decimal is required
        stats.decimals([.01, .02, .3])  # 2: 2 decimals are required
        stats.decimals(.01)             # 2: Only 1 no. of 2 decimal precision

    Notes
    -----
    This function first calculates the smallest difference between any pair of
    numbers (ignoring floating-point errors). It then finds the log10 of that
    difference, which represents the minimum decimals required to
    differentiate between these numbers.
    '''
    series = np.ma.masked_array(series, mask=np.isnan(series)).astype(float)
    series = series.reshape((series.size,))
    diffs = np.diff(series[series.argsort()])
    inf_diff = 1e-10
    min_float = .999999
    diffs = diffs[diffs > inf_diff]
    if len(diffs) > 0:
        smallest = np.nanmin(diffs.filled(np.Inf))
    else:
        nonnan = series.compressed()
        smallest = (abs(nonnan[0]) or 1) if len(nonnan) > 0 else 1
    return int(max(0, np.floor(min_float - np.log10(smallest))))


def format(series, comma=False):
    '''
    Returns a ``series`` of numbers formatted as strings with
    *just enough* decimals to differentiate between most numbers.

    Parameters
    ----------
    series : int, float, Pandas Series, numpy array, list or iterable
        Data to convert to strings
    comma : boolean
        Set ``comma=True`` to add thousands comma separator

    Returns
    -------
    result : str, or list of str
        If ``series`` is iterable, returns a list of str.
        Else, just returns a str.
        These are formatted with the minimum precision required.
    '''
    precision = decimals(series)
    if comma:
        format = '{:,.%df}' % precision
    else:
        format = '{:.%df}' % precision
    if hasattr(series, '__iter__'):
        return [format.format(float(val)) for val in series]
    else:
        return format.format(series)


ten = 10
twenty = 20
thirty = 30
fourty = 40
LAKHS = [
    {'above': 1e12, 'divideby': 1e12, 'unit': 'lk cr'},
    {'above': 1e7, 'divideby': 1e7, 'unit': 'cr'},
    {'above': 1e5, 'divideby': 1e5, 'unit': 'lk'},
    {'above': 1e3, 'divideby': 1e0, 'unit': ''},
    {'above': 1e0, 'divideby': 1e0, 'unit': ''},
]

MILLIONS = [
    {'above': 1e12, 'divideby': 1e12, 'unit': 'tn'},
    {'above': 1e9, 'divideby': 1e9, 'unit': 'bn'},
    {'above': 1e6, 'divideby': 1e6, 'unit': 'mn'},
    {'above': 1e3, 'divideby': 1e3, 'unit': 'K'},
    {'above': 1e0, 'divideby': 1e0, 'unit': ''},
]

BYTES = [
    {'above': 2**fourty, 'divideby': 2**fourty, 'unit': 'TB'},
    {'above': 2**thirty, 'divideby': 2**thirty, 'unit': 'GB'},
    {'above': 2**twenty, 'divideby': 2**twenty, 'unit': 'MB'},
    {'above': 2**ten, 'divideby': 2**ten, 'unit': 'KB'},
    {'above': 2**0, 'divideby': 2**0, 'unit': 'bytes'},
]

TIME = [
    {'above': 365 * 86400, 'divideby': 365 * 86400,
     'units': 'years', 'unit': 'year'},
    {'above': thirty * 86400, 'divideby': thirty * 86400,
     'units': 'months', 'unit': 'month'},
    {'above': 7 * 86400, 'divideby': 7 * 86400, 'units': 'weeks', 'unit': 'week'},
    {'above': 86400, 'divideby': 86400, 'units': 'days', 'unit': 'day'},
    {'above': 3600, 'divideby': 3600, 'units': 'hrs', 'unit': 'hr'},
    {'above': 60, 'divideby': 60, 'units': 'mins', 'unit': 'min'},
    {'above': 1, 'divideby': 1, 'unit': 's'},
    {'above': .001, 'divideby': .001, 'unit': 'ms'},
]


def units(scale,
          format='{:,.%df}{:s}',
          prefix='',
          suffix='',
          significance=3,
          max_decimals=4,
          integer=False,
          unitsep=' '):
    '''
    A powerful and flexible unit conversion mechanism. For example::

        rs = stats.units(stats.LAKHS, format='Rs {:,.2f}{:s}')
        rs(100000)          # --> 'Rs 1.00 lk'

        when = stats.units(stats.TIME, format='{:,.0f}{:s}')
        when(86400)         # --> '1 day'

    These scales are pre-defined. See the examples for how to create your own.

    - ``LAKHS``: thousand, lakh, crore, lakh crore
    - ``MILLIONS``: thousand, million, billion, trillion
    - ``BYTES``: bytes, KB, MB, GB, TB
    - ``TIME``: ms, second, minute, hour, day, week, month, year

    Parameters
    ----------
    scale : array of ticks
        Each tick is a dict that should have the following keys

        - above : beyond or at what value does this scale kick in (e.g. 1000)
        - divideby : what should I divide the value by (e.g. 1000)
        - unit : what are the units (e.g. 'thousand')

    format : str
        a format string that takes a float and a string unit.
        ``format`` can contain a '%d' representing number of digits. If so,
        this is replaced by the number of decimals for that format.

        - significance: number of significant digits to show. default: 3
        - max_decimals: maximum number of decimal places allowed. default: 4
        - integer: True if numbers < 1 have no decimals

    unitsep : str
        The character between number and unit (if unit exists)

    Returns
    -------
    converter: function
        A function that converts values into units.

    Examples
    --------
    Currency units::

        rs = stats.units(stats.LAKHS, format='Rs {:,.2f}{:s}')
        rs(1e9)     # Rs 100.00 cr

    Time units::

        when = stats.units(stats.TIME, format='{:,.0f}{:s}')
        when(0.1)           # 100 ms
        when(10)            # 10 s
        when(100)           # 2 mins
        when(1000)          # 17 mins
        when(10000)         # 3 hrs
        when(100000)        # 1 day
        when(1000000)       # 2 weeks
        when(10000000)      # 4 months
        when(100000000)     # 3 years

    You can define a format with a fixed number of decimals::

        usd = stats.units(stats.MILLIONS, format='{:+,.2f}${:s}')
        usd(1e8)            # +100.00$ mn
        usd(0.123)          # +0.12$
        usd(1234)           # +1.23$ K
        usd(12345)          # +12.35$ K
        usd(123456)         # +123.46$ K

    ``significance=`` limits the total number of digits::

        usd = stats.units(stats.MILLIONS, format='{:,.%df}${:s}',
                          significance=3)
        usd(0.123)          # 0.123$
        usd(1234)           # 1.23$ K
        usd(12345)          # 12.3$ K
        usd(123456)         # 123$ K

    ``max_decimals=`` limits the number of digits after the decimal::

        usd = stats.units(stats.MILLIONS, format='{:,.%df}${:s}',
                          max_decimals=1)
        usd(0.123)          # 0.1$
        usd(1234)           # 1.2$ K
        usd(12345)          # 12.3$ K

    You can define your own custom scale::

        BYTES = [
            {'above': 2**40, 'divideby': 2**40, 'unit': 'TB'},
            {'above': 2**30, 'divideby': 2**30, 'unit': 'GB'},
            {'above': 2**20, 'divideby': 2**20, 'unit': 'MB'},
            {'above': 2**10, 'divideby': 2**10, 'unit': 'KB'},
            {'above': 2**0, 'divideby': 2**0, 'unit': 'bytes'},
        ]
        bytes = stats.units(BYTES, format='{:,.0f}{:s}')
        bytes(1000)                     # 1,000 bytes
        bytes(1024)                     # 1 KB
        bytes(2 * 1024 * 1024)          # 2 MB
        bytes(3 * 1024 * 1024 * 1024)   # 3 GB
    '''
    format = prefix + format + suffix
    _scale = [dict(tick) for tick in scale]
    for tick in _scale:
        if unitsep:
            if 'unit' in tick and tick['unit']:
                tick['unit'] = unitsep + tick['unit']
            if 'units' in tick and tick['units']:
                tick['units'] = unitsep + tick['units']
        tick['max'] = 0 if integer and tick['divideby'] == 1 else max_decimals
        tick['divideby'] = float(tick['divideby'])

    if '%d' in format:
        def _units(data):
            '''Convert to string based on a pre-defined precision'''
            i, count = 0, len(_scale) - 1
            while True:
                tick = _scale[i]
                if abs(data) >= tick['above'] or i == count:
                    data = data / tick['divideby']
                    pow10 = np.ceil(np.log10(abs(data))) if data else 1
                    decimals = min(tick['max'],
                                   max(0, int(significance - pow10)))
                    return (format % decimals).format(data, tick['unit'])
                i += 1
    else:
        def _units(data):
            '''Convert to string based on a auto-precision'''
            i, count = 0, len(_scale) - 1
            min_rng = 0.5
            max_rng = 1.5
            while True:
                tick = _scale[i]
                if abs(data) >= tick['above'] or i == count:
                    data = data / tick['divideby']
                    one = 'units' not in tick or (data < max_rng and data >= min_rng)
                    return format.format(
                        data, tick['unit' if one else 'units'])
                i += 1
    return _units


def opacity(prob, method='stars'):
    '''
    Returns an opacity value given a probability / statistical significance.
    This follows the statistics convention of assigning stars.

    Parameters
    ----------
    prob : float
        Statistical significance / probability
    method : {'stars'}
        The method used to assign opacity. Currently, the following methods
        are available:

        ``stars`` : uses the concept of assigning 1, 2 or 3 stars in statistics
            - prob > 0.05: 25% opacity
            - prob > 0.01: 50% opacity
            - prob > 0.001: 75% opacity
            - Else: 100% opacity
    '''
    point_zero_one = 0.01
    point_zero_zero_one = 0.01
    point_zero_five = 0.05
    point_two_five = 0.25
    point_five = 0.50
    point_seven_five = 0.75
    one = 1.00
    if method.lower().startswith('star'):
        return (point_two_five if prob > point_zero_five else
                point_five if prob > point_zero_one else
                point_seven_five if prob > point_zero_zero_one else
                one)
    return one - prob


def round_near(value):
    '''
    Rounds off a positive value's last significant digit to the nearest
    multiple of 2, 5 or 10.

    Parameters
    ----------
    value : float
        The *positive* number to round off

    Returns
    -------
    round : float
        ``value`` with the last significant digit rounded off

    Examples
    --------
    Typical usage::

        stats.round_near(1.4)     # 1
        stats.round_near(3.8)     # 5
        stats.round_near(.094)    # 0.1
        stats.round_near(30)      # 20.0
        stats.round_near(np.inf)  # inf
        stats.round_near(np.nan)  # nan
    '''
    if value == 0 or not np.isfinite(value) or np.isnan(value):
        return value
    if value < 0:
        value = -value
        sign = -1
    else:
        sign = +1
    decimals = 1
    while value > 10:
        value /= 10.
        decimals *= 10.
    while value < 1:
        value *= 10.
        decimals /= 10.

    one_pfive = 1.5
    three_pfive = 3.5
    seven_pfive = 7.5
    one = 1
    two = 2
    five = 5
    ten = 10
    return sign * decimals * (
        one if value < one_pfive else
        two if value < three_pfive else
        five if value < seven_pfive else
        ten)


def ticks(series, count):
    '''
    Returns approximately ``count`` uniform values *within* the ``series``.
    Typically used to plot axis ticks for the ``series``.

    This method ensures that the ticks are at round numbers (which is why the
    number of ticks is approximate -- it may not be possible to have the exact
    number of ticks aligned at round numbers.)

    Parameters
    ----------
    series : list or iterable of float
        Range of values over which ticks are computed
    count : int
        Approximate number of ticks

    Returns
    -------
    ticks : numpy array of float
        Round values of approximately ``count`` ticks in the
        range of ``series``.

    Examples
    --------
    Typical usage::

        stats.ticks([0, 100], 5)
        # np.array([0., 20., 40., 60., 80., 100.])

        stats.ticks([13, 39], 5)
        # np.array([15., 20., 25., 30., 35.])

        stats.ticks([46, 47], 5)
        # np.array([46., 46.2, 46.4, 46.6, 46.8, 47.])
    '''
    series = np.array(series)
    end, start = np.nanmax(series), np.nanmin(series)
    interval = round_near((end - start) / float(count))
    shift = start % interval
    start = start if shift == 0 else start + interval - shift
    ten_pow_ten = 1e-10
    return np.arange(start, end + ten_pow_ten, interval)


def andjoin(series, sep=', ', last=' and '):
    '''
    Joins a ``series`` of strings joined by comma, except the ``last`` one
    which is joined by ``and``. For example::

        stats.andjoin(['A', 'B', 'C'])        # 'A, B and C'

    Parameters
    ----------
    series : list or iterable of str
        Strings to concatenate with a comma and ``and``
    sep : str
        Separator between first few words. Defaults to comma
    last : str
        Separator between last pair of words. Defaults to ``and``

    Examples
    --------
    Typical usage::

        stats.andjoin(['red', 'blue', 'green'])
        # 'red, blue and green'

        stats.andjoin(['red', 'blue', 'green'], sep=' or ', last=None)
        # 'red or blue or green'
    '''
    series = list(series)
    if not last:
        return sep.join(series)
    else:
        if len(series) > 2:
            series = list(series)
            return sep.join(series[:-1]) + last + series[-1]
        else:
            return last.join(series)


class Map(object):
    '''
    Creates transformations functions between a domain and the range, allowing
    interpolation back and forth.

    For example, you can map ranges of numbers, colours, dates and strings
    between each other.

    Parameters
    ----------
    domain : list of (number, color, date or strings)
        Domain values that define the input range.
        These should be steadily increasing or decreasing.
    range : list of (number, color, date or strings)
        Range values. You need exactly as many items as in the ``domain``
    clamp : boolean, optional
        By default, values beyond the ``domain`` are extrapolated beyond
        ``range``. To ensure that they stay within ``range``, set
        ``clamp=True``
    power : float, optional
        By default, a piece-wise linear scale is used. You can change it to a
        power scale with a specified power. For example, ``power=0.5`` defines
        a square-root scale.

    Returns
    -------
    map : function
        A function that converts a value in the domain to the range.

    Examples
    --------
    Piece-wise linear domain and range::

        g = stats.Map([0, 0.5, 1], [0, 10, 20])
        g(.1)       #   2.0
        g(1.5)      #  30.0 (extrapolated)
        g(-2)       # -40.0 (extrapolated)

    Extrapolations can be clamped::

        g = stats.Map([0, 0.5, 1], [0, 10, 20], clamp=True)
        g(1.5)      # 20.0 (clamped)
        g(-2)       #  0.0 (clamped)

    Interpolation can be on a power scale::

        g = stats.Map([1, 2, 3], [1, 4, 9], power=2)
        g(1.5)      # 1.75

    Colours can be interpolated::

        g = stats.Map([0, .2, .4], ['#f00', '#ff0', '#fff'])
        g(.1)               # #ff7f00: Returns midpoint of #f00 and #ff0
        g(.3)               # #ffff7f: Midpoint between #ff0 and #fff
        g.invert(g(.3))     # 0.2 ... but colour inversion isn't guaranteed

    In particular, :mod:`color` gradients can be interpolated. Only the
    colour values from the gradients are used::

        import color as _color
        g = stats.Map([0, .2, .4], _color.RdYlGn)
        g(0)                # #d73027: first colour in _color.RdYlGn
        g(.2)               # #ffffbf: second colour in _color.RdYlGn
        g(.4)               # #199850: third & last colour in _color.RdYlGn
    '''
    def __init__(self, domain, range, clamp=False, power=1):
        self.domain = list(domain)
        if isinstance(range[0], list):
            self.range = [val[-1] for val in range]
        else:
            self.range = list(range)
        self.clamp = clamp
        self.power = power

        if self.domain[0] <= self.domain[-1]:
            self._find_domain = self._find_forward
        else:
            self._find_domain = self._find_reverse

        if self.range[0] <= self.range[-1]:
            self._find_range = self._find_forward
        else:
            self._find_range = self._find_reverse

        self.t2d, self.d2t = self._map_functions(self.domain[0])
        self.t2r, self.r2t = self._map_functions(self.range[0])

    def _map_functions(self, value):
        '''Find type(``value``) and return its map and inverse functions'''
        try:
            float(value)
            return self._number, self._invert_number
        except Exception:
            pass

        try:
            color.rgba(value)
            return self._color, self._invert_color
        except Exception:
            pass

        try:
            time.mktime(value.timetuple())
            return self._date, self._invert_date
        except Exception:
            pass

        return self._discrete, self._invert_discrete

    @staticmethod
    def _find_forward(value, series, clamp=False):
        '''Find the index and value of a given value in an increasing series'''
        i = 0
        while i + 2 < len(series) and value > series[i + 1]:
            i += 1
        if clamp:
            if value < series[0]:
                value = series[0]
            elif value > series[-1]:
                value = series[-1]
        return i, value

    @staticmethod
    def _find_reverse(value, series, clamp=False):
        '''Find the index and value of a given value in an decreasing series'''
        i = len(series) - 2
        while i > 0 and value > series[i]:
            i -= 1
        if clamp:
            value = (series[0] if value > series[0] else
                     series[-1] if value < series[-1] else value)
        return i, value

    def __call__(self, value):
        '''Convert the value from the domain to the range.'''
        i, value = self._find_domain(value, self.domain, self.clamp)
        pos = self.d2t(self.domain[i], self.domain[i + 1], value)
        return self.t2r(self.range[i], self.range[i + 1], pos ** self.power)

    def invert(self, value):
        '''If possible, invert the value and convert into the domain'''
        i, value = self._find_range(value, self.range)
        pos = self.r2t(self.range[i], self.range[i + 1], value)
        return self.t2d(self.domain[i], self.domain[i + 1],
                        pos ** (1 / self.power))

    # Type-specific functions that define how to handle

    @staticmethod
    def _number(start, end, pos):
        '''
        Find a value at position ``pos`` between ``start`` and ``end``

        Examples
        --------
        Typical usage::

            stats.Map._number(3, 9, 0)    # 3
            stats.Map._number(3, 9, 0.5)  # 6
            stats.Map._number(3, 9, 1)    # 9
        '''
        return start + (end - start) * pos

    @staticmethod
    def _invert_number(start, end, value):
        '''
        Find the position of a ``value`` between ``start`` and ``end``

        Examples
        --------
        Typical usage::

            stats.Map._invert_number(3, 9, 3)     # 0
            stats.Map._invert_number(3, 9, 6)     # 0.5
            stats.Map._invert_number(3, 9, 9)     # 1
        '''
        return float(value - start) / (end - start)

    @staticmethod
    def _color(start, end, pos):
        '''
        Interpolate in the HSL color space.

        Examples
        --------
        Typical usage::

            stats.Map._color('blue', 'white', .5)     # #7f7fff
            stats.Map._color('blue', 'red', .5)       # #f0f
        '''
        color1, color2 = color.hsla(start), color.hsla(end)
        colors = list(Map._number(va, vb, pos)
                      for va, vb in zip(color1, color2))

        # TODO: Use HCL, and fall back to HSL
        # http://stackoverflow.com/q/2593832
        if not -0.5 < color1[0] - color2[0] < 0.5:
            hue1 = color1[0] - 1 if color1[0] > 0.5 else color1[0]
            hue2 = color2[0] - 1 if color2[0] > 0.5 else color2[0]
            colors[0] = Map._number(hue1, hue2, pos) % 1.
        else:
            colors[0] = colors[0] % 1.

        # If one of the colours has saturation = 0, hue is undefined. Use the
        # other's hue
        if color1[1] == 0:
            colors[0] = color2[0]
        elif color2[1] == 0:
            colors[0] = color1[0]

        # Clamp
        for index in range(1, 4):
            if colors[index] < 0 or np.isnan(colors[index]):
                colors[index] = 0
            elif colors[index] > 1:
                colors[index] = 1

        rgb = colorsys.hsv_to_rgb(colors[0], colors[1], colors[2])
        return color.name(*(rgb + (colors[3],)))

    @staticmethod
    def _invert_color(start, end, value):
        '''
        Uninterpolate hue. If that's same, use lightness, then saturation

        Examples
        --------
        Typical usage::

            stats.Map._invert_color('blue', 'white', 'blue')    # -0.0
            stats.Map._invert_color('blue', 'red', 'white')     #  1.0
        '''
        start = color.hsla(start)
        end = color.hsla(end)
        value = color.hsla(value)
        if start[0] != end[0]:
            return Map._invert_number(start[0], end[0], value[0])
        elif start[2] != end[2]:
            return Map._invert_number(start[2], end[2], value[2])
        else:
            return Map._invert_number(start[1], end[1], value[1])

    @staticmethod
    def _date(start, end, pos):
        '''
        Interpolate date

        Examples
        --------
        Typical usage::

            stats.Map._date(datetime(2000, 1, 1), datetime(2000, 3, 1), .5)
            # datetime.datetime(2000, 1, 31, 0, 0)
        '''
        start = time.mktime(start.timetuple())
        end = time.mktime(end.timetuple())
        return datetime.fromtimestamp(start + (end - start) * pos)

    @staticmethod
    def _invert_date(start, end, value):
        '''
        Uninterpolate date

        Examples
        --------
        Typical usage::

            stats.Map._invert_date(datetime(2000, 1, 1), datetime(2000, 3, 1),
                                   datetime(2000, 1, 31))
            # 0.5
        '''
        start = time.mktime(start.timetuple())
        end = time.mktime(end.timetuple())
        value = time.mktime(value.timetuple())
        return (value - start) / (end - start)

    @staticmethod
    def _discrete(start, end, pos):
        '''
        Interpolate string

        Examples
        --------
        Typical usage::

            stats.Map._discrete('a', 'b', 0.2)    # 'a'
            stats.Map._discrete('a', 'b', 0.5)    # 'b'
            stats.Map._discrete('a', 'b', 0.8)    # 'b'
        '''
        return start if pos < .5 else end

    @staticmethod
    def _invert_discrete(start, end, value):
        '''
        Uninterpolate string

        Examples
        --------
        Typical usage::

            stats.Map._invert_discrete('a', 'b', 'a')     # 0.0
            stats.Map._invert_discrete('a', 'b', 'b')     # 1.0
        '''
        if value == start:
            return 0.0
        elif value == end:
            return 1.0
        else:
            raise ValueError('Invalid value')


def to_date(dates, **args):
    '''
    Converts a Pandas series containing date strings into datetimes
    *efficiently* if there are very few distinct date strings. Use this for
    dates, not date + time strings -- there is no likely performance benefit
    there (though the function will work fine.)

    Parameters
    ----------
    dates : Pandas Series of date strings
        List of date strings to be converted to datetime
    errors, dayfirst, utc, box, format, ... : pd.to_datetime arguments
        Any arguments valid for ``pd.to_datetime`` works.

    Returns
    -------
    series : Pandas series of datetime objects

    '''
    return dates.map({v: pd.to_datetime(v, **args) for v in dates.unique()})


def groupby(data, groups, agg, fillna=None):
    '''
    Create groups with subtotals.

    Parameters
    ----------
    data : Pandas DataFrame
        The data that must be grouped
    groups : List of columns
        Levels by which the data must be grouped
    agg : list of functions, or dict of column: function
        Defines how columns should be aggregated. Same parameter as Pandas
        ``groupby().agg(...)``
    fillna : scalar (default: NaN)
        The sub-totals and grand total will be named what's in this column

    Returns
    -------
    dataframe : pd.DataFrame
        Result grouped by ``groups``, with columns as per ``agg``

    Examples
    --------
    If the dataset looks like this::

        Country   State     Month   Population  Income
        USA       Alabama   Jan-15       11950   24766
        USA       Alaska    Jan-15       48989    4885
        USA       Arizona   Jan-15        1302   14949
        India     Gurarat   Jan-15        2985    7778
        India     Kerala    Jan-15        1362   32240
        India     Bihar     Jan-15       42820   44700
        USA       Alabama   Feb-15       19094   55426
        USA       Alaska    Feb-15        2753    3221
        USA       Arizona   Feb-15        1570   15373
        India     Gurarat   Feb-15       78745   12690
        India     Kerala    Feb-15       45415   34453
        India     Bihar     Feb-15       39041   16295
        USA       Alabama   Mar-15       72286   57334
        USA       Alaska    Mar-15       29694   15930
        USA       Arizona   Mar-15        2144   70806
        India     Gurarat   Mar-15       21068   35126
        India     Kerala    Mar-15       45108    2233
        India     Bihar     Mar-15        7354    2415

    Then the result of::

        stats.groupby(data, ['Country', 'State'], {
            'Population': 'sum',
            'Income': 'sum',
        }, fillna='Total')

    ... looks like this::

        level   Country   State   Population  Income
            0   Total     Total       473680  450620    <- grand total
            1   USA       Total       189782  262690    <- sub total by Country
            1   India     Total       283898  187930    <- sub total by Country
            2   USA       Alabama     103330  137526    <- groupby
            2   USA       Alaska       81436   24036
            2   USA       Arizona       5016  101128
            2   India     Gurarat     102798   55594
            2   India     Kerala       91885   68926
            2   India     Bihar        89215   63410

    The first row has the grand total of all metrics. The next set of rows
    have the sub-total by the first ``groupby`` element, then the first two
    ``groupby`` elements, and so on.

    Totals are replaced by the ``Total`` word because we've specified
    ``fillna='Total'``. You can use any other string. By default, the totals
    are filled with ``NaN``.

    For columns of type string, the function does not accepts ``sum`` as a
    parameter for  aggregation. Since, it might result in creation of
    very lengthy string.
        '''
    for col, agg_func in six.iteritems(agg):
        if data[col].dtype == object and agg_func == 'sum':
            raise NotImplementedError('Do not sum object columns')
    grand_total = data.groupby(np.zeros(len(data)), sort=False).agg(agg)
    grand_total['level'] = 0
    frames = [grand_total]
    for level in range(1, 1 + len(groups)):
        frame = data.groupby(
            groups[:level],
            sort=False,
            as_index=False
        ).agg(agg)
        frame['level'] = level
        frames.append(frame)
    result = pd.concat(frames, ignore_index=True)
    if fillna is not None:
        result[groups] = result[groups].astype(object).fillna(fillna)
    return result


class Filter(object):
    '''
    Filter support for DataFrames.

    Parameters
    ----------
    data : DataFrame
        Indices will be created on this DataFrame to speed up filtering
    cols : list of columns, default None
        Indices will be created only for these columns
    key : str
        Filter indices are cached by this key. You are strongly advised to
        provide a unique string for each dataset to reduce memory usage.
    max_distinct : int, default None
        Columns with more distinct values will be ignored. If some columns
        have too many values and are should be ignored (e.g. an unique ID
        column), use ``max_distinct``

    Examples
    --------
    Here's a typical use in a template:
    '''
    cache = {}

    def __init__(self, data, cols=None, key=None, max_distinct=None):
        self.data = data
        self.cols = data.columns if cols is None else cols
        if key is None:
            key = '\t'.join(['{}'.format(id(data))] + ['{}'.format(col) for col in self.cols])
        if key in Filter.cache:
            self.indices = Filter.cache[key]
        else:
            Filter.cache[key] = self.indices = {}
            for col in self.cols:
                values = data[col]
                groupby = values.groupby(values, sort=False)
                # Ignore columns with more than max_distinct distinct values
                if max_distinct and groupby.ngroups > max_distinct:
                    continue
                self.indices[col] = groupby.indices

    def by(self, col, values):
        '''
        Filters a column by one or more values and returning the rows of the
        DataFrame (suitable for use in DataFrame.iloc).

        Returns None if the column does not exist, or no values are provided.
        None means the same as "all values", i.e. the entire dataset.

        Parameters
        ----------
        col : column name to filter
            If the column is not indexed, returns None
        values : value or list/tuple/iterable
            Rows matching ANY of the values ("OR") are returned

        Examples
        --------
        Typical usage::

            data = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
            select = stats.Filter(data, key='sample-data')
            rows = select.by('A', 1)
            data.iloc[rows]

        This returns the DataFrame::

               A  B
            0  1  3
        '''
        indices = self.indices.get(col)
        if indices is None:
            return None
        if hasattr(values, '__iter__') and not isinstance(values, six.string_types):
            rows = None
            for value in values:
                index = indices.get(value, _NP_EMPTY_INT_ARRAY)
                rows = index if rows is None else np.union1d(rows, index)
        else:
            rows = indices.get(values, _NP_EMPTY_INT_ARRAY)
        return rows

    def filter(self, filters, ignore=None):
        '''
        Returns a filtered DataFrame based on the provided filters.

        Parameters
        ----------
        filters : dictionary of {column: values}
            values may be a single value or a list/tuple/iterable.
            Rows matching ANY of the values ("OR") are returned
        ignore : list/iterable of filter columns to ignore, default None
            A convenience parameter to ignore specific filter columns.
            Used internally by :func:`Filter.apply()`

        Examples
        --------
        Typical usage::

            data = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
            select = stats.Filter(data, key='sample-data')
            select.filter({'A': 1, 'B': 3})

        This returns the DataFrame::

               A  B
            0  1  3
        '''
        rows = self.rows(filters, ignore)
        return self.data if rows is None else self.data.iloc[rows]

    def rows(self, filters=None, ignore=None, rows=None):
        '''
        Filters multiple columns and returns matching rows of the DataFrame
        (suitable for use in DataFrame.iloc)

        Generally, you'd use :func:`Filter.filter()` rathar than this method.

        Parameters
        ----------
        filters : dictionary of {column: values}
            values may be a single value or a list/tuple/iterable.
            Rows matching ANY of the values ("OR") are returned
        ignore : list/iterable of filter columns to ignore, default None
            A convenience parameter to ignore specific filter columns.
            Used internally by :func:`Filter.apply()`
        rows : list of previously matching rows, default None
            Provides a starting point to resume filtering.
            Used internally by :func:`Filter.apply()`

        Examples
        --------
        Typical usage::

            data = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
            select = stats.Filter(data, key='sample-data')
            rows = select.rows({'A': 1, 'B': 3})
            data.iloc[rows]

        This returns the DataFrame::

               A  B
            0  1  3
        '''
        if filters is not None:
            for col, values in six.iteritems(filters):
                if ignore is not None and col in ignore:
                    continue
                new = self.by(col, values)
                if new is not None:
                    rows = new if rows is None else np.intersect1d(rows, new)
        return rows

    def apply(self, cols, filters, method):
        '''
        See :func:`Filter.unique` and :func:`Filter.value_counts`

        Aggregates one or more columns after applying filters *except to the
        column itself*. For example, if there are 3 columns A, B, C, then

        - column A is aggregated by applying filters B and C
        - column B is aggregated by applying filters A and C
        - column C is aggregated by applying filters A and B

        This ensures that values for a given column are not the trivial list
        of passed filter values. This also mimics Excel filter behaviour.

        Parameters
        ----------
        cols : list/tuple/iterable of column names
            Columns that are not indexed, are ignored
        filters : dictionary of {column: values}
            values may be a single value or a list/tuple/iterable.
            Rows matching ANY of the values ("OR") are returned
        method : series aggregation function
            'unique' and 'value_counts' are often used
        '''
        colset = {col for col in cols if col in self.indices}
        common = self.rows(filters, ignore=colset)
        rest = {col: values for col, values in six.iteritems(filters)
                if col in colset}
        result = {}
        for col in cols:
            rows = self.rows(rest, ignore={col}, rows=common)
            sub = self.data if rows is None else self.data.iloc[rows]
            result[col] = getattr(sub[col], method)()
        return result

    def unique(self, cols, filters):
        '''
        Returns unique values in one or more columns after applying filters
        *except to the column itself*. For example, if there are 3 columns A,
        B, C, then it returns unique values for 'A' after applying filters for
        B and C, but not A itself.

        Parameters
        ----------
        cols : list/tuple/iterable of column names
            Columns that are not indexed, are ignored
        filters : dictionary of {column: values}
            values may be a single value or a list/tuple/iterable.
            Rows matching ANY of the values ("OR") are returned

        Examples
        --------
        Typical usage::

            data = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [1, 1, 2, 2]})
            select = stats.Filter(data, key='sample-data')
            select.unique(['A', 'B'], {'A': 1, 'B': 2})

        This returns the dictionary::
            {'A': array([3, 4], dtype=int64),
             'B': array([1], dtype=int64)}
        '''
        if hasattr(cols, '__iter__') and not isinstance(cols, six.string_types):
            return self.apply(cols, filters, 'unique')
        else:
            return self.apply([cols], filters, 'unique')[cols]

    def value_counts(self, cols, filters):
        '''
        Returns frequency counts in one or more columns after applying filters
        *except to the column itself*. For example, if there are 3 columns A,
        B, C, then it returns the frequency counts for 'A' after applying
        filters for B and C, but not A itself.

        Parameters
        ----------
        cols : list/tuple/iterable of column names
            Columns that are not indexed, are ignored
        filters : dictionary of {column: values}
            values may be a single value or a list/tuple/iterable.
            Rows matching ANY of the values ("OR") are returned

        Examples
        --------
        Typical usage::

            data = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [1, 1, 2, 2]})
            select = stats.Filter(data, key='sample-data')
            result = select.value_counts(['A', 'B'], {'A': 1, 'B': 2})
            result['A'].to_dict()   # {3: 1, 4: 1}
            result['B'].to_dict()   # {1: 1}
        '''
        if hasattr(cols, '__iter__') and not isinstance(cols, six.string_types):
            return self.apply(cols, filters, 'value_counts')
        else:
            return self.apply([cols], filters, 'value_counts')[cols]


def unid(key=None):
    '''
    Generates a unique string identifier every time it is called

    Parameters
    ----------
    key : optional namespace for the id
        Returned values are guaranteed to be unique within the namespace

    Examples
    --------
    Typical usage::

        stats.unid('x')       # u'x_1'
        stats.unid('x')       # u'x_2'
        stats.unid('y')       # u'y_1'
    '''
    _ID[key] = _ID.get(key, 0) + 1
    return '{:s}_{:d}'.format('{}'.format(key), _ID[key])
