# coding=utf-8

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
from openexp._canvas._element.element import Element


class Line(Element):

	def __init__(self, canvas, sx, sy, ex, ey, **properties):

		properties = properties.copy()
		properties.update({'sx' : sx, 'sy' : sy, 'ex' : ex, 'ey' : ey})
		Element.__init__(self, canvas, **properties)

	@property
	def rect(self):

		top = min(sy, ey)
		bottom = max(sy, ey)
		left = min(sx, ex)
		right = max(sx, ex)
		return left, top, right-left, bottom-top