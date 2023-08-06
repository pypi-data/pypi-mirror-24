# Copyright (c) 2016 Cyso < development [at] cyso . com >
#
# This file is part of omniconf, a.k.a. python-omniconf .
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see
# <http://www.gnu.org/licenses/>.

from omniconf.types import separator_sequence
import nose.tools


SEPARATOR_SEQUENCES = [
    ("", ",", [""]),
    ("a", ",", ["a"]),
    ("a,b,c", ",", ["a", "b", "c"]),
    ("foo,bar;baz;", ";", ["foo,bar", "baz", ""]),
    (["foo", "bar"], ",", ["foo", "bar"]),
    ([], ",", [])
]


def _test_separator_sequence(_in, _sep, _out):
    seq = separator_sequence(_sep)(_in)
    nose.tools.assert_sequence_equal(seq, _out)
    nose.tools.assert_equal(seq.__str__(), _out.__str__())


def test_separator_sequence():
    for _in, _sep, _out in SEPARATOR_SEQUENCES:
        yield _test_separator_sequence, _in, _sep, _out
