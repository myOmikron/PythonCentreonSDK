"""
This program is a library to communicate with the Centreon REST API

Copyright (C) 2019 Niklas Pfister, contact@omikron.pw

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
import enum


class TimePeriod:
    """This class represents a time period

    :param id_unique: ID of the time period
    :type id_unique: int
    :param name: Name of the time period
    :type name: str
    :param alias: Alias of the time period
    :type alias: str
    :param sunday: Period on sunday
    :type sunday: str
    :param monday: Period on monday
    :type monday: str
    :param tuesday: Period on tuesday
    :type tuesday: str
    :param wednesday: Period on wednesday
    :type wednesday: str
    :param thursday: Period on thursday
    :type thursday: str
    :param friday: Period on friday
    :type friday: str
    :param saturday: Period on saturday
    :type saturday: str
    """
    def __init__(self, id_unique, name, alias, sunday, monday, tuesday, wednesday, thursday, friday, saturday):
        self.id_unique = id_unique
        self.name = name
        self.alias = alias
        self.sunday = sunday
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday


class TimePeriodParam(enum.Enum):
    """This class represents a parameter for a time period"""
    NAME = "name"
    """Name of the time period (str)"""
    ALIAS = "alias"
    """Alias of the time period (str)"""
    SUNDAY = "sunday"
    """Time period definition for sunday (str)"""
    MONDAY = "monday"
    """Time period definition for monday (str)"""
    TUESDAY = "tuesday"
    """Time period definition for tuesday (str)"""
    WEDNESDAY = "wednesday"
    """Time period definition for wednesday (str)"""
    THURSDAY = "thursday"
    """Time period definition for thursday (str)"""
    FRIDAY = "friday"
    """Time period definition for friday (str)"""
    SATURDAY = "saturday"
    """Time period definition for saturday (str)"""
    INCLUDE = "include"
    """This parameter is used to include other time periods (str, list of str)"""
    EXCLUDE = "exclude"
    """This parameter is used to exclude other time periods (str, list of str)"""


class TimePeriodException:
    """This class represents a exception

    :param days: Days to exclude
    :type days: str
    :param timerange: Timerange to exclude
    :type timerange: str
    """
    def __init__(self, days, timerange):
        self.days = days
        self.timerange = timerange
