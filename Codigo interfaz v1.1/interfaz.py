from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QMenu, QAction
from PyQt5.QtGui import QContextMenuEvent

from pyqtdesigner.interfaz_ui import Ui_MainWindow

import json

import parametros as p

from move_gen import MoveGen
from zone import Zone


class Interfaz(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.zone = Zone(self)
        self.ui.verticalLayout.addWidget(self.zone)
        self.move_gen = MoveGen()
        self.timer = QTimer()
        self.radios = {
            self.ui.radio_movie: "movie",
            self.ui.radio_random: "random",
            self.ui.radio_fly: "fly",
            self.ui.radio_smart_fly: "smart_fly"
        }

        self.set_initials()
        self.set_connections()
        self.set_params()

    def set_initials(self):
        self.ui.radio_movie.setChecked(True)
        self.ui.button_start.setEnabled(True)
        self.ui.button_stop.setEnabled(False)
        with open(p.SETTINGS_PATH, 'r') as f:
            data = json.load(f)

        self.ui.spin_size.setValue(data['point_radius'])
        self.ui.spin_dist.setValue(data['distance'])
        self.ui.spin_vel.setValue(data['vel'])

        self.zone.point_rad = data['point_radius']
        self.move_gen.__dict__.update(data)
        self.update_vel_dist()

    def set_connections(self):
        self.ui.spin_size.valueChanged.connect(self.resize_point)
        self.ui.spin_dist.valueChanged.connect(self.update_vel_dist)
        self.ui.spin_vel.valueChanged.connect(self.update_vel_dist)

        self.ui.spin_size.valueChanged.connect(self.save_settings)
        self.ui.spin_dist.valueChanged.connect(self.save_settings)
        self.ui.spin_vel.valueChanged.connect(self.save_settings)

        for radio_button in self.radios.keys():
            radio_button.toggled.connect(self.set_mode)

        self.ui.button_start.clicked.connect(self.start)
        self.ui.button_stop.clicked.connect(self.stop)
        self.ui.pushButton_randomStep.clicked.connect(self.random_step)

    def set_params(self):
        with open(p.SETTINGS_PATH, 'r') as f:
            data = json.load(f)

        self.other_params = [
            [self.ui.spinBox_fly_max_angle, "fly_max_angle"],
            [self.ui.spinBox_sfly_max_angle, "sfly_max_angle"],
            [self.ui.doubleSpinBox_sfly_max_beta, "sfly_max_beta_value"],
        ]

        self.time_arrays = [
            [[self.ui.spinBox_fly_time_low, self.ui.spinBox_fly_time_high],
             "fly_max_counter_limits"],
            [[self.ui.spinBox_sfly_time_low, self.ui.spinBox_sfly_time_high],
             "sfly_max_counter_limits"],
            [[self.ui.spinBox_rndm_time_low, self.ui.spinBox_rndm_time_high],
             "random_max_counter_limits"]
        ]

        for time_array in self.time_arrays:
            spins = time_array[0]
            for spin in spins:
                spin.valueChanged.connect(self.time_array_changed)
                spin.valueChanged.connect(self.save_settings)

        for other_param in self.other_params:
            other_param[0].valueChanged.connect(self.other_param_changed)
            other_param[0].valueChanged.connect(self.save_settings)

        for time_array in self.time_arrays:
            for index in range(len(time_array[0])):
                time_array[0][index].setValue(data[time_array[1]][index])

        for other_param in self.other_params:
            other_param[0].setValue(data[other_param[1]])

    def save_settings(self):
        with open(p.SETTINGS_PATH, 'r') as f:
            data = json.load(f)

        data['point_radius'] = self.ui.spin_size.value()
        data['distance'] = self.ui.spin_dist.value()
        data['vel'] = self.ui.spin_vel.value()

        for time_array in self.time_arrays:
            variable = time_array[1]
            range = []
            for item in time_array[0]:
                range.append(item.value())
            data[variable] = range

        for param in self.other_params:
            variable = param[1]
            data[variable] = param[0].value()

        with open(p.SETTINGS_PATH, 'w') as f:
            json.dump(data, f, indent=2)

    def set_mode(self):
        for radio_button in self.radios.keys():
            if radio_button.isChecked():
                self.move_gen.mode = self.radios[radio_button]

    @pyqtSlot(int)
    def time_array_changed(self, value: int):
        for time_array in self.time_arrays:
            for object in time_array[0]:
                if object == self.sender():
                    variable = time_array[1]

        name = self.sender().objectName()
        type = name.split('_')[-1]
        if type == 'low':
            other_spin = self.ui.__dict__[name.replace(type, 'high')]
            other_spin.setMinimum(value + 1)
            range = (value, other_spin.value())
        elif type == 'high':
            other_spin = self.ui.__dict__[name.replace(type, 'low')]
            other_spin.setMaximum(value - 1)
            range = (other_spin.value(), value)

        self.move_gen.__dict__[variable] = range

    def other_param_changed(self, value):
        for param in self.other_params:
            if param[0] == self.sender():
                variable = param[1]

        self.move_gen.__dict__[variable] = value

    # True for moving, False for stopped
    def set_state(self, state: bool):
        self.ui.button_start.setEnabled(1 - state)
        self.ui.button_stop.setEnabled(state)
        # TODO

    def start(self):
        self.ui.button_start.setEnabled(False)
        self.ui.button_stop.setEnabled(True)
        for radio in self.radios.keys():
            radio.setEnabled(False)
        self.move_gen.set_ranges(*self.zone.calculate_available_zone())
        self.move_gen.restart_movement()
        self.timer.timeout.connect(self.movement)
        self.timer.start(int(p.PERIOD * 1000))

    def stop(self):
        self.ui.button_start.setEnabled(True)
        self.ui.button_stop.setEnabled(False)
        for radio in self.radios.keys():
            radio.setEnabled(True)
        self.timer.stop()
        self.timer.disconnect()

    def random_step(self):
        print("random step")
        dist_cm = self.ui.doubleSpinBox_randomStepDist.value()
        self.zone.ref_pos = self.move_gen.random_step(
            self.zone.ref_pos, dist_cm)
        self.zone.update()

    def movement(self):
        self.zone.ref_pos = self.move_gen.move(self.zone.ref_pos)
        self.zone.update()

    def resizeEvent(self, _):
        self.move_gen.set_ranges(*self.zone.calculate_available_zone())
        self.update_vel_dist()

    def resize_point(self):
        size = self.ui.spin_size.value()
        self.zone.point_rad = size
        self.zone.update()
        self.move_gen.set_ranges(*self.zone.calculate_available_zone())

    def update_vel_dist(self):
        vel = self.ui.spin_vel.value()
        #dist_cm = self.ui.spin_dist.value()
        dpi = QMainWindow().screen().physicalDotsPerInch()
        dist_pix = self.zone.calculata_dist_pix()
        dist_cm = dist_pix*(2.54/dpi)
        self.move_gen.set_vel_dist(vel, dist_cm, dist_pix)
        self.move_gen.set_ranges(*self.zone.calculate_available_zone())

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu(self)
        action_show = QAction("Show Controls")
        action_hide = QAction("Hide Controls")
        action_full = QAction("Show Fullscreen")
        action_not_full = QAction("Show Normal")
        actions = (action_show, action_hide, action_full, action_not_full)
        for action in actions:
            action.triggered.connect(self.resizeEvent)

        if self.isFullScreen():
            menu.addAction(action_not_full)
        else:
            menu.addAction(action_full)

        if self.ui.dockWidget.isHidden():
            menu.addAction(action_show)
        else:
            menu.addAction(action_hide)

        action_show.triggered.connect(self.ui.dockWidget.show)
        action_hide.triggered.connect(self.ui.dockWidget.hide)
        action_full.triggered.connect(self.showFullScreen)
        action_not_full.triggered.connect(self.showNormal)
        action_full.triggered.connect(self.reset_pos)
        action_not_full.triggered.connect(self.reset_pos)
        menu.exec(self.mapToGlobal(event.pos()))

    def reset_pos(self):
        self.zone.ref_pos = [200, 200]
