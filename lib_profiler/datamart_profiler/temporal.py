import collections
from collections import Counter
from datetime import datetime
import dateutil.parser
import dateutil.tz
import logging
import pandas

from .warning_tools import raise_warnings


logger = logging.getLogger(__name__)


# Keep in sync with frontend's TemporalResolution
temporal_aggregation_keys = {
    'year': '%Y',
    'quarter': lambda dt: dt.__class__(
        year=dt.year,
        month=((dt.month - 1) // 3) * 3 + 1,
        day=1,
        tzinfo=dt.tzinfo,
    ),
    'month': '%Y-%m',
    'week': lambda dt: (
        # Simply using "%Y-%W" doesn't work at year boundaries
        # Map each timestamp to the first day of its week
        (dt - pandas.Timedelta(days=dt.weekday())).strftime('%Y-%m-%d')
    ),
    'day': '%Y-%m-%d',
    'hour': '%Y-%m-%d %H',
    'minute': '%Y-%m-%d %H:%M',
    'second': '%Y-%m-%d %H:%M:%S',
}


def get_temporal_resolution(values):
    """Returns the resolution of the temporal attribute.
    """

    if not isinstance(values, set):
        values = set(values)

    if len(values) == 1:
        value, = values
        if value.second:
            return 'second'
        elif value.minute:
            return 'minute'
        elif value.hour:
            return 'hour'
        else:
            return 'day'

    # Python 3.7+ iterates on dict in insertion order
    for resolution, key in temporal_aggregation_keys.items():
        counts = collections.defaultdict(collections.Counter)
        if isinstance(key, str):
            for value in values:
                bin = value.strftime(key)
                counts[bin][value] += 1
        else:
            for value in values:
                bin = key(value)
                counts[bin][value] += 1

        avg_per_bin = sum(len(v) for v in counts.values()) / len(counts)
        if avg_per_bin < 1.05:
            # 5 % error tolerated
            return resolution

    return 'second'


def detect_quarter(timestamp):
    # Convert timestamp string to datetime object
    #timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

    # Extract the month from the timestamp
    month = timestamp.month

    # Determine the quarter based on the month
    if 1 <= month <= 3:
        return 1
    elif 4 <= month <= 6:
        return 2
    elif 7 <= month <= 9:
        return 3
    else:
        return 4

def getQuarterData(values):
    quarter_counts = Counter(map(detect_quarter, values))

    # Calculate percentages
    total_timestamps = len(values)
    quarter_percentages = {quarter: count / total_timestamps * 100 for quarter, count in quarter_counts.items()}

    return quarter_percentages

def detect_week(timestamp):
    #timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    week_number = timestamp.isocalendar()[1]
    return week_number

def getWeekData(timestamps):
    # Count occurrences of each week
    week_counts = Counter(map(detect_week, timestamps))

    # Calculate percentages
    total_timestamps = len(timestamps)
    week_percentages = {week: count / total_timestamps * 100 for week, count in week_counts.items()}

    return week_percentages
def detect_time_of_day(timestamp):
    #timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    hour = timestamp.hour

    if 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 18:
        return "afternoon"
    elif 18 <= hour < 24:
        return "evening"
    else:
        return "night"

def getTimeOfDayData(timestamps):
    # Count occurrences of each time of day
    time_of_day_counts = Counter(map(detect_time_of_day, timestamps))

    # Calculate percentages
    total_timestamps = len(timestamps)
    time_of_day_percentages = {time_of_day: count / total_timestamps * 100 for time_of_day, count in time_of_day_counts.items()}

    return time_of_day_percentages

_defaults = datetime(1985, 1, 1), datetime(2005, 6, 1)


def parse_date(string):
    """Parse a full date from a string.

    This will accept dates with low precision, but reject strings that only
    mention a time or a partial date, e.g. ``"June 6 11:00"`` returns None
    (could be any year) but ``"June 2020"`` parses into
    ``2020-06-01 00:00:00 UTC``
    """
    with raise_warnings(dateutil.parser.UnknownTimezoneWarning):
        # This is a dirty trick because dateutil returns a datetime for strings
        # that only contain times. We parse it twice with different defaults,
        # so we can tell whether the default date is used in the result
        try:
            dt1 = dateutil.parser.parse(string, default=_defaults[0])
            dt2 = dateutil.parser.parse(string, default=_defaults[1])
        except Exception:  # ValueError, OverflowError, UnknownTimezoneWarning
            return None

    if dt1 != dt2:
        # It was not a date, just a time; no good
        return None

    # If no timezone was read, assume UTC
    if dt1.tzinfo is None:
        dt1 = dt1.replace(tzinfo=dateutil.tz.UTC)
    return dt1

def checkAndCombineTemporalColumns(data, column_meta):
    # col_names = data.columns
    # #print(col_names)
    # if 'year' in col_names and 'month' in col_names and 'day' in col_names:
    #   hours = df['hours'] if 'hours' in columns else '0'
    #   minutes = df['minutes'] if 'minutes' in columns else '0'
    #   seconds = df['seconds'] if 'seconds' in columns else '0'
    #   data['gen_timestamp'] = pd.to_datetime(data[['year', 'month', 'day', 'hours', 'minutes', 'seconds']]).astype('str')
    #   columns.append({'name':'gen_timestamp'})

    # #print(columns)
    # return data,columns

    # Extract column names and their resolutions from column_meta
    resolutions = {}
    for col in column_meta['temporal_coverage']:
        if col['temporal_resolution']:
          if 'day' in col['temporal_resolution'] or 'month' in col['temporal_resolution'] or 'year' in col['temporal_resolution']:
            resolutions[col['temporal_resolution']] = col['column_names'][0]

    if(len(resolutions) > 0):
      data['Concatenated Date'] = 'DD-MM-YYYY'
      for col_type, col in resolutions.items():
        if col_type == 'day':
          data['Concatenated Date'] = data.apply(lambda row: row['Concatenated Date'].replace('DD', row[col]), axis=1)
          continue
        if col_type == 'month':
          data['Concatenated Date'] = data.apply(lambda row: row['Concatenated Date'].replace('MM', row[col]), axis=1)
          continue
        if col_type == 'year':
          data['Concatenated Date'] = data.apply(lambda row: row['Concatenated Date'].replace('YYYY', row[col]), axis=1)
          continue

      data['Concatenated Date'] = pandas.to_datetime(data['Concatenated Date'])

    return data, column_meta