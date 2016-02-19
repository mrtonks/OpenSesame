#-*- coding:utf-8 -*-

"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame.py3compat import *
from libopensesame.base_response_item import base_response_item
from openexp.mouse import mouse


class mouse_response_mixin(object):

	"""
	desc:
		A mixin class that should be inherited along with base_response_item
		by all classes that want to collect mouse responses.
	"""

	def prepare_response_func(self):

		"""See base_response_item."""

		self._mouse = mouse(self.experiment, timeout=self._timeout,
			buttonlist=self._allowed_responses)
		return self._mouse.get_click

	def process_response(self, response_args):

		"""See base_response_item."""

		response, pos, t1 = response_args
		if pos is None:
			self.experiment.var.cursor_x = u'NA'
			self.experiment.var.cursor_y = u'NA'
		else:
			self.experiment.var.cursor_x, self.experiment.var.cursor_y = pos
		base_response_item.process_response(self, (response, t1) )


class mouse_response(mouse_response_mixin, base_response_item):

	"""
	desc:
		An item for collecting mouse responses.
	"""

	description = u'Collects mouse responses'
	process_feedback = True

	def reset(self):

		"""See item."""

		self.var.flush = u'yes'
		self.var.show_cursor = u'yes'
		self.var.timeout = u'infinite'
		self.var.duration = u'mouseclick'
		self.var.unset(u'allowed_responses')
		self.var.unset(u'correct_response')
		self._resp_codes = {
			None : u'timeout',
			1 : u'left_button',
			2 : u'middle_button',
			3 : u'right_button',
			4 : u'scroll_up',
			5 : u'scroll_down'
			}

	def validate_response(self, response):

		"""See base_response_item."""

		return response in self._resp_codes \
			or response in self._resp_codes.values()

	def response_matches(self, test, ref):

		"""See base_response_item."""

		if test in self._resp_codes and self._resp_codes[test] == ref:
			return True
		return test == ref

	def prepare(self):

		"""See item."""

		base_response_item.prepare(self)
		self._flush = self.var.flush == u'yes'

	def run(self):

		"""See item."""

		if self._flush:
			self._mouse.flush()
		# Show cursor if necessary
		if self.var.show_cursor == u'yes':
			self._mouse.visible = True
		base_response_item.run(self)
		self._mouse.visible = False

	def coroutine(self):

		"""See coroutines plug-in."""

		self._mouse.timeout = 0
		alive = True
		yield
		self._t0 = self.set_item_onset()
		if self._flush:
			self._mouse.flush()
		while alive:
			button, pos, time = self._mouse.get_click()
			if button is not None:
				break
			alive = yield
		self.process_response((button, pos, time))

	def var_info(self):

		"""See item."""

		l = base_response_item.var_info(self)
		l.append( (u'cursor_x', u'[Depends on response]') )
		l.append( (u'cursor_y', u'[Depends on response]') )
		return l
