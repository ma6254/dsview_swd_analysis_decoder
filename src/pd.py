##
# This file is part of the libsigrokdecode project.
##
# Copyright (C) 2011-2014 Uwe Hermann <uwe@hermann-uwe.de>
# Copyright (C) 2019 DreamSourceLab <support@dreamsourcelab.com>
##
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
##
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
##
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
##

import sigrokdecode as srd
from common.srdhelper import bitpack
from math import floor, ceil

'''
OUTPUT_PYTHON format:

Packet:
[<ptype>, <rxtx>, <pdata>]

This is the list of <ptype>s and their respective <pdata> values:
 - 'STARTBIT': The data is the (integer) value of the start bit (0/1).
 - 'DATA': This is always a tuple containing two items:
   - 1st item: the (integer) value of the UART data. Valid values
     range from 0 to 511 (as the data can be up to 9 bits in size).
   - 2nd item: the list of individual data bits and their ss/es numbers.
 - 'PARITYBIT': The data is the (integer) value of the parity bit (0/1).
 - 'STOPBIT': The data is the (integer) value of the stop bit (0 or 1).
 - 'INVALID STARTBIT': The data is the (integer) value of the start bit (0/1).
 - 'INVALID STOPBIT': The data is the (integer) value of the stop bit (0/1).
 - 'PARITY ERROR': The data is a tuple with two entries. The first one is
   the expected parity value, the second is the actual parity value.
 - 'BREAK': The data is always 0.
 - 'FRAME': The data is always a tuple containing two items: The (integer)
   value of the UART data, and a boolean which reflects the validity of the
   UART frame.

'''

# Given a parity type to check (odd, even, zero, one), the value of the
# parity bit, the value of the data, and the length of the data (5-9 bits,
# usually 8 bits) return True if the parity is correct, False otherwise.
# 'none' is _not_ allowed as value for 'parity_type'.


class SamplerateError(Exception):
    pass


class ChannelError(Exception):
    pass


class Decoder(srd.Decoder):
    api_version = 3
    id = 'swd_analyzer'
    name = 'SWD Analyzer'
    longname = 'SWD Analyzer'
    desc = 'SWD Analyzer'
    license = 'gplv2+'
    inputs = ['swd']
    outputs = ['swd_analyzer']
    tags = ['Embedded/industrial']
    options = (
    )

    annotations = (
    )

    annotation_rows = (
    )

    # def putx(self, data):
    #     s, halfbit = self.startsample, self.bit_width / 2.0
    #     if self.options['anno_startstop'] == 'yes':
    #         self.put(s - floor(halfbit), self.samplenum +
    #                  ceil(halfbit), self.out_ann, data)
    #     else:
    #         self.put(self.byte_start, self.samplenum + ceil(halfbit *
    #                  (1+self.options['num_stop_bits'])), self.out_ann, data)

    # def putg(self, data):
    #     s, halfbit = self.samplenum, self.bit_width / 2.0
    #     self.put(s - floor(halfbit), s + ceil(halfbit), self.out_ann, data)

    # def putgse(self, ss, es, data):
    #     self.put(ss, es, self.out_ann, data)

    def __init__(self):
        self.reset()

    def reset(self):
        self.samplerate = None
        self.byte_timeout = None
        self.request_timeout = None
        self.frame_start = 0
        self.frame_stop = 0
        self.frame_valid = None
        self.request_state = 0
        self.request_req_start = 0
        self.request_req_stop = 0
        self.polling_cycle_start = -1
        self.polling_cycle_stop = -1
        self.data_bytes = []
        self.data_ss = []
        self.data_es = []
        self.byte = 0
        self.ss = 0
        self.es = 0

    def metadata(self, key, value):
        if key == srd.SRD_CONF_SAMPLERATE:
            self.samplerate = value

            self.byte_timeout = ceil(
                float(self.options['byte_timeout']) /
                1000_000 * float(self.samplerate)
            )

            self.request_timeout = ceil(
                float(self.options['request_timeout']) /
                1000_000 * float(self.samplerate)
            )

    def start(self):
        self.out_python = self.register(srd.OUTPUT_PYTHON)
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def decode(self, ss, es, data):
        ptype, rxtx, pdata = data
        self.ss = ss

        raise SamplerateError("unknow devode data type {}".format(ptype))
