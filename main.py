import sys

import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QSpinBox, QColorDialog, QPushButton, \
    QCheckBox, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class GraphPlotterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle("Vizualization")
        self.setGeometry(100, 100, 500, 350)
        self.graph_settings = {
            "AoI vs D": {"csv": "Matrix_RC515.csv", "selected": False, "x": "region_value", "y": "value_aoi",
                         "width": 5, "height": 5, "color": 'blue', "markers": 5},
            "CLR vs D": {"csv": "Matrix_RC515.csv", "selected": False, "x": "region_value", "y": "value_clr",
                         "width": 5, "height": 5, "color": 'green', "markers": 5},
            "PAoI vs D": {"csv": "Matrix_RC515.csv", "selected": False, "x": "region_value", "y": "value_paoi",
                          "width": 5, "height": 5, "color": 'red', "markers": 5},
            "PDR vs D": {"csv": "Matrix_RC515.csv", "selected": False, "x": "region_value", "y": "value_pdr",
                         "width": 5, "height": 5, "color": 'red', "markers": 5},
            "PLR vs D": {"csv": "Matrix_RC515.csv", "selected": False, "x": "region_value", "y": "value_plr",
                         "width": 5, "height": 5, "color": 'red', "markers": 5},
            "PDR vs PLR": {"csv": "Matrix_RC515.csv", "selected": False, "x": "value_plr", "y": "value_pdr", "width": 5,
                           "height": 5, "color": 'red', "markers": 5},
            "AoI vs PKeep": {"csv": "Average_aoi.csv", "selected": False, "x": "pkeep", "y": "average_aoi", "width": 5,
                             "height": 5, "color": 'blue',
                             "markers": 5},
            "CLR vs PKeep": {"csv": "Average_clr.csv", "selected": False, "x": "pkeep", "y": "average_clr", "width": 5,
                             "height": 5, "color": 'green',
                             "markers": 5},
            "PAoI vs PKeep": {"csv": "Average_paoi.csv", "selected": False, "x": "pkeep", "y": "average_paoi",
                              "width": 5, "height": 5, "color": 'red',
                              "markers": 5},
            "PDR vs PKeep": {"csv": "Average_pdr.csv", "selected": False, "x": "pkeep", "y": "average_pdr", "width": 5,
                             "height": 5, "color": 'red',
                             "markers": 5},
            "PLR vs PKeep": {"csv": "Average_plr.csv", "selected": False, "x": "pkeep", "y": "average_plr", "width": 5,
                             "height": 5, "color": 'red',
                             "markers": 5},
        }

        self.init_ui()

    def init_ui(self):
        # Создаем графический виджет

        # Создаем элементы управления
        self.graph_selectors = {}
        self.checkbox_layout = QVBoxLayout()

        for graph_name, settings in self.graph_settings.items():
            checkbox = QCheckBox(graph_name)
            checkbox.setChecked(settings["selected"])
            checkbox.stateChanged.connect(lambda state, name=graph_name: self.toggle_graph_checkbox(state, name))
            self.graph_selectors[graph_name] = checkbox

            settings_layout = self.create_settings_layout(graph_name)
            self.checkbox_layout.addWidget(checkbox)
            self.checkbox_layout.addLayout(settings_layout)

        plot_button = QPushButton("Построить выбранные графики")
        plot_button.clicked.connect(self.plot_selected_graphs)

        # Создаем компоновку для элементов управления
        control_layout = QVBoxLayout()
        control_layout.addLayout(self.checkbox_layout)
        control_layout.addWidget(plot_button)

        # Создаем основную компоновку
        main_layout = QVBoxLayout()
        main_layout.addLayout(control_layout)

        # Устанавливаем компоновку для окна
        self.setLayout(main_layout)

    def create_settings_layout(self, graph_name):
        settings_layout = QHBoxLayout()

        width_spinbox = QSpinBox()
        width_spinbox.setRange(1, 2000)
        width_spinbox.setValue(self.graph_settings[graph_name]["width"])
        width_spinbox.valueChanged.connect(
            lambda value, name=graph_name: self.update_graph_settings(name, "width", value))

        height_spinbox = QSpinBox()
        height_spinbox.setRange(1, 2000)
        height_spinbox.setValue(self.graph_settings[graph_name]["height"])
        height_spinbox.valueChanged.connect(
            lambda value, name=graph_name: self.update_graph_settings(name, "height", value))

        color_button = QPushButton("Выбрать цвет")
        color_button.clicked.connect(lambda name=graph_name: self.choose_color(name))

        markers_spinbox = QSpinBox()
        markers_spinbox.setRange(0, 100)
        markers_spinbox.setValue(self.graph_settings[graph_name]["markers"])
        markers_spinbox.valueChanged.connect(
            lambda value, name=graph_name: self.update_graph_settings(name, "markers", value))

        settings_layout.addWidget(QLabel("Ширина:"))
        settings_layout.addWidget(width_spinbox)
        settings_layout.addWidget(QLabel("Высота:"))
        settings_layout.addWidget(height_spinbox)

        settings_layout.addWidget(color_button)
        settings_layout.addWidget(QLabel("Маркеры:"))
        settings_layout.addWidget(markers_spinbox)

        return settings_layout

    def choose_color(self, graph_name):
        color = QColorDialog.getColor()
        if color.isValid():
            self.graph_settings[graph_name]["color"] = color.name()

    def toggle_graph_checkbox(self, state, graph_name):
        self.graph_settings[graph_name]["selected"] = state == 2

    def update_graph_settings(self, graph_name, setting_name, value):
        self.graph_settings[graph_name][setting_name] = value

    def plot_selected_graphs(self):

        # Строим выбранные графики
        for kpi_name, kpi in self.graph_settings.items():
            df = pd.read_csv(kpi["csv"], delimiter=',')
            if kpi["selected"] == True:
                fig = plt.figure(kpi_name, figsize=(kpi["width"], kpi["height"]))

                x = df[kpi["x"]]
                y = df[kpi["y"]]
                plt.plot(x, y, label=kpi_name, color=kpi["color"], marker='o',
                         markersize=kpi["markers"])
                plt.grid()
                plt.legend()
                plt.xlabel(kpi["x"])
                plt.ylabel(kpi["y"])
                plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphPlotterApp()
    window.show()
    sys.exit(app.exec_())
