# -*- coding: utf-8 -*-
##  Photini - a simple photo metadata editor.
##  http://github.com/jim-easterbrook/Photini
##  Copyright (C) 2012-17  Jim Easterbrook  jim@jim-easterbrook.me.uk
##
##  This program is free software: you can redistribute it and/or
##  modify it under the terms of the GNU General Public License as
##  published by the Free Software Foundation, either version 3 of the
##  License, or (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##  General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see
##  <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import codecs
from datetime import datetime
from fractions import Fraction
import locale
import logging
import os
import re

try:
    import pgi
    pgi.install_as_gi()
    using_pgi = True
except ImportError:
    using_pgi = False
import gi
for gexiv2_vsn in ('0.10', '0.4'):
    try:
        gi.require_version('GExiv2', gexiv2_vsn)
        break
    except ValueError:
        pass
from gi.repository import GLib, GObject, GExiv2
import six

from photini import __version__

logger = logging.getLogger(__name__)

gexiv2_version = '{} {}, GExiv2 {}.{}.{}, GObject {}'.format(
    ('PyGI', 'pgi')[using_pgi], gi.__version__, GExiv2.MAJOR_VERSION,
    GExiv2.MINOR_VERSION, GExiv2.MICRO_VERSION, GObject._version)

# pydoc gi.repository.GExiv2.Metadata is useful to see methods available

GExiv2.initialize()

# we can't reroute GExiv2 messages to Python logging, so mute them...
GExiv2.log_set_level(GExiv2.LogLevel.MUTE)

# ...unless in test mode
def debug_metadata():
    GExiv2.log_set_level(GExiv2.LogLevel.INFO)

# recent versions of Exiv2 have these namespaces defined, but older versions
# may not recognise them
for prefix, name in (
        ('video',   'http://www.video/'),
        ('xmpGImg', 'http://ns.adobe.com/xap/1.0/g/img/')):
    GExiv2.Metadata.register_xmp_namespace(name, prefix)

def safe_fraction(value):
    # Avoid ZeroDivisionError when '0/0' used for zero values in Exif
    if isinstance(value, six.string_types):
        numerator, sep, denominator = value.partition('/')
        if denominator and int(denominator) == 0:
            return Fraction(0.0)
    return Fraction(value).limit_denominator(1000000)


class MetadataValue(object):
    # base for classes that store a metadata value, e.g. a string, int
    # or float
    def __init__(self, value):
        assert(value is not None)
        self.value = value

    @classmethod
    def from_file(cls, tag, file_value):
        return cls(file_value)

    def to_exif(self):
        return self.value

    def to_iptc(self):
        return self.value

    def to_xmp(self):
        return self.value

    def __str__(self):
        return six.text_type(self.value)

    def __nonzero__(self):
        return bool(self.value)

    def __eq__(self, other):
        return isinstance(other, MetadataValue) and self.value == other.value

    def __ne__(self, other):
        return not isinstance(other, MetadataValue) or self.value != other.value

    def contains(self, other):
        # "contains" = no need to merge or replace.
        return (not other) or (other.value == self.value)

    def merge(self, other, family=None):
        # Only called if contains returns False. Returns True if other
        # merged into self, False if self should be replaced by other.
        return False


class MetadataDictValue(MetadataValue):
    # base for classes that store a dictionary of metadata values, e.g.
    # latitude & longitude
    value = {}

    def __getattr__(self, name):
        if name in self.value:
            return self.value[name]
        return super(MetadataDictValue, self).__getattr__(name)

    def __setattr__(self, name, value):
        if name in self.value:
            self.value[name] = value
            return
        super(MetadataDictValue, self).__setattr__(name, value)


class FocalLength(MetadataDictValue):
    # store actual focal length and 35mm film equivalent
    def __init__(self, value):
        if isinstance(value, six.string_types):
            value = value.split(',')
        fl, fl_35 = value
        if fl in (None, ''):
            fl = None
        else:
            fl = safe_fraction(fl)
        if fl_35 in (None, ''):
            fl_35 = None
        else:
            fl_35 = int(fl_35)
        super(FocalLength, self).__init__({'fl': fl, 'fl_35': fl_35})

    @classmethod
    def from_file(cls, tag, file_value):
        focal_length, focal_length_35mm = file_value
        return cls((focal_length, focal_length_35mm))

    def to_exif(self):
        if self.fl is None:
            focal_length = None
        else:
            focal_length = '{:d}/{:d}'.format(
                self.fl.numerator, self.fl.denominator)
        if self.fl_35 is None:
            focal_length_35mm = None
        else:
            focal_length_35mm = '{:d}'.format(self.fl_35)
        return focal_length, focal_length_35mm

    def to_35(self, value):
        if self.fl and self.fl_35:
            return int((float(value) * self.fl_35 / self.fl) + 0.5)
        return None

    def from_35(self, value):
        if self.fl and self.fl_35:
            return round(float(value) * self.fl / self.fl_35, 2)
        return None

    def __nonzero__(self):
        return (self.fl is not None) or (self.fl_35 is not None)

    def contains(self, other):
        return (not other) or ((other.fl in (None, self.fl)) and
                               (other.fl_35 in (None, self.fl_35)))

    def merge(self, other, family=None):
        if self.fl is None:
            self.fl = other.fl
        if self.fl_35 is None:
            self.fl_35 = other.fl_35
        return True


class LatLon(MetadataDictValue):
    # simple class to store latitude and longitude
    def __init__(self, value):
        if isinstance(value, six.string_types):
            value = value.split(',')
        lat, lon = value
        super(LatLon, self).__init__({
            'lat' : round(float(lat), 6),
            'lon' : round(float(lon), 6),
            })

    # Do something different with Xmp.video tags
    @classmethod
    def from_file(cls, tag, file_value):
        if isinstance(tag, six.string_types) and tag.startswith('Xmp.video'):
            match = re.match(r'([-+]\d+\.\d+)([-+]\d+\.\d+)', file_value)
            if not match:
                return None
            return cls(match.group(1, 2))
        if not all(file_value):
            return None
        if MetadataHandler.is_exif_tag(tag):
            lat_string, lat_ref, lon_string, lon_ref = file_value
            return cls((cls.from_exif_part(lat_string, lat_ref),
                        cls.from_exif_part(lon_string, lon_ref)))
        lat_string, lon_string = file_value
        return cls((cls.from_xmp_part(lat_string), cls.from_xmp_part(lon_string)))

    @staticmethod
    def from_exif_part(value, ref):
        parts = [float(Fraction(x)) for x in value.split()] + [0.0, 0.0]
        result = parts[0] + (parts[1] / 60.0) + (parts[2] / 3600.0)
        if ref in ('S', 'W'):
            result = -result
        return result

    @staticmethod
    def to_exif_part(value):
        if value >= 0.0:
            negative = False
        else:
            negative = True
            value = -value
        degrees = int(value)
        value = (value - degrees) * 60.0
        minutes = int(value)
        seconds = (value - minutes) * 60.0
        seconds = safe_fraction(seconds)
        return '{:d}/1 {:d}/1 {:d}/{:d}'.format(
            degrees, minutes, seconds.numerator, seconds.denominator), negative

    def to_exif(self):
        lat_string, negative = self.to_exif_part(self.lat)
        lat_ref = 'NS'[negative]
        lon_string, negative = self.to_exif_part(self.lon)
        lon_ref = 'EW'[negative]
        return lat_string, lat_ref, lon_string, lon_ref

    @staticmethod
    def from_xmp_part(value):
        ref = value[-1]
        if ref in ('N', 'S', 'E', 'W'):
            value = value[:-1]
        if ',' in value:
            degrees, minutes = value.split(',')
            value = float(degrees) + (float(minutes) / 60.0)
        else:
            value = float(value)
        if ref in ('S', 'W'):
            value = -value
        return value

    def __str__(self):
        return '{:.6f}, {:.6f}'.format(self.lat, self.lon)

    def contains(self, other):
        return (not other) or ((abs(other.lat - self.lat) < 0.000001) and
                               (abs(other.lon - self.lon) < 0.000001))


class Location(MetadataDictValue):
    # stores IPTC defined location heirarchy
    def __init__(self, value):
        if isinstance(value, dict):
            value = (value['sublocation'], value['city'],
                     value['province_state'], value['country_name'],
                     value['country_code'], value['world_region'])
        elif isinstance(value, six.string_types):
            value = value.split(',')
        value = [x or None for x in value]
        country_code = value[4]
        if country_code:
            country_code = country_code.upper()
        super(Location, self).__init__({
            'sublocation'   : value[0],
            'city'          : value[1],
            'province_state': value[2],
            'country_name'  : value[3],
            'country_code'  : country_code,
            'world_region'  : value[5]
            })

    @classmethod
    def from_file(cls, tag, file_value):
        if len(file_value) == 5:
            return cls(file_value + [None])
        return cls(file_value)

    def to_iptc(self):
        return (self.value['sublocation'],
                self.value['city'],
                self.value['province_state'],
                self.value['country_name'],
                self.value['country_code'],
                self.value['world_region'])

    def to_xmp(self):
        return (self.value['sublocation'],
                self.value['city'],
                self.value['province_state'],
                self.value['country_name'],
                self.value['country_code'],
                self.value['world_region'])

    def contains(self, other):
        if not other:
            return True
        for key in self.value:
            if (self.value[key] and other.value[key] and
                    other.value[key] not in self.value[key]):
                return False
        return True

    def merge(self, other, family=None):
        for key in self.value:
            if (self.value[key] and other.value[key] and
                    other.value[key] not in self.value[key]):
                self.value[key] += ' // ' + other.value[key]
        return True


class LensSpec(MetadataDictValue):
    # simple class to store lens "specificaton"
    def __init__(self, value):
        if isinstance(value, six.string_types):
            sep = None
            if ',' in value:
                sep = ','
            value = value.split(sep)
        min_fl, max_fl, min_fl_fn, max_fl_fn = value
        super(LensSpec, self).__init__({
            'min_fl'    : safe_fraction(min_fl),
            'max_fl'    : safe_fraction(max_fl),
            'min_fl_fn' : safe_fraction(min_fl_fn),
            'max_fl_fn' : safe_fraction(max_fl_fn),
            })

    def __str__(self):
        return '{:g} {:g} {:g} {:g}'.format(
            float(self.min_fl),    float(self.max_fl),
            float(self.min_fl_fn), float(self.max_fl_fn))

    def to_exif(self):
        return ' '.join(
            ['{:d}/{:d}'.format(x.numerator, x.denominator) for x in (
                self.min_fl, self.max_fl, self.min_fl_fn, self.max_fl_fn)])

    def contains(self, other):
        if (not other) or (other.value == self.value):
            return True
        # only interested in non-zero values
        for key in self.value:
            if other.value[key] and other.value[key] != self.value[key]:
                return False
        return True


class DateTime(MetadataDictValue):
    # store date and time with "precision" to store how much is valid
    # tz_offset is stored in minutes
    def __init__(self, value):
        date_time, precision, tz_offset = value
        if date_time is None:
            # use a well known 'zero'
            date_time = datetime(1970, 1, 1)
        else:
            date_time = self.truncate_date_time(date_time, precision)
        if precision <= 3:
            tz_offset = None
        super(DateTime, self).__init__({
            'datetime'  : date_time,
            'precision' : precision,
            'tz_offset' : tz_offset,
            })

    @staticmethod
    def truncate_date_time(date_time, precision):
        parts = [date_time.year, date_time.month, date_time.day,
                 date_time.hour, date_time.minute, date_time.second,
                 date_time.microsecond][:precision]
        parts.extend((1, 1, 1)[len(parts):])
        return datetime(*parts)

    @classmethod
    def from_ISO_8601(cls, date_string, time_string, tz_string):
        """Sufficiently general ISO 8601 parser.

        Inputs must be in "basic" format, i.e. no '-' or ':' separators.
        See https://en.wikipedia.org/wiki/ISO_8601

        """
        # parse tz_string
        if tz_string:
            tz_offset = (int(tz_string[1:3]) * 60) + int(tz_string[3:])
            if tz_string[0] == '-':
                tz_offset = -tz_offset
        else:
            tz_offset = None
        if time_string == '000000':
            # assume no time information
            time_string = ''
            tz_offset = None
        datetime_string = date_string + time_string
        precision = min((len(datetime_string) - 2) // 2, 7)
        if precision <= 0:
            return None
        fmt = ''.join(('%Y', '%m', '%d', '%H', '%M', '%S', '.%f')[:precision])
        return cls(
            (datetime.strptime(datetime_string, fmt), precision, tz_offset))

    def to_ISO_8601(self, fmt=('%Y', '-%m', '-%d', 'T%H', ':%M', ':%S', '.%f'),
                    precision=None, time_zone=True):
        if precision is None:
            precision = self.precision
        fmt = ''.join(fmt[:precision])
        datetime_string = self.datetime.strftime(fmt)
        if precision > 3 and time_zone and self.tz_offset is not None:
            # add time zone
            minutes = self.tz_offset
            if minutes >= 0:
                datetime_string += '+'
            else:
                datetime_string += '-'
                minutes = -minutes
            datetime_string += '{:02d}:{:02d}'.format(
                minutes // 60, minutes % 60)
        return datetime_string

    # many quicktime movies use Apple's 1904 timestamp zero point
    qt_offset = (datetime(1970, 1, 1) - datetime(1904, 1, 1)).total_seconds()

    # Do something different with Xmp.video tags
    @classmethod
    def from_file(cls, tag, file_value):
        if MetadataHandler.is_exif_tag(tag):
            return cls.from_exif(file_value)
        if MetadataHandler.is_iptc_tag(tag):
            return cls.from_iptc(file_value)
        if tag.startswith('Xmp.video'):
            time_stamp = int(file_value)
            if time_stamp == 0:
                return None
            # assume date should be in range 1970 to 2034
            if time_stamp > cls.qt_offset:
                time_stamp -= cls.qt_offset
            return cls((datetime.utcfromtimestamp(time_stamp), 6, 0))
        return cls.from_xmp(file_value)

    # Exif datetime is always full resolution and valid. Assume a time
    # of 00:00:00 is a none value though.
    @classmethod
    def from_exif(cls, file_value):
        datetime_string = file_value[0]
        if not datetime_string:
            return None
        # separate date & time and remove separators
        date_string = datetime_string[:10].replace(':', '')
        time_string = datetime_string[11:].replace(':', '')
        # append sub seconds
        if len(file_value) > 1:
            sub_sec_string = file_value[1]
            if sub_sec_string:
                time_string += '.' + sub_sec_string
        result = cls.from_ISO_8601(date_string, time_string, '')
        # set time zone
        if result.precision > 3 and len(file_value) > 2:
            tz_string = file_value[2]
            if tz_string:
                result.tz_offset = int(tz_string)
        return result

    def to_exif(self):
        datetime_string, sep, sub_sec_string = self.to_ISO_8601(
            fmt=('%Y', ':%m', ':%d', ' %H', ':%M', ':%S', '.%f'),
            time_zone=False).partition('.')
        # pad out any missing values
        #                   YYYY mm dd HH MM SS
        datetime_string += '0000:01:01 00:00:00'[len(datetime_string):]
        if self.precision > 3 and self.tz_offset is not None:
            tz_string = str(self.tz_offset)
        else:
            tz_string = ''
        return datetime_string, sub_sec_string, tz_string

    # IPTC date & time should have no separators and be 8 and 11 chars
    # respectively (time includes time zone offset). I suspect the exiv2
    # library is adding separators, but am not sure.

    # The date (and time?) can have missing values represented by 00
    # according to
    # https://de.wikipedia.org/wiki/IPTC-IIM-Standard#IPTC-Felder
    @classmethod
    def from_iptc(cls, file_value):
        date_string, time_string = file_value
        if not date_string:
            return None
        # remove separators (that shouldn't be there)
        date_string = date_string.replace('-', '')
        # remove missing values
        while len(date_string) > 4 and date_string[-2:] == '00':
            date_string = date_string[:-2]
        if date_string == '0000':
            return None
        # ignore time if date is not full precision
        if len(date_string) < 8:
            time_string = ''
        if time_string:
            # remove separators (that shouldn't be there)
            time_string = time_string.replace(':', '')
            # split off time zone
            tz_string = time_string[6:]
            time_string = time_string[:6]
        else:
            tz_string = ''
            time_string = ''
        return cls.from_ISO_8601(date_string, time_string, tz_string)

    def to_iptc(self):
        if self.precision <= 3:
            date_string = self.to_ISO_8601()
            #               YYYY mm dd
            date_string += '0000-00-00'[len(date_string):]
            time_string = None
        else:
            datetime_string = self.to_ISO_8601(precision=6)
            date_string = datetime_string[:10]
            time_string = datetime_string[11:]
        return date_string, time_string

    # XMP uses extended ISO 8601, but the time cannot be hours only. See
    # p75 of
    # https://partners.adobe.com/public/developer/en/xmp/sdk/XMPspecification.pdf
    # According to p71, when converting Exif values with no time zone,
    # local time zone should be assumed. However, the MWG guidelines say
    # this must not be assumed to be the time zone where the photo is
    # processed. It also says the XMP standard has been revised to make
    # time zone information optional.
    @classmethod
    def from_xmp(cls, file_value):
        date_string, sep, time_string = file_value.partition('T')
        if len(time_string) > 6 and time_string[-6] in ('+', '-'):
            tz_string = time_string[-6:]
            time_string = time_string[:-6]
        elif len(time_string) > 1 and time_string[-1] == 'Z':
            tz_string = '+00:00'
            time_string = time_string[:-1]
        else:
            tz_string = ''
        return cls.from_ISO_8601(
            date_string.replace('-', ''), time_string.replace(':', ''),
            tz_string.replace(':', ''))

    def to_xmp(self):
        precision = self.precision
        if precision == 4:
            precision = 5
        return self.to_ISO_8601(precision=precision)

    def __str__(self):
        return self.to_ISO_8601()

    def contains(self, other):
        if (not other) or (other.value == self.value):
            return True
        if other.datetime != self.datetime:
            return False
        if self.precision < 7 and other.precision < self.precision:
            return False
        if other.tz_offset in (None, self.tz_offset):
            return True
        return False

    def merge(self, other, family=None):
        result = False
        # work out apparent precisions by stripping zeroes
        self_precision = self.precision
        while self_precision > 1 and self.truncate_date_time(
                        self.datetime, self_precision - 1) == self.datetime:
            self_precision -= 1
        other_precision = other.precision
        while other_precision > 1 and self.truncate_date_time(
                        other.datetime, other_precision - 1) == other.datetime:
            other_precision -= 1
        # if datetime values differ, choose the one with more apparent precision
        if other.datetime != self.datetime and other_precision > self_precision:
            self.datetime = other.datetime
            self.precision = other.precision
            self.tz_offset = other.tz_offset
            return True
        # some formats default to a higher precision than wanted
        if (other.datetime == self.datetime and
                    self.precision < 7 and other.precision < self.precision):
            self.precision = other.precision
            result = True
        # don't trust IPTC time zone and Exif time zone is quantised to
        # whole hours, unlike Xmp
        if other.tz_offset is not None and family != 'Iptc':
            if self.tz_offset is None:
                self.tz_offset = other.tz_offset
                result = True
            elif self.tz_offset != other.tz_offset and family == 'Xmp':
                self.tz_offset = other.tz_offset
                result = True
        return result


class MultiString(MetadataValue):
    def __init__(self, value):
        if isinstance(value, six.string_types):
            value = value.split(';')
        value = list(filter(bool, [x.strip() for x in value]))
        super(MultiString, self).__init__(value)

    def to_exif(self):
        return ';'.join(self.value)

    def __str__(self):
        return '; '.join(self.value)

    def contains(self, other):
        return (not other) or (not bool(
            [x for x in other.value if x not in self.value]))

    def merge(self, other, family=None):
        self.value += other.value
        return True


class String(MetadataValue):
    def __init__(self, value):
        if isinstance(value, list):
            value = value[0]
        super(String, self).__init__(value)

    @classmethod
    def from_file(cls, tag, file_value):
        value = six.text_type(file_value).strip()
        if not value:
            return None
        return cls(value)

    def contains(self, other):
        return (not other) or (other.value in self.value)

    def merge(self, other, family=None):
        self.value += ' // ' + other.value
        return True


class CharacterSet(String):
    known_encodings = {
        'ascii'   : '\x1b(B',
        'latin_1' : '\x1b/A',
        'latin1'  : '\x1b.A',
        'utf_8'   : '\x1b%G',
        }

    @classmethod
    def from_file(cls, tag, file_value):
        for charset, encoding in cls.known_encodings.items():
            if encoding == file_value:
                return cls(charset)
        logger.warning('Unknown character encoding "%s"', repr(file_value))
        return None

    def to_iptc(self):
        return self.known_encodings[self.value]


class Software(String):
    @classmethod
    def from_file(cls, tag, file_value):
        if isinstance(file_value, tuple):
            program, version = file_value
            if not program:
                return None
            if version:
                program += ' v' + version
            return cls(program)
        return cls(file_value)

    def to_iptc(self):
        return self.value.split(' v')


class Int(MetadataValue):
    def __init__(self, value):
        super(Int, self).__init__(int(value))

    def to_exif(self):
        return '{:d}'.format(self.value)

    def __nonzero__(self):
        return self.value is not None

    def __str__(self):
        return '{:d}'.format(self.value)


class Aperture(MetadataValue):
    def __init__(self, value):
        super(Aperture, self).__init__(Fraction(value))

    def to_exif(self):
        return '{:d}/{:d}'.format(self.value.numerator, self.value.denominator)

    def __nonzero__(self):
        return self.value is not None

    def __str__(self):
        return '{:g}'.format(float(self.value))

    def contains(self, other):
        return (not other) or ((min(other.value, self.value) /
                                max(other.value, self.value)) > 0.95)


# maximum length of Iptc data
_max_bytes = {
    'Iptc.Application2.Byline'           :   32,
    'Iptc.Application2.Caption'          : 2000,
    'Iptc.Application2.City'             :   32,
    'Iptc.Application2.Copyright'        :  128,
    'Iptc.Application2.CountryCode'      :    3,
    'Iptc.Application2.CountryName'      :   64,
    'Iptc.Application2.Headline'         :  256,
    'Iptc.Application2.Keywords'         :   64,
    'Iptc.Application2.ObjectName'       :   64,
    'Iptc.Application2.Program'          :   32,
    'Iptc.Application2.ProgramVersion'   :   10,
    'Iptc.Application2.ProvinceState'    :   32,
    'Iptc.Application2.SubLocation'      :   32,
    'Iptc.Envelope.CharacterSet'         :   32,
    }

# extra Xmp namespaces we may need
_extra_ns = {
    'Iptc4xmpExt': 'http://iptc.org/std/Iptc4xmpExt/2008-02-29/',
    }

class MetadataHandler(GExiv2.Metadata):
    def __init__(self, path, is_sidecar=False):
        super(MetadataHandler, self).__init__()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._path = path
        self._is_sidecar = is_sidecar
        # read metadata from file
        self.open_path(self._path)
        # make list of possible character encodings
        self._encodings = []
        for name in ('utf_8', 'latin_1'):
            self._encodings.append(codecs.lookup(name).name)
        char_set = locale.getdefaultlocale()[1]
        if char_set:
            try:
                name = codecs.lookup(char_set).name
                if name not in self._encodings:
                    self._encodings.append(name)
            except LookupError:
                pass
        # convert IPTC data to UTF-8
        if self._is_sidecar or not self.has_iptc():
            return
        current_encoding = self.get_value(
            CharacterSet, 'Iptc.Envelope.CharacterSet')
        if current_encoding:
            if current_encoding.value == 'utf_8':
                return
            try:
                name = codecs.lookup(current_encoding.value).name
                if name not in self._encodings:
                    self._encodings.insert(0, name)
            except LookupError:
                pass
        for tag in self.get_iptc_tags():
            try:
                value_list = self.get_multiple(tag)
                self.set_multiple(tag, value_list)
            except Exception as ex:
                self._logger.exception(ex)

    def _decode_string(self, value):
        if not value:
            return value
        for encoding in self._encodings:
            try:
                return value.decode(encoding)
            except UnicodeDecodeError:
                continue
        return value.decode('utf_8', 'replace')

    def get_value(self, data_type, tag):
        # exiv2 pretends XMP files have non-xmp tags
        if self._is_sidecar and not self.is_xmp_tag(tag):
            return None
        # get string or multiple strings
        if tag in ('Iptc.Application2.Byline', 'Iptc.Application2.Keywords',
                   'Xmp.dc.creator', 'Xmp.dc.subject'):
            file_value = self.get_multiple(tag)
        elif tag in ('Xmp.dc.description', 'Xmp.dc.rights', 'Xmp.dc.title',
                     'Xmp.tiff.Copyright'):
            file_value = self.get_multiple(tag)
            if file_value:
                file_value = file_value[0]
        else:
            file_value = self.get_string(tag)
        if file_value is None or not any(file_value):
            return None
        # manipulate some tags' data
        if tag in ('Exif.Image.ApertureValue',
                   'Exif.Photo.ApertureValue'):
            # convert APEX aperture value
            file_value = 2.0 ** (Fraction(file_value) / 2.0)
        elif tag in ('Exif.Image.XPAuthor', 'Exif.Image.XPComment',
                     'Exif.Image.XPKeywords', 'Exif.Image.XPSubject',
                     'Exif.Image.XPTitle'):
            # decode UCS2 string
            file_value = bytearray(map(int, file_value.split()))
            file_value = file_value.decode('utf_16').strip('\x00')
        elif tag == 'Exif.Image.TimeZoneOffset':
            # convert hours to minutes
            file_value = str(int(file_value) * 60)
        elif tag == 'Exif.CanonCs.Lens':
            long_focal, short_focal, focal_units = file_value.split()
            file_value = ('{}/{}'.format(short_focal, focal_units),
                          '{}/{}'.format(long_focal, focal_units),
                          0, 0)
        # convert to Photini data type
        return data_type.from_file(tag, file_value)

    def clear_value(self, tag):
        # exiv2 pretends XMP files have non-xmp tags
        if self._is_sidecar and not self.is_xmp_tag(tag):
            return
        if isinstance(tag, tuple):
            for sub_tag in tag:
                self.clear_value(sub_tag)
            return
        self.clear_tag(tag)

    def set_value(self, tag, value):
        # exiv2 pretends XMP files have non-xmp tags
        if self._is_sidecar and not self.is_xmp_tag(tag):
            return
        if not value:
            self.clear_value(tag)
            return
        # convert from Photini data type to string or multiple string
        if self.is_exif_tag(tag):
            file_value = value.to_exif()
        elif self.is_iptc_tag(tag):
            file_value = value.to_iptc()
        else:
            file_value = value.to_xmp()
        # manipulate some tags' data
        if tag == 'Exif.Image.TimeZoneOffset':
            # convert minutes to hours
            file_value = str(int(round(float(file_value) / 60.0)))
        # write to file
        if tag in ('Iptc.Application2.Byline', 'Iptc.Application2.Keywords',
                   'Xmp.dc.creator', 'Xmp.dc.subject'):
            self.set_multiple(tag, file_value)
        else:
            self.set_string(tag, file_value)

    def get_string(self, tag):
        if isinstance(tag, tuple):
            return list(map(self.get_string, tag))
        try:
            result = self.get_tag_string(tag)
            if six.PY2:
                result = self._decode_string(result)
        except UnicodeDecodeError as ex:
            self._logger.error(str(ex))
            return ''
        return result

    def get_multiple(self, tag):
        if isinstance(tag, tuple):
            return list(map(self.get_multiple, tag))
        try:
            result = self.get_tag_multiple(tag)
            if six.PY2:
                result = list(map(self._decode_string, result))
        except UnicodeDecodeError as ex:
            self._logger.error(str(ex))
            return []
        return result

    def set_string(self, tag, value):
        if isinstance(tag, tuple):
            for sub_tag, sub_value in zip(tag, value):
                self.set_string(sub_tag, sub_value)
            return
        if not value:
            self.clear_value(tag)
            return
        if self.is_iptc_tag(tag) and tag in _max_bytes:
            value = value.encode('utf_8')[:_max_bytes[tag]]
            if not six.PY2:
                value = value.decode('utf_8', errors='ignore')
        elif six.PY2:
            value = value.encode('utf_8')
        if self.is_xmp_tag(tag) and '/' in tag:
            # create XMP structure/container
            container, subtag = tag.split('/')
            bag = container.partition('[')[0]
            ns_prefix = subtag.partition(':')[0]
            no_bag = True
            ns_defined = ns_prefix not in _extra_ns
            for t in self.get_xmp_tags():
                if t.startswith(bag):
                    # file already has container
                    no_bag = False
                if ns_prefix in t:
                    # file has correct namespace defined
                    ns_defined = True
            if no_bag:
                # create empty container
                if '[' in container:
                    self.set_xmp_tag_struct(bag, GExiv2.StructureType.ALT)
                else:
                    self.set_xmp_tag_struct(bag, GExiv2.StructureType.SEQ)
            if not ns_defined:
                # create some XMP data with the correct namespace
                data = '''<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 4.4.0-Exiv2">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description
        xmlns:{}="{}">
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>'''.format(ns_prefix, _extra_ns[ns_prefix])
                if six.PY2:
                    data = data.decode('utf-8')
                # open the data to register the correct namespace
                md = GExiv2.Metadata()
                md.open_buf(data.encode('utf-8'))
        self.set_tag_string(tag, value)

    def set_multiple(self, tag, value):
        if isinstance(tag, tuple):
            for sub_tag, sub_value in zip(tag, value):
                self.set_multiple(sub_tag, sub_value)
            return
        if not value:
            self.clear_value(tag)
            return
        if self.is_iptc_tag(tag) and tag in _max_bytes:
            value = [x.encode('utf_8')[:_max_bytes[tag]] for x in value]
            if not six.PY2:
                value = [x.decode('utf_8') for x in value]
        elif six.PY2:
            value = [x.encode('utf_8') for x in value]
        self.set_tag_multiple(tag, value)

    @staticmethod
    def is_exif_tag(tag):
        if isinstance(tag, tuple):
            tag = tag[0]
        return GExiv2.Metadata.is_exif_tag(tag)

    @staticmethod
    def is_iptc_tag(tag):
        if isinstance(tag, tuple):
            tag = tag[0]
        return GExiv2.Metadata.is_iptc_tag(tag)

    @staticmethod
    def is_xmp_tag(tag):
        if isinstance(tag, tuple):
            tag = tag[0]
        return GExiv2.Metadata.is_xmp_tag(tag)

    def save(self, file_times):
        try:
            self.save_file(self._path)
            if file_times:
                os.utime(self._path, file_times)
        except Exception as ex:
            self._logger.exception(ex)
            return False
        return True

    def clone(self, other):
        # copy from other to self
        for tag in other.get_exif_tags():
            self.set_string(tag, other.get_string(tag))
        for tag in other.get_iptc_tags():
            self.set_multiple(tag, other.get_multiple(tag))
        for tag in other.get_xmp_tags():
            if not self._is_sidecar and tag.startswith('Xmp.xmp.Thumbnails'):
                # don't try and fit a thumbnail in 64k Xmp segment
                continue
            if self.get_tag_type(tag) == 'XmpText':
                self.set_string(tag, other.get_string(tag))
            else:
                self.set_multiple(tag, other.get_multiple(tag))

    def get_all_tags(self):
        return self.get_exif_tags() + self.get_iptc_tags() + self.get_xmp_tags()

    def get_xmp_thumbnail(self):
        widths = []
        tags = []
        for tag in self.get_xmp_tags():
            # not everyone uses the 'xmpGImg' prefix
            if tag.startswith('Xmp.xmp.Thumbnails') and tag.endswith('width'):
                widths.append(int(self.get_string(tag)))
                tags.append(tag)
        if not widths:
            return None
        best = widths.index(max(widths))
        tag = tags[best].replace('width', 'image')
        data = self.get_string(tag)
        if not six.PY2:
            data = bytes(data, 'ASCII')
        return codecs.decode(data, 'base64_codec')

    def set_xmp_thumbnail(self, data, fmt, w, h):
        data = codecs.encode(data, 'base64_codec')
        self.set_string('Xmp.xmp.Thumbnails', None)
        self.set_string('Xmp.xmp.Thumbnails[1]/xmpGImg:format', fmt)
        self.set_string('Xmp.xmp.Thumbnails[1]/xmpGImg:width', str(w))
        self.set_string('Xmp.xmp.Thumbnails[1]/xmpGImg:height', str(h))
        self.set_string('Xmp.xmp.Thumbnails[1]/xmpGImg:image', data)


class Metadata(object):
    # type of each Photini data field's data
    _data_type = {
        'aperture'       : Aperture,
        'camera_model'   : String,
        'character_set'  : CharacterSet,
        'copyright'      : String,
        'creator'        : MultiString,
        'date_digitised' : DateTime,
        'date_modified'  : DateTime,
        'date_taken'     : DateTime,
        'description'    : String,
        'focal_length'   : FocalLength,
        'keywords'       : MultiString,
        'latlong'        : LatLon,
        'lens_make'      : String,
        'lens_model'     : String,
        'lens_serial'    : String,
        'lens_spec'      : LensSpec,
        'location_shown' : Location,
        'location_taken' : Location,
        'orientation'    : Int,
        'software'       : Software,
        'timezone'       : Int,
        'title'          : String,
        }
    # mapping of preferred tags to Photini data fields
    _primary_tags = {
        'aperture'       : (('Exif', 'Exif.Photo.FNumber'),),
        'camera_model'   : (('Exif', 'Exif.Image.Model'),),
        'character_set'  : (('Iptc', 'Iptc.Envelope.CharacterSet'),),
        'copyright'      : (('Exif', 'Exif.Image.Copyright'),
                            ('Xmp',  'Xmp.dc.rights'),
                            ('Iptc', 'Iptc.Application2.Copyright')),
        'creator'        : (('Exif', 'Exif.Image.Artist'),
                            ('Xmp',  'Xmp.dc.creator'),
                            ('Iptc', 'Iptc.Application2.Byline')),
        'date_digitised' : (('Exif', ('Exif.Photo.DateTimeDigitized',
                                      'Exif.Photo.SubSecTimeDigitized')),
                            ('Xmp',  'Xmp.xmp.CreateDate'),
                            ('Iptc', ('Iptc.Application2.DigitizationDate',
                                      'Iptc.Application2.DigitizationTime'))),
        'date_modified'  : (('Exif', ('Exif.Image.DateTime',
                                      'Exif.Photo.SubSecTime')),
                            ('Xmp',  'Xmp.xmp.ModifyDate')),
        'date_taken'     : (('Exif', ('Exif.Photo.DateTimeOriginal',
                                      'Exif.Photo.SubSecTimeOriginal',
                                      'Exif.Image.TimeZoneOffset')),
                            ('Xmp',  'Xmp.photoshop.DateCreated'),
                            ('Iptc', ('Iptc.Application2.DateCreated',
                                      'Iptc.Application2.TimeCreated'))),
        'description'    : (('Exif', 'Exif.Image.ImageDescription'),
                            ('Xmp',  'Xmp.dc.description'),
                            ('Iptc', 'Iptc.Application2.Caption')),
        'focal_length'   : (('Exif', ('Exif.Photo.FocalLength',
                                      'Exif.Photo.FocalLengthIn35mmFilm')),),
        'keywords'       : (('Xmp',  'Xmp.dc.subject'),
                            ('Iptc', 'Iptc.Application2.Keywords')),
        'latlong'        : (('Exif', ('Exif.GPSInfo.GPSLatitude',
                                      'Exif.GPSInfo.GPSLatitudeRef',
                                      'Exif.GPSInfo.GPSLongitude',
                                      'Exif.GPSInfo.GPSLongitudeRef')),),
        'lens_make'      : (('Exif', 'Exif.Photo.LensMake'),),
        'lens_model'     : (('Exif', 'Exif.Photo.LensModel'),),
        'lens_serial'    : (('Exif', 'Exif.Photo.LensSerialNumber'),),
        'lens_spec'      : (('Exif', 'Exif.Photo.LensSpecification'),),
        'location_shown' : (
            ('Xmp', ('Xmp.iptcExt.LocationShown[1]/Iptc4xmpExt:Sublocation',
                     'Xmp.iptcExt.LocationShown[1]/Iptc4xmpExt:City',
                     'Xmp.iptcExt.LocationShown[1]/Iptc4xmpExt:ProvinceState',
                     'Xmp.iptcExt.LocationShown[1]/Iptc4xmpExt:CountryName',
                     'Xmp.iptcExt.LocationShown[1]/Iptc4xmpExt:CountryCode',
                     'Xmp.iptcExt.LocationShown[1]/Iptc4xmpExt:WorldRegion')),),
        'location_taken' : (
            ('Xmp', ('Xmp.iptcExt.LocationCreated[1]/Iptc4xmpExt:Sublocation',
                     'Xmp.iptcExt.LocationCreated[1]/Iptc4xmpExt:City',
                     'Xmp.iptcExt.LocationCreated[1]/Iptc4xmpExt:ProvinceState',
                     'Xmp.iptcExt.LocationCreated[1]/Iptc4xmpExt:CountryName',
                     'Xmp.iptcExt.LocationCreated[1]/Iptc4xmpExt:CountryCode',
                     'Xmp.iptcExt.LocationCreated[1]/Iptc4xmpExt:WorldRegion')),
            ('Xmp', ('Xmp.iptc.Location',
                     'Xmp.photoshop.City',
                     'Xmp.photoshop.State',
                     'Xmp.photoshop.Country',
                     'Xmp.iptc.CountryCode')),
            ('Iptc', ('Iptc.Application2.SubLocation',
                      'Iptc.Application2.City',
                      'Iptc.Application2.ProvinceState',
                      'Iptc.Application2.CountryName',
                      'Iptc.Application2.CountryCode'))),
        'orientation'    : (('Exif', 'Exif.Image.Orientation'),),
        'software'       : (('Exif', 'Exif.Image.ProcessingSoftware'),
                            ('Iptc', ('Iptc.Application2.Program',
                                      'Iptc.Application2.ProgramVersion'))),
        'timezone'       : (),
        'title'          : (('Xmp',  'Xmp.dc.title'),
                            ('Iptc', 'Iptc.Application2.ObjectName')),
        }
    # mapping of duplicate tags to Photini data fields
    # data in these is merged in when data is read
    # they get deleted when data is written
    _secondary_tags = {
        'aperture'       : (('Exif', 'Exif.Image.FNumber'),
                            ('Exif', 'Exif.Image.ApertureValue'),
                            ('Exif', 'Exif.Photo.ApertureValue'),
                            ('Xmp', 'Xmp.exif.FNumber'),
                            ('Xmp', 'Xmp.exif.ApertureValue')),
        'copyright'      : (('Xmp', 'Xmp.tiff.Copyright'),),
        'creator'        : (('Exif', 'Exif.Image.XPAuthor'),
                            ('Xmp', 'Xmp.tiff.Artist')),
        'date_digitised' : (('Xmp', 'Xmp.exif.DateTimeDigitized'),),
        'date_modified'  : (('Xmp', 'Xmp.tiff.DateTime'),),
        'date_taken'     : (('Exif', ('Exif.Image.DateTimeOriginal',)),
                            ('Xmp', 'Xmp.exif.DateTimeOriginal')),
        'description'    : (('Exif', 'Exif.Image.XPComment'),
                            ('Exif', 'Exif.Image.XPSubject'),
                            ('Xmp', 'Xmp.tiff.ImageDescription')),
        'focal_length'   : (('Exif', ('Exif.Image.FocalLength',
                                      'Exif.Photo.FocalLengthIn35mmFilm')),
                            ('Xmp', ('Xmp.exif.FocalLength',
                                     'Xmp.exif.FocalLengthIn35mmFilm'))),
        'keywords'       : (('Exif', 'Exif.Image.XPKeywords'),),
        'latlong'        : (('Xmp', ('Xmp.exif.GPSLatitude',
                                     'Xmp.exif.GPSLongitude')),),
        'lens_model'     : (('Exif', 'Exif.Canon.LensModel'),
                            ('Exif', 'Exif.OlympusEq.LensModel'),),
        'lens_serial'    : (('Exif', 'Exif.OlympusEq.LensSerialNumber'),),
        'lens_spec'      : (('Exif', 'Exif.Image.LensInfo'),
                            ('Exif', 'Exif.CanonCs.Lens'),
                            ('Exif', 'Exif.Nikon3.Lens')),
        'orientation'    : (('Xmp', 'Xmp.tiff.Orientation'),),
        'title'          : (('Exif', 'Exif.Image.XPTitle'),
                            ('Iptc', 'Iptc.Application2.Headline')),
        }
    # tags that are read and merged but not deleted
    _read_tags = {
        'camera_model'   : (('Exif', 'Exif.Image.UniqueCameraModel'),
                            ('Xmp', 'Xmp.video.Model')),
        'date_digitised' : (('Xmp', 'Xmp.video.DateUTC'),),
        'date_modified'  : (('Xmp', 'Xmp.video.ModificationDate'),),
        'date_taken'     : (('Xmp', 'Xmp.video.DateUTC'),),
        'latlong'        : (('Xmp', 'Xmp.video.GPSCoordinates'),),
        'timezone'       : (('Exif', 'Exif.Image.TimeZoneOffset'),
                            ('Exif', 'Exif.NikonWt.Timezone')),
        }
    # tags that aren't read but are cleared when Photini data is written
    _clear_tags = {
        'lens_model'     : ('Exif.CanonCs.LensType',),
        'lens_spec'      : ('Exif.CanonCs.ShortFocal',
                            'Exif.CanonCs.MaxAperture',
                            'Exif.CanonCs.MinAperture'),
        }
    def __init__(self, path, new_status=None):
        super(Metadata, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self._new_status = new_status
        # create metadata handlers for image file and/or sidecar
        self._path = path
        self._sc_path = self._find_side_car(path)
        self._sc = None
        if self._sc_path:
            try:
                self._sc = MetadataHandler(self._sc_path, is_sidecar=True)
            except Exception as ex:
                self.logger.exception(ex)
        self._if = None
        try:
            self._if = MetadataHandler(path)
        except GLib.Error:
            # expected if unrecognised file format
            pass
        except Exception as ex:
            self.logger.exception(ex)
        if not self._if and not self._sc:
            self.create_side_car()
        self._unsaved = False

    def _find_side_car(self, path):
        for base in (os.path.splitext(path)[0], path):
            for ext in ('.xmp', '.XMP'):
                result = base + ext
                if os.path.exists(result):
                    return result
        return None

    def create_side_car(self):
        self._sc_path = self._path + '.xmp'
        with open(self._sc_path, 'w') as of:
            of.write('''<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 4.4.0-Exiv2">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:xmp="http://ns.adobe.com/xap/1.0/"
   xmp:CreatorTool="{}"/>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>'''.format('Photini editor v' + __version__))
        try:
            self._sc = MetadataHandler(self._sc_path, is_sidecar=True)
        except Exception as ex:
            self.logger.exception(ex)
        if self._sc and self._if:
            self._sc.clone(self._if)

    def save(self, if_mode, sc_mode, force_iptc, file_times):
        if not self._unsaved:
            return
        self.software = 'Photini editor v' + __version__
        self.character_set = 'utf_8'
        save_iptc = force_iptc or self.has_iptc()
        for name in self._primary_tags:
            value = getattr(self, name)
            # write data to primary tags
            for family, tag in self._primary_tags[name]:
                if save_iptc or family != 'Iptc':
                    self.set_value(tag, value)
            # delete secondary tags
            if name in self._secondary_tags:
                for family, tag in self._secondary_tags[name]:
                    self.set_value(tag, None)
            # clear duplicated but unreadable data
            if name in self._clear_tags:
                for tag in self._clear_tags[name]:
                    self.set_value(tag, None)
        if self._if and sc_mode == 'delete' and self._sc:
            self._if.clone(self._sc)
        OK = False
        if self._if and if_mode:
            OK = self._if.save(file_times)
            if OK:
                # check that data really was saved
                saved_tags = MetadataHandler(self._path).get_all_tags()
                for tag in self._if.get_all_tags():
                    if tag not in saved_tags:
                        self.logger.warning('tag not saved: %s', tag)
                        OK = False
        if sc_mode == 'delete' and self._sc and OK:
            os.unlink(self._sc_path)
            self._sc = None
        if sc_mode in ('auto', 'delete') and not self._sc and not OK:
            self.create_side_car()
        if sc_mode == 'always' and not self._sc:
            self.create_side_car()
        if self._sc:
            OK = self._sc.save(file_times)
        self._set_unsaved(not OK)

    # getters: use sidecar if tag is present, otherwise use image file
    def get_value(self, data_type, tag):
        result = None
        if self._sc:
            result = self._sc.get_value(data_type, tag)
        if self._if and not result:
            result = self._if.get_value(data_type, tag)
        return result

    def has_iptc(self):
        if self._sc and self._sc.has_iptc():
            return True
        if self._if and self._if.has_iptc():
            return True
        return False

    def get_thumbnail(self):
        for source in self._sc, self._if:
            if source:
                # try Xmp first
                thumb = source.get_xmp_thumbnail()
                if thumb:
                    return thumb
                # then try Exif
                thumb = source.get_exif_thumbnail()
                if using_pgi:
                    # get_exif_thumbnail returns (OK, data) tuple
                    thumb = thumb[thumb[0]]
                if thumb:
                    return bytearray(thumb)
        return None

    def get_mime_type(self):
        if self._if:
            return self._if.get_mime_type()
        return None

    # setters: set in both sidecar and image file
    def set_value(self, tag, value):
        if self._sc:
            self._sc.set_value(tag, value)
        if self._if:
            self._if.set_value(tag, value)

    def copy(self, other):
        # copy from other to self, sidecar over-rides image
        if self._sc:
            if other._if:
                self._sc.clone(other._if)
            if other._sc:
                self._sc.clone(other._sc)
        if self._if:
            if other._if:
                self._if.clone(other._if)
            if other._sc:
                self._if.clone(other._sc)
        self._set_unsaved(True)

    def set_thumbnail(self, thumb, fmt, w, h):
        if self._sc:
            self._sc.set_xmp_thumbnail(thumb, fmt, w, h)
        if self._if:
            self._if.set_exif_thumbnail_from_buffer(thumb)
        self._set_unsaved(True)

    def __getattr__(self, name):
        if name not in self._primary_tags:
            return super(Metadata, self).__getattr__(name)
        # make list of tags to read
        tag_list = list(self._primary_tags[name])
        if name in self._secondary_tags:
            tag_list.extend(self._secondary_tags[name])
        if name in self._read_tags:
            tag_list.extend(self._read_tags[name])
        # read data, merging in any conflicting values
        value = {'Exif': None, 'Iptc': None, 'Xmp': None}
        used_tag = {'Exif': None, 'Iptc': None, 'Xmp': None}
        for family, tag in tag_list:
            try:
                new_value = self.get_value(self._data_type[name], tag)
            except Exception as ex:
                self.logger.exception(ex)
                continue
            if not new_value:
                continue
            elif not value[family]:
                value[family] = new_value
                used_tag[family] = tag
            elif value[family].contains(new_value):
                continue
            elif value[family].merge(new_value):
                self.logger.info(
                    '%s: merged %s into %s',
                    os.path.basename(self._path), tag, used_tag[family])
            else:
                self.logger.warning(
                    '%s: using %s value "%s", ignoring %s value "%s"',
                    os.path.basename(self._path), used_tag[family],
                    str(value[family]), tag, str(new_value))
        # choose preferred family
        if value['Exif']:
            preference = 'Exif'
        elif value['Xmp']:
            preference = 'Xmp'
        else:
            preference = 'Iptc'
        # merge in non-matching data so user can review it
        result = value[preference]
        if result:
            for family in ('Exif', 'Xmp', 'Iptc'):
                other = value[family]
                if result.contains(other):
                    continue
                elif result.merge(other, family):
                    self.logger.info(
                        '%s: merged %s data into %s',
                        os.path.basename(self._path),
                        used_tag[family], used_tag[preference])
                else:
                    self.logger.warning(
                        '%s: using %s value "%s", ignoring %s value "%s"',
                        os.path.basename(self._path), used_tag[preference],
                        str(result), used_tag[family], str(other))
        # merge in camera timezone if needed
        if (result and name.startswith('date_') and
                            result.tz_offset is None and self.timezone):
            result.tz_offset = self.timezone.value
            self.logger.info(
                '%s: merged camera timezone offset into %s',
                os.path.basename(self._path), used_tag[preference])
        # add value to object attributes so __getattr__ doesn't get
        # called again
        super(Metadata, self).__setattr__(name, result)
        return result

    def __setattr__(self, name, value):
        if name not in self._primary_tags:
            return super(Metadata, self).__setattr__(name, value)
        if value in (None, '', [], {}):
            value = None
        elif not isinstance(value, self._data_type[name]):
            value = self._data_type[name](value)
            if not value:
                value = None
        if getattr(self, name) == value:
            return
        super(Metadata, self).__setattr__(name, value)
        self._set_unsaved(True)

    def _set_unsaved(self, status):
        self._unsaved = status
        if self._new_status:
            self._new_status(self._unsaved)

    def changed(self):
        return self._unsaved
