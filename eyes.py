#!/usr/bin/env python
#Copyright (c) 2012 Walter Bender
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from gettext import gettext as _

from plugins.eyes.eyesj import Eyesjun
from plugins.plugin import Plugin

from TurtleArt.tapalette import make_palette
from TurtleArt.talogo import primitive_dictionary
from TurtleArt.tautils import debug_output

import logging
_logger = logging.getLogger('turtleart-activity Eyes-junior plugin')


class Eyes(Plugin):

    def __init__(self, parent):
        self._parent = parent
        self._status = False

        '''
        The following code will initialize a USB Eyes-junior
        device. Please note that it is necessary to set up the udev
        permissions for this device by running the script:

        sudo sh postint

        You only have to do this once.
        '''

        self.eyes = Eyesjun()

        if self.eyes.fd is None:
            _logger.info("Eyes device not found")
            self._status = False
        else:
            _logger.info("Eyes device found")
            _logger.info(self.eyes.get_version())
            self._status = True

    def setup(self):
        ''' Set up Expeyes-specific blocks '''
        primitive_dictionary['eyes-pvsv'] = self._prim_eyes_set_pvs_voltage
        primitive_dictionary['eyes-sqr1v'] = self._prim_eyes_set_sqr1_voltage
        primitive_dictionary['eyes-sqr1f'] = self._prim_eyes_set_sqr1_freq
        primitive_dictionary['eyes-sqr2v'] = self._prim_eyes_set_sqr2_voltage
        primitive_dictionary['eyes-sqr2f'] = self._prim_eyes_set_sqr2_freq
        primitive_dictionary['eyes-set-state'] = self._prim_eyes_set_state
        primitive_dictionary['eyes-get-state'] = self._prim_eyes_get_state
        primitive_dictionary['eyes-voltage'] = self._prim_eyes_get_voltage
        primitive_dictionary['eyes-capture'] = self._prim_eyes_capture

        palette = make_palette('eyes',
                               colors=["#FF6060", "#A06060"],
                               help_string=_('Palette of Expeyes blocks'))

        palette.add_block('pvsv',
                          style='basic-style-1arg',
                          label=_('set PVS'),
                          default=5,
                          help_string=_('set programmable voltage output'),
                          value_block=True,
                          prim_name='eyes-pvsv')
        palette.add_block('sqr1v',
                          style='basic-style-1arg',
                          label=_('set SQR1 voltage'),
                          default=5,
                          help_string=_('set square wave 1 voltage output'),
                          value_block=True,
                          prim_name='eyes-sqr1v')
        palette.add_block('sqr1f',
                          style='basic-style-1arg',
                          label=_('set SQR1 frequency'),
                          default=5,
                          help_string=_('set square wave 1 frequency output'),
                          value_block=True,
                          prim_name='eyes-sqr1f')
        palette.add_block('sqr2v',
                          style='basic-style-1arg',
                          label=_('set SQR2 voltage'),
                          default=5,
                          help_string=_('set square wave 2 voltage output'),
                          value_block=True,
                          prim_name='eyes-sqr2v')
        palette.add_block('sqr2f',
                          style='basic-style-1arg',
                          label=_('set SQR2 frequency'),
                          default=5,
                          help_string=_('set square wave 2 frequency output'),
                          value_block=True,
                          prim_name='eyes-sqr2f')
        palette.add_block('od1s',
                          style='basic-style-1arg',
                          label=_('set OD1'),
                          help_string=_('set digital output level low (0) or \
high (1)'),
                          value_block=True,
                          prim_name='eyes-od1s')
        palette.add_block('in1s',
                          style='boolean-block-style',
                          label=_('IN1 level'),
                          prim_name='eyes-in1s',
                          value_block=True,
                          help_string=_('returns 1 if input 1 voltage level >\
2.5 volts, 0 if in1 voltage level <= 2.5 volts'))
        palette.add_block('in2s',
                          style='boolean-block-style',
                          label=_('IN2 level'),
                          prim_name='eyes-in2s',
                          value_block=True,
                          help_string=_('returns 1 if input 2 voltage level >\
2.5 volts, 0 if in2 voltage level <= 2.5 volts'))
        palette.add_block('sens',
                          style='boolean-block-style',
                          label=_('SEN level'),
                          prim_name='eyes-sens',
                          value_block=True,
                          help_string=_('returns 1 if resistive sensor voltage \
level > 2.5 volts, 0 if sen voltage level <= 2.5 volts'))
        palette.add_block('capture-a1',
                          style='basic-style-2arg',
                          label=[_('capture A1'), _('samples'), _('interval')],
                          default=[300, 100],
                          help_string=_('capture multiple samples from analog \
input 1 at interval (MS); results pushed to FIFO'),
                          prim_name='eyes-capture-a1')
        palette.add_block('a1',
                          style='box-style',
                          label=_('A1'),
                          help_string=_('read analog input 1 voltage'),
                          value_block=True,
                          prim_name='eyes-a1')
        palette.add_block('capture-a2',
                          style='basic-style-2arg',
                          label=[_('capture A2'), _('samples'), _('interval')],
                          default=[300, 100],
                          help_string=_('capture multiple samples from analog \
input 2 at interval (MS); results pushed to FIFO'),
                          prim_name='eyes-capture-a2')
        palette.add_block('a2',
                          style='box-style',
                          label=_('A2'),
                          help_string=_('read analog input 2 voltage'),
                          value_block=True,
                          prim_name='eyes-a2')
        palette.add_block('capture-in1',
                          style='basic-style-2arg',
                          label=[_('capture IN1'), _('samples'), _('interval')],
                          default=[300, 100],
                          help_string=_('capture multiple samples from input 1 \
at interval (MS); results pushed to FIFO'),
                          prim_name='eyes-capture-in1')
        palette.add_block('in1',
                          style='box-style',
                          label=_('IN1'),
                          help_string=_('read input 1 voltage'),
                          value_block=True,
                          prim_name='eyes-in1v')
        palette.add_block('capture-in2',
                          style='basic-style-2arg',
                          label=[_('capture IN2'), _('samples'), _('interval')],
                          default=[300, 100],
                          help_string=_('capture multiple samples from input 2 \
at interval (MS); results pushed to FIFO'),
                          prim_name='eyes-capture-in2')
        palette.add_block('in2',
                          style='box-style',
                          label=_('IN2'),
                          help_string=_('read input 2 voltage'),
                          value_block=True,
                          prim_name='eyes-in2')
        palette.add_block('capture-sen',
                          style='basic-style-2arg',
                          label=[_('capture SEN'), _('samples'), _('interval')],
                          help_string=_('capture multiple samples from sensor \
input at interval (MS); results pushed to FIFO'),
                          default=[300, 100],
                          prim_name='eyes-capture-sen')
        palette.add_block('sen',
                          style='box-style',
                          label=_('SEN'),
                          help_string=_('read analog sensor input voltage'),
                          value_block=True,
                          prim_name='eyes-sen')
        palette.add_block('sqr1',
                          style='box-style',
                          label=_('SQR1'),
                          help_string=_('read square wave 1 voltage'),
                          value_block=True,
                          prim_name='eyes-sqr1')
        palette.add_block('sqr2',
                          style='box-style',
                          label=_('SQR2'),
                          help_string=_('read square wave 2 voltage'),
                          value_block=True,
                          prim_name='eyes-sqr2')
        palette.add_block('pvs',
                          style='box-style',
                          label=_('PVS'),
                          help_string=_('read programmable voltage'),
                          value_block=True,
                          prim_name='eyes-pvs')

        self._parent.lc.def_prim(
            'eyes-pvs', 1,
            lambda self, x: primitive_dictionary['eyes-pvs'](x))
        self._parent.lc.def_prim(
            'eyes-sqr1v', 1,
            lambda self, x: primitive_dictionary['eyes-sqr1'](x))
        self._parent.lc.def_prim(
            'eyes-sqr1f', 1,
            lambda self, x: primitive_dictionary['eyes-sqr1f'](x))
        self._parent.lc.def_prim(
            'eyes-sqr2v', 1,
            lambda self, x: primitive_dictionary['eyes-sqr2'](x))
        self._parent.lc.def_prim(
            'eyes-sqr2f', 1,
            lambda self, x: primitive_dictionary['eyes-sqr2f'](x))
        self._parent.lc.def_prim(
            'eyes-in1', 0,
            lambda self: primitive_dictionary['eyes-get-state'](3))
        self._parent.lc.def_prim(
            'eyes-in2', 0,
            lambda self: primitive_dictionary['eyes-get-state'](4))
        self._parent.lc.def_prim(
            'eyes-sen', 0,
            lambda self: primitive_dictionary['eyes-get-state'](5))
        self._parent.lc.def_prim(
            'eyes-od1', 1,
            lambda self, x: primitive_dictionary['eyes-set-state'](10, x))
        self._parent.lc.def_prim(
            'eyes-a1', 0,
            lambda self: primitive_dictionary['eyes-voltage'](1))
        self._parent.lc.def_prim(
            'eyes-a2', 0,
            lambda self, x: primitive_dictionary['eyes-voltage'](2))
        self._parent.lc.def_prim(
            'eyes-in1', 0,
            lambda self, x: primitive_dictionary['eyes-voltage'](3))
        self._parent.lc.def_prim(
            'eyes-in2', 0,
            lambda self, x: primitive_dictionary['eyes-voltage'](4))
        self._parent.lc.def_prim(
            'eyes-sen', 0,
            lambda self, x: primitive_dictionary['eyes-voltage'](5))
        self._parent.lc.def_prim(
            'eyes-sqr1', 0,
            lambda self, x: primitive_dictionary['eyes-voltage'](6))
        self._parent.lc.def_prim(
            'eyes-sqr2', 0,
            lambda self, x: primitive_dictionary['eyes-voltage'](7))
        self._parent.lc.def_prim(
            'eyes-pvs', 0,
            lambda self, x: primitive_dictionary['eyes-voltage'](12))
        self._parent.lc.def_prim(
            'eyes-capture-a1', 2,
            lambda self, x, y: primitive_dictionary['eyes-capture'](1, x, y))
        self._parent.lc.def_prim(
            'eyes-capture-a2', 2,
            lambda self, x, y: primitive_dictionary['eyes-capture'](2, x, y))
        self._parent.lc.def_prim(
            'eyes-capture-in1', 2,
            lambda self, x, y: primitive_dictionary['eyes-capture'](3, x, y))
        self._parent.lc.def_prim(
            'eyes-capture-in2', 2,
            lambda self, x, y: primitive_dictionary['eyes-capture'](4, x, y))
        self._parent.lc.def_prim(
            'eyes-capture-sen', 2,
            lambda self, x, y: primitive_dictionary['eyes-capture'](5, x, y))

    def _status_report(self):
        debug_output('Reporting Eyes status: %s' % (str(self._status)))
        return self._status

    def _prim_eyes_set_pvs_voltage(self, volt):
        if self._status:
            self.eyes.set_voltage(volt)
        else:
            self._parent.showlabel('status', _('Expeyes device not found'))

    def _prim_eyes_set_sqr1_voltage(self, volt):
        if self._status:
            self.eyes.set_sqr1_dc(volt)
        else:
            self._parent.showlabel('status', _('Expeyes device not found'))

    def _prim_eyes_set_sqr1_freq(self, freq):
        if freq < 0.7:
            freq = 0.7
        if freq > 200000:
            freq = 200000
        if self._status:
            self.eyes.set_sqr1(freq)
        else:
            self._parent.showlabel('status', _('Expeyes device not found'))

    def _prim_eyes_set_sqr2_voltage(self, volt):
        if self._status:
            self.eyes.set_sqr2_dc(volt)
        else:
            self._parent.showlabel('status', _('Expeyes device not found'))

    def _prim_eyes_set_sqr2_freq(self, freq):
        if freq < 0.7:
            freq = 0.7
        if freq > 200000:
            freq = 200000
        if self._status:
            self.eyes.set_sqr2(freq)
        else:
            self._parent.showlabel('status', _('Expeyes device not found'))

    def _prim_eyes_get_state(self, channel):
        return self.eyes.get_state(channel)

    def _prim_eyes_set_state(self, channel, state):
        if state < 1:
            state = 0
        else:
            state = 1
        if self._status:
            self.eyes.set_state(channel, state)
        else:
            self._parent.showlabel('status', _('Expeyes device not found'))

    def _prim_eyes_get_voltage(self, channel):
        if self._status:
            return self.eyes.get_voltage(channel)
        else:
            self._parent.showlabel('status', _('Expeyes device not found'))
            return -1

    def _prim_eyes_capture(self, channel, samples, interval):
        if samples < 0:
            samples = 0
        elif samples > 1800:
            samples = 1800
        if self._status:
            t, v = self.eyes.capture(channel, int(samples), int(interval))
            for i in range(len(v)):
                # Push onto stack as FIFO
                self._parent.lc.heap.append(v[len(v) - i - 1])
        else:
            for i in range(int(samples)):
                self._parent.lc.heap.append(-1)  # Push onto stack as FIF
            self._parent.showlabel('status', _('Expeyes device not found'))
