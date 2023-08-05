# -*- coding: utf-8 -*-
#
# AWL simulator - FUP - Boolean element classes
#
# Copyright 2016-2017 Michael Buesch <m@bues.ch>
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
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from __future__ import division, absolute_import, print_function, unicode_literals
from awlsim.common.compat import *

from awlsim.common.xmlfactory import *

from awlsim.gui.fup.fup_base import *
from awlsim.gui.fup.fup_elem import *
from awlsim.gui.fup.fup_elemoperand import *


class FupElem_BOOLEAN_factory(FupElem_factory):
	def composer_getTags(self):
		connTags = []
		for inp in self.elem.inputs:
			connTags.extend(inp.factory(conn=inp).composer_getTags())
		for out in self.elem.outputs:
			connTags.extend(out.factory(conn=out).composer_getTags())
		return [
			self.Tag(name="element",
				attrs={
					"type" : "boolean",
					"subtype" : self.elem.OP_SYM_NAME,
					"x" : str(self.elem.x),
					"y" : str(self.elem.y),
				},
				tags=[
					self.Tag(name="connections",
						 tags=connTags),
				])
		]

class FupElem_BOOLEAN(FupElem):
	"""Boolean FUP/FBD element base class"""

	factory = FupElem_BOOLEAN_factory

	def __init__(self, x, y, nrInputs=2):
		FupElem.__init__(self, x, y)

		self.inputs = [ FupConnIn(self)\
				for i in range(nrInputs) ]
		self.outputs = [ FupConnOut(self) ]

	# Overridden method. For documentation see base class.
	def insertConn(self, beforeIndex, conn):
		if conn and conn.OUT:
			return False
		return FupElem.insertConn(self, beforeIndex, conn)

	# Overridden method. For documentation see base class.
	def addConn(self, conn):
		if conn and conn.OUT:
			return False
		return FupElem.addConn(self, conn)

	# Overridden method. For documentation see base class.
	def getAreaViaPixCoord(self, pixelX, pixelY):
		if self.grid:
			cellWidth = self.grid.cellPixWidth
			cellHeight = self.grid.cellPixHeight
			totalWidth = cellWidth
			totalHeight = cellHeight * self.height
			xpad, ypad = self._xpadding, self._ypadding
			if pixelY > ypad and pixelY < totalHeight - ypad:
				if pixelX < xpad:
					# inputs
					idx = pixelY // cellHeight
					return self.AREA_INPUT, idx
				elif pixelX > totalWidth - xpad:
					# outputs
					if pixelY >= totalHeight - cellHeight:
						return self.AREA_OUTPUT, 0
				else:
					# body
					return self.AREA_BODY, 0
		return self.AREA_NONE, 0

	# Overridden method. For documentation see base class.
	def getConnRelCoords(self, conn):
		x, y = 0, -1
		if conn.IN:
			y = self.inputs.index(conn)
		elif conn.OUT:
			y = self.outputs.index(conn)
			if y >= 0:
				y = self.height - 1
		if x >= 0 and y >= 0:
			return x, y
		return FupElem.getConnRelCoords(self, conn)

	# Overridden method. For documentation see base class.
	@property
	def height(self):
		return len(self.inputs)

	# Overridden method. For documentation see base class.
	def draw(self, painter):
		grid = self.grid
		if not grid:
			return
		cellWidth = grid.cellPixWidth
		cellHeight = grid.cellPixHeight
		xpad, ypad = self._xpadding, self._ypadding
		elemHeight = cellHeight * self.height
		elemWidth = cellWidth
		notR = 3
		notD = notR * 2

		# Draw inputs
		painter.setBrush(self._bgBrush)
		for i, conn in enumerate(self.inputs):
			x = conn.CONN_OFFS if conn.isConnected else 0
			y = (i * cellHeight) + (cellHeight // 2)
			painter.setPen(self._connPen if conn.isConnected
				       else self._connOpenPen)
			painter.drawLine(x, y, xpad, y)
			if conn.inverted:
				painter.setPen(self._connInvSelPen\
					       if self.selected else\
					       self._connInvPen)
				painter.drawEllipse(xpad - notD, y - notR,
						    notD, notD)

		# Draw output
		painter.setBrush(self._bgBrush)
		if self.outputs:
			assert(len(self.outputs) == 1)
			conn = self.outputs[0]
			x = (cellWidth - conn.CONN_OFFS) if conn.isConnected\
			    else cellWidth
			y = elemHeight - (cellHeight // 2)
			painter.setPen(self._connPen if conn.isConnected
				       else self._connOpenPen)
			painter.drawLine(cellWidth - xpad, y,
					 cellWidth, y)
			if conn.inverted:
				painter.setPen(self._connInvSelPen\
					       if self.selected else\
					       self._connInvPen)
				painter.drawEllipse(cellWidth - xpad, y - notR,
						    notD, notD)

		# Draw body
		painter.setPen(self._outlineSelPen if self.selected
			       else self._outlinePen)
		painter.setBrush(self._bgBrush)
		(tlX, tlY), (trX, trY), (blX, blY), (brX, brY) = self._calcBodyBox()
		painter.drawRoundedRect(tlX, tlY,
					trX - tlX, blY - tlY,
					self.BODY_CORNER_RADIUS,
					self.BODY_CORNER_RADIUS)

		# Draw symbol text
		painter.setFont(getDefaultFixedFont(11))
		painter.drawText(0, 5,
				 elemWidth, elemHeight - 5,
				 Qt.AlignVCenter | Qt.AlignHCenter,
				 self.OP_SYM)

	# Overridden method. For documentation see base class.
	def prepareContextMenu(self, menu, area=None, conn=None):
		menu.enableInvertConn(True)
		menu.enableAddInput(True)
		menu.enableRemoveConn(conn is not None and conn.IN and len(self.inputs) > 2)
		menu.enableDisconnWire(conn is not None and conn.isConnected)

	# Overridden method. For documentation see base class.
	def setConnInverted(self, conn, inverted=True):
		if conn in self.inputs or conn in self.outputs:
			conn.inverted = inverted
			return True
		return False

class FupElem_AND(FupElem_BOOLEAN):
	"""AND FUP/FBD element"""

	OP_SYM		= "&"
	OP_SYM_NAME	= "and"	# XML ABI name

class FupElem_OR(FupElem_BOOLEAN):
	"""OR FUP/FBD element"""

	OP_SYM		= ">=1"
	OP_SYM_NAME	= "or"	# XML ABI name

class FupElem_XOR(FupElem_BOOLEAN):
	"""XOR FUP/FBD element"""

	OP_SYM		= "X"
	OP_SYM_NAME	= "xor"	# XML ABI name
