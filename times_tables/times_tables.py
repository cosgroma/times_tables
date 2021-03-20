"""Main module."""

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt

# from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, QVBoxLayout, QWidget

pg.setConfigOptions(antialias=True)


class ModuloCircle(object):
  """docstring for ModuloCircle"""
  def __init__(self, radius, num_points, mult_factor):
    super(ModuloCircle, self).__init__()

    self.pw = pg.PlotWidget(title="Modulo Circle")
    self.pw.resize(QtCore.QSize(500, 500))
    self.pw.showGrid(x=False, y=False)
    self.pw.hideAxis('left')
    self.pw.hideAxis('bottom')

    self.radius = radius
    self.num_points = num_points
    self.circ_size = self.num_points**3

    self.mult_factor = mult_factor
    self.build_circle()
    self.plot_points()
    self.add_lines()
    # self.update_lines()


  def build_circle(self):
    x = np.cos(np.linspace(0, self.radius * 2 * np.pi, self.circ_size))
    y = np.sin(np.linspace(0, self.radius * 2 * np.pi, self.circ_size))
    self.circle = (x,y)
    self.circ_points = np.array(list(zip(x, y)))
    self.pw.plot(*self.circle)

  def plot_points(self):
    circ_point_idx = list(np.linspace(0, self.circ_size, self.num_points, endpoint=False, dtype=np.int32))
    self.points = self.circ_points[circ_point_idx]
    self.points_artist = self.pw.plot(self.points, pen=None, symbolBrush=(255, 0, 0), symbolPen='w')

  def update_points(self):
    circ_point_idx = list(np.linspace(0, self.circ_size, self.num_points, endpoint=False, dtype=np.int32))
    self.points = self.circ_points[circ_point_idx]
    self.points_artist.setData(self.points)
    self.update_lines()
  
  def add_lines(self):
    self.lines = []
    for idx in range(0, self.num_points):
      nindx = (idx * self.mult_factor) % self.num_points
      self.lines.append(
        self.pw.plot(
          [self.points[idx][0], self.points[nindx][0]],
          [self.points[idx][1], self.points[nindx][1]]
          )
        )  
  
  def clear_lines(self):
    for idx in range(0, self.num_points):
      self.lines[idx].setData()

  def update_lines(self):
    for idx in range(0, self.num_points):
      if idx >= len(self.lines):
        self.lines.append(self.pw.plot())

    for idx in range(0, self.num_points):
      nindx = (idx * self.mult_factor) % self.num_points
      self.lines[idx].setData(
          [self.points[idx][0], self.points[nindx][0]],
          [self.points[idx][1], self.points[nindx][1]]
          )  

  def update_num_points(self, num_points):
    self.clear_lines()
    self.num_points = num_points
    self.update_points()

  def update_mult_factor(self, mult_factor):
    self.clear_lines()
    self.mult_factor = mult_factor
    self.update_points()


class TimesTables(QWidget):
  """docstring for TimesTables"""
  def __init__(self, parent=None):
    super(TimesTables, self).__init__(parent=parent)
    self.verticalLayout = QVBoxLayout(self)
    initial_num_points = 200
    initial_mult_factor = 2

    self.mod_circle = ModuloCircle(1, initial_num_points, initial_mult_factor)
    self.verticalLayout.addWidget(self.mod_circle.pw)
    
    self.num_points_slider = QSlider(self)
    self.num_points_slider.setOrientation(Qt.Horizontal)
    self.num_points_slider.setMinimum(initial_num_points)
    self.num_points_slider.setMaximum(200)
    self.num_points_slider.valueChanged.connect(self.set_num_points)
    self.verticalLayout.addWidget(self.num_points_slider)

    
    self.mult_factor_slider = QSlider(self)
    self.mult_factor_slider.setOrientation(Qt.Horizontal)
    self.mult_factor_slider.setMinimum(initial_mult_factor)
    self.mult_factor_slider.setMaximum(200-1)
    self.mult_factor_slider.valueChanged.connect(self.set_mult_factor)
    self.verticalLayout.addWidget(self.mult_factor_slider)
    

    self.resize(QtCore.QSize(500, 500))


  def set_mult_factor(self, value):
    self.mod_circle.update_mult_factor(value)

  def set_num_points(self, value):
    self.mod_circle.update_num_points(value)
    

    

def main():
  import sys
  app = QtGui.QApplication([])
  tt = TimesTables()
  tt.show()
  app.exec_()

if __name__ == '__main__':
  main()