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


ANN_RESET = 0
ANN_TOUCH = 1
ANN_DATA = 2


class Decoder(srd.Decoder):
    api_version = 3
    id = 'swd_analyzer'
    name = 'SWD Analyzer'
    longname = 'SWD Analyzer'
    desc = 'SWD Analyzer'
    license = 'gplv2+'
    inputs = ['swd']
    outputs = []
    tags = ['Debug/trace']
    options = (
        {'id': 'core', 'desc': 'core type',
            'default': 'M0', 'values': ('M0', 'M3', 'M4'), 'idn': 'dec_core_type'},
    )

    annotations = (
        ('reset', 'RESET'),
        ('touch', 'TOUCH'),
        ('7', 'data', 'DATA'),
    )

    annotation_rows = (
        ('touch', 'Touch', (ANN_TOUCH,)),
        ('data', 'DATA', (ANN_RESET, ANN_DATA,)),
    )

    def __init__(self):
        self.reset()

    def reset(self):

        self.touch_ss = None
        self.touch_es = None
        self.idcode = None
        # self.es = 0
        # self.cnt = 0

    def metadata(self, key, value):
        if key == srd.SRD_CONF_SAMPLERATE:
            self.samplerate = value

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)
        # self.out_python = self.register(srd.OUTPUT_PYTHON)

    def decode(self, ss, es, data):
        ptype, pdata = data
        # self.ss = ss

        if ptype == 'LINE_RESET':

            if self.touch_ss is None:
                self.touch_ss = ss

        elif ptype == 'DP_READ':

            if pdata[0] == 0:

                self.idcode = pdata[1]
                self.status = pdata[2]

                if self.status == 'OK':

                    if (self.touch_ss is not None) and (self.touch_es is None):
                        self.touch_es = es

                        self.put(self.touch_ss, self.touch_es, self.out_ann,
                                 [ANN_TOUCH, [
                                     "TOUCH 0x{:08X} {:f}S".format(
                                         self.idcode, (self.touch_es-self.touch_ss)/self.samplerate),
                                 ]])

                    self.put(ss, es, self.out_ann,
                             [ANN_DATA, [
                                 "IDCODE 0x{:08X}".format(self.idcode),
                             ]])

            # else:
            #     self.put(ss, es, self.out_ann,
            #              [ANN_DATA, [
            #                  "{0}".format(data),
            #              ]])

        # else:
        #     self.put(ss, es, self.out_ann,
        #              [ANN_DATA, [
        #                  "{0}".format(data),
        #              ]])
