"""
Copyright [2016] [Satbir Singh]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from gui import control
from gui import circle
from gui import line
from gui import textdraw

from PySide import QtCore

LEFT = -7.9
RIGHT = 7.9
TOP = -8
BOTTOM = 8

LEN = 15

Gap = 2.0


class SourceManager(object):
    """

    """

    def __init__(self):
        """

        """
        self.sources = {}
        self._index = 0
        self._zoom_factor = 1
        self._recenter = 0
        pass

    def register_source(self, source):
        """ Register an source with manager

        :param source: input source
        :return: index number of this source, this index can be later used to delete this source
        """
        self._index += 1
        self.sources[self._index] = source

        return self._index

    def delete_source(self, index):
        del self.sources[index]

    def getControls(self):
        """

        :return:
        """

        controls = []
        text = []

        if not self.sources:
            return controls, text
        data = self.sources[1].get_data(self._zoom_factor, self._recenter)
        y_axis = 0
        for key, value in sorted(data.iteritems()):
            y_axis += 1
            t = textdraw.Text()
            t.x = LEFT
            t.y = y_axis + 0.2
            t.text = key
            text.append(t)
            bounds = control.Bounds(control.Point(LEFT, y_axis), control.Point(BOTTOM, y_axis))
            lineA = line.ALine()
            lineA.set_bounds(bounds)
            controls.append(lineA)
            for a in value:
                x_axis = LEFT + (self.sources[1].getpos(a) * LEN)
                c = circle.Circle(control.Point(x_axis, y_axis), .5)
                controls.append(c)

                bounds = control.Bounds(control.Point(x_axis, y_axis), control.Point(x_axis, TOP+2))
                lineA = line.ALine()
                lineA.set_color(1, 1, 0)
                lineA.set_bounds(bounds)
                lineA.enableStipple(True)
                controls.append(lineA)
                pass

        t1 = textdraw.Text()
        t1.x = LEFT
        t1.y = TOP+3
        t1.text = str(self.sources[1].render_start_date())
        text.append(t1)
        t2 = textdraw.Text()
        t2.x = RIGHT-4
        t2.y = TOP+3
        t2.text = str(self.sources[1].render_end_date())
        text.append(t2)
        bounds = control.Bounds(control.Point(LEFT, TOP+2), control.Point(RIGHT, TOP+2))
        scale = line.ALine()
        scale.set_color(1, 1, 0)
        scale.set_bounds(bounds)
        scale.enableStipple(True)
        controls.append(scale)

        return controls, text

    def zoom_in(self):
        self._zoom_factor += 1
        print "zoom_in %d" % self._zoom_factor

    def zoom_out(self):
        self._zoom_factor -= 1
        if self._zoom_factor is 0:
            self._zoom_factor = 1

        print "zoom_out %d" % self._zoom_factor

    def go_right(self):
        self._recenter -= 1
        print "go_right %d" % self._recenter

    def go_left(self):
        self._recenter += 1
        print "v %d" % self._recenter

    def reset_scale(self):
        print "reset_scale"
        self._recenter = 0
        self._zoom_factor = 1
