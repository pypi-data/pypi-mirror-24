"""
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from .context import parse_alignment


def test_parse_alignment():
    # init
    options = {}
    # check alignment
    assert parse_alignment('LRC', 4) == [
        'AlignLeft',
        'AlignRight',
        'AlignCenter',
        'AlignDefault'
    ]
    # check alignment too long
    assert parse_alignment('LRCDLRCDLRCDLRCDLRCDLRCD', 4) == [
        'AlignLeft',
        'AlignRight',
        'AlignCenter',
        'AlignDefault'
    ]
    # check invalid
    assert parse_alignment('abcd', 4) is None
    # check wrong type
    assert parse_alignment(1, 1) is None
    return
