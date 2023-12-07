from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtGui import QPainter, QBrush, QPen

import parametros as p


class Zone(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimumSize(*p.ZONE_MINIMUM_SIZE)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.point_rad: float = 30
        self.ref_pos = [200, 200]

    def paintEvent(self, _):
        painter = QPainter(self)
        self.draw_crosses(painter)
        self.draw_ref(painter)

    def draw_ref(self, painter: QPainter):
        painter.setPen(QPen(Qt.green, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        ref_point = QPoint(int(self.ref_pos[0]), int(self.ref_pos[1]))
        painter.drawEllipse(ref_point, self.point_rad, self.point_rad)

    def calculate_available_zone(self):
        margin = (p.CROSS_SIZE + 1) / 2 + self.point_rad + 1
        x_range = [margin,
                   self.rect().width() - margin]
        y_range = [margin,
                   self.rect().height() - margin]
        return x_range, y_range

    def calculata_dist_pix(self):
        dist_pix = self.rect().width() - p.CROSS_SIZE
        return dist_pix

    def draw_crosses(self, painter: QPainter):
        painter.setPen(Qt.white)
        self.draw_cross((0, 0), painter)
        self.draw_cross((self.rect().width() - p.CROSS_SIZE,
                         self.rect().height() - p.CROSS_SIZE), painter)
        self.draw_cross((0, self.rect().height() - p.CROSS_SIZE), painter)
        self.draw_cross((self.rect().width() - p.CROSS_SIZE, 0), painter)

    def draw_cross(self, corner_ul: tuple, painter: QPainter):
        painter.drawLine(int(corner_ul[0]),
                         int(corner_ul[1] + (p.CROSS_SIZE - 1) / 2),
                         int(corner_ul[0] + p.CROSS_SIZE - 1),
                         int(corner_ul[1] + (p.CROSS_SIZE - 1) / 2))

        painter.drawLine(int(corner_ul[0] + (p.CROSS_SIZE - 1) / 2),
                         int(corner_ul[1]),
                         int(corner_ul[0] + (p.CROSS_SIZE - 1) / 2),
                         int(corner_ul[1] + p.CROSS_SIZE - 1))
