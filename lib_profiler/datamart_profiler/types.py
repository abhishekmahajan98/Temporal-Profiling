# Column types

MISSING_DATA = 'https://metadata.datadrivendiscovery.org/types/MissingData'
"""No data (whole column is missing)"""

INTEGER = 'http://schema.org/Integer'
"""Integer (numbers without a decimal point)"""

FLOAT = 'http://schema.org/Float'
"""Floating-point numbers"""

TEXT = 'http://schema.org/Text'
"""Text, better represented as strings"""

BOOLEAN = 'http://schema.org/Boolean'
"""Booleans, e.g. only the two values \"true\" and \"false\""""

LATITUDE = 'http://schema.org/latitude'
"""Numerical values representing latitude coordinates"""

LONGITUDE = 'http://schema.org/longitude'
"""Numerical values representing longitude coordinates"""

DATE_TIME = 'http://schema.org/DateTime'
"""A specific instant in time (not partial ones such as "July 4" or "12am")"""

#Added new Datatype as Date ONLY
DATE = 'http://schema.org/Date'
"""A date value in ISO 8601"""

#Added new Datatyoe as Time ONLY
TIME = 'http://schema.org/Time'
"""A point in time recurring on multiple days in the form hh:mm:ss[Z|(+|-)hh:mm]"""

ADDRESS = 'http://schema.org/address'
"""The street address of a location"""

ADMIN = 'http://schema.org/AdministrativeArea'
"""A named administrative area, such as a country, state, or city"""

URL = 'http://schema.org/URL'
"""A URL"""

FILE_PATH = 'https://metadata.datadrivendiscovery.org/types/FileName'
"""A filename"""

ID = 'http://schema.org/identifier'
"""An identifier"""

CATEGORICAL = 'http://schema.org/Enumeration'
"""Categorical values, i.e. drawn from a limited number of options"""

GEO_POINT = 'http://schema.org/GeoCoordinates'
"""A geographic location (latitude+longitude coordinates)"""

GEO_POLYGON = 'http://schema.org/GeoShape'
"""A geographic shape described by its coordinates"""


# Dataset types

DATASET_NUMERICAL = 'numerical'
DATASET_CATEGORICAL = 'categorical'
DATASET_SPATIAL = 'spatial'
DATASET_TEMPORAL = 'temporal'
