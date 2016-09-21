import sys
import math
from OpenGL.GL import *
from PySide import QtCore, QtGui, QtOpenGL


class Bubble(object):
    def __init__(self, x, y, w):
        self._x = x
        self._y = y
        self._w = w
        pass

    def render(self):
        num_triangles = 20
        twice_the_pi = 3.14159 * 2
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0, 1, 0)
        glVertex2f(self._x, self._y)
        for i in range(num_triangles+1):
            glVertex2f(self._x + (self._w * math.cos(i * twice_the_pi / num_triangles)),
                       self._y + (self._w * math.sin(i * twice_the_pi / num_triangles)))
        glEnd()


class LocalWidget(QtOpenGL.QGLWidget):
    zRotationChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(LocalWidget, self).__init__(parent)
        self.width = 0
        self.height = 0
        self._bubble = Bubble(- 3.0, 1.0, 1.0)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.render)
        timer.start(20)

    def render(self):
        self._bubble.render()

    def __del__(self):
        print "GLWidget.__del__"
        self.makeCurrent()

    def initializeGL(self):
        print "GLWidget.initializeGL"

        glEnable(GL_BLEND)
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        self._bubble.render()
        glPopMatrix()

    def resizeGL(self, width, height):
        print "GLWidget.resizeGL"

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0, +1.0, -1.0, 1.0, 5.0, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -40.0)

    def mousePressEvent(self, event):
        print "dx %d" % event.x()
        print "dy %d" % event.y()

    def mouseMoveEvent(self, event):
        print "dx %d" % event.x()
        print "dy %d" % event.y()


class DisplayEngine(QtGui.QMainWindow):
    def __init__(self):
        print "DisplayEngine.__init__"
        super(DisplayEngine, self).__init__()
        central_widget = QtGui.QWidget()
        self.setCentralWidget(central_widget)
        self.glWidget = LocalWidget()

        self.glWidgetArea = QtGui.QScrollArea()
        self.glWidgetArea.setWidget(self.glWidget)
        self.glWidgetArea.setWidgetResizable(True)
        self.glWidgetArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.glWidgetArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.glWidgetArea.setSizePolicy(QtGui.QSizePolicy.Ignored,
                                        QtGui.QSizePolicy.Ignored)
        self.glWidgetArea.setMinimumSize(50, 50)
        central_layout = QtGui.QGridLayout()
        central_layout.addWidget(self.glWidgetArea, 0, 0, 4, 4)
        central_widget.setLayout(central_layout)
        self.setWindowTitle("Visual Log Monitor")
        self.resize(600, 600)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = DisplayEngine()
    mainWin.show()
    sys.exit(app.exec_())
