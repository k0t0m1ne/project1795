import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkinter import colorchooser
import matplotlib.pyplot as plt


class GraphPlotterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vizualization")
        self.geometry("350x600")
        self.csv_file = ""
        self.graph_settings = {
            "AoI vs D": {"csv": "metrics_distance.csv", "selected": tk.BooleanVar(value=False), "x": "region_max_distance", "y": "mean_aoi",
                         "xlim0": tk.DoubleVar(value=0), "xlim1": tk.DoubleVar(value=1000),
                         "ylim0": tk.DoubleVar(value=0), "ylim1": tk.DoubleVar(value=2),
                         "width": tk.DoubleVar(value=5), "height": tk.DoubleVar(value=5), "color": 'blue', "markers": 'None'},
            "CLR vs D": {"csv": "metrics_distance.csv", "selected": tk.BooleanVar(value=False), "x": "region_max_distance", "y": "CLR",
                         "xlim0": tk.DoubleVar(value=0), "xlim1": tk.DoubleVar(value=1000),
                         "ylim0": tk.DoubleVar(value=0), "ylim1": tk.DoubleVar(value=2),
                         "width": tk.DoubleVar(value=5), "height": tk.DoubleVar(value=5), "color": 'green', "markers": 'None'},
            "PAoI vs D": {"csv": "metrics_distance.csv", "selected": tk.BooleanVar(value=False), "x": "region_max_distance", "y": "mean_paoi",
                          "xlim0": tk.DoubleVar(value=0), "xlim1": tk.DoubleVar(value=1000),
                         "ylim0": tk.DoubleVar(value=0), "ylim1": tk.DoubleVar(value=2),
                         "width": tk.DoubleVar(value=5), "height": tk.DoubleVar(value=5), "color": 'red', "markers": 'None'},
            "PDR vs D": {"csv": "metrics_distance.csv", "selected": tk.BooleanVar(value=False), "x": "region_max_distance", "y": "PDR",
                         "xlim0": tk.DoubleVar(value=0), "xlim1": tk.DoubleVar(value=1000),
                         "ylim0": tk.DoubleVar(value=0), "ylim1": tk.DoubleVar(value=2),
                         "width": tk.DoubleVar(value=5), "height": tk.DoubleVar(value=5), "color": 'red', "markers": 'None'},
            "PLR vs D": {"csv": "metrics_distance.csv", "selected": tk.BooleanVar(value=False), "x": "region_max_distance", "y": "PLR",
                         "xlim0": tk.DoubleVar(value=0), "xlim1": tk.DoubleVar(value=1000),
                         "ylim0": tk.DoubleVar(value=0), "ylim1": tk.DoubleVar(value=2),
                         "width": tk.DoubleVar(value=5), "height": tk.DoubleVar(value=5), "color": 'red', "markers": 'None'},
            "PDR vs PLR": {"csv": "metrics_distance.csv", "selected": tk.BooleanVar(value=False), "x": "PLR", "y": "PDR",
                           "xlim0": tk.DoubleVar(value=0), "xlim1": tk.DoubleVar(value=1),
                         "ylim0": tk.DoubleVar(value=0), "ylim1": tk.DoubleVar(value=1),
                         "width": tk.DoubleVar(value=5), "height": tk.DoubleVar(value=5), "color": 'red', "markers": 'None'},
            "AoI vs PKeep": {"csv": "avg_metrics_parameter.csv", "selected": tk.BooleanVar(value=False), "x": "var_parameter", "y": "mean_aoi",
                             "xlim0": tk.DoubleVar(value=0), "xlim1": tk.DoubleVar(value=1),
                         "ylim0": tk.DoubleVar(value=0), "ylim1": tk.DoubleVar(value=1),
                         "width": tk.DoubleVar(value=5), "height": tk.DoubleVar(value=5), "color": 'blue',
                             "markers": 'None'},
            "CLR vs PKeep": {"csv": "avg_metrics_parameter.csv", "selected": tk.BooleanVar(value=False), "x": "var_parameter", "y": "CLR",
                             "xlim0": tk.DoubleVar(value=0), "xlim1": tk.DoubleVar(value=1),
                         "ylim0": tk.DoubleVar(value=0), "ylim1": tk.DoubleVar(value=1),
                         "width": tk.DoubleVar(value=5), "height": tk.DoubleVar(value=5), "color": 'green',
                             "markers": 'None'},
            "PAoI vs PKeep": {"csv": "avg_metrics_parameter.csv", "selected": tk.BooleanVar(value=False), "x": "var_parameter", "y": "mean_paoi",
                              "xlim0": tk.DoubleVar(value=0), "xlim1": tk.DoubleVar(value=1),
                         "ylim0": tk.DoubleVar(value=0),    "ylim1": tk.DoubleVar(value=1),
                         "width": tk.DoubleVar(value=5), "height": tk.DoubleVar(value=5), "color": 'red',
                              "markers": 'None'},
            "PDR vs PKeep": {"csv": "avg_metrics_parameter.csv", "selected": tk.BooleanVar(value=False), "x": "var_parameter", "y": "PDR",
                             "xlim0": tk.DoubleVar(value=0), "xlim1": tk.DoubleVar(value=1),
                         "ylim0": tk.DoubleVar(value=0), "ylim1": tk.DoubleVar(value=1),
                         "width": tk.DoubleVar(value=5), "height": tk.DoubleVar(value=5), "color": 'red',
                             "markers": 'None'},
            "PLR vs PKeep": {"csv": "avg_metrics_parameter.csv", "selected": tk.BooleanVar(value=False), "x": "var_parameter", "y": "PLR", "xlim0": tk.DoubleVar(value=0), "xlim1": tk.DoubleVar(value=1),
                         "ylim0": tk.DoubleVar(value=0), "ylim1": tk.DoubleVar(value=1),
                         "width": tk.DoubleVar(value=5), "height": tk.DoubleVar(value=5), "color": 'red',
                             "markers": 'None'},
        }

        self.init_ui()

    def init_ui(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        self.graph_frame = ttk.Frame(self.main_frame)
        self.graph_frame.pack(fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.graph_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.canvas = tk.Canvas(self.graph_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        self.graph_inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.graph_inner_frame, anchor="nw")

        self.graph_inner_frame.bind("<Configure>",
                                    lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        plot_button = ttk.Button(self.main_frame, text="Построить выбранные графики",
                                 command=self.plot_selected_graphs)
        plot_button.pack(side="top", padx=10, pady=10)

        for graph_name, settings in self.graph_settings.items():
            graph_label_frame = ttk.LabelFrame(self.graph_inner_frame, text=graph_name)
            graph_label_frame.pack(fill="x", padx=10, pady=5, anchor="nw")

            checkbox = ttk.Checkbutton(graph_label_frame, text="Построить", variable=settings["selected"])
            checkbox.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            settings["checkbox"] = checkbox

            ttk.Label(graph_label_frame, text="Маркер:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            marker_combobox = ttk.Combobox(graph_label_frame, values=['None','o', '.', 'x', 's'], state="readonly", width=6)
            marker_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
            marker_combobox.set(settings["markers"])
            settings["marker_combobox"] = marker_combobox

            ttk.Label(graph_label_frame, text="Цвет:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
            color_button = ttk.Button(graph_label_frame, text="Выбрать цвет",
                                      command=lambda graph=graph_name: self.choose_color(graph))
            color_button.grid(row=2, column=1, padx=0, pady=5, sticky="w")
            settings["color_button"] = color_button

            self.create_setting_input(graph_label_frame, "Ширина:", settings["width"], 3, 0, settings)
            self.create_setting_input(graph_label_frame, "Высота:", settings["height"], 3, 2, settings)
            self.create_setting_input(graph_label_frame, "Xlim от:", settings["xlim0"], 5, 0, settings)
            self.create_setting_input(graph_label_frame, "до:", settings["xlim1"], 5, 2, settings)
            self.create_setting_input(graph_label_frame, "Ylim от:", settings["ylim0"], 6, 0, settings)
            self.create_setting_input(graph_label_frame, "до:", settings["ylim1"], 6, 2, settings)

    def create_setting_input(self, parent_frame, label_text, setting_var, row, column, settings):
        ttk.Label(parent_frame, text=label_text).grid(row=row, column=column, padx=5, pady=5, sticky="w")
        setting_spinbox = ttk.Spinbox(parent_frame, from_=0, to=1000.00, increment=1, width=5,
                                      textvariable=setting_var)
        setting_spinbox.grid(row=row, column=column + 1, padx=5, pady=5, sticky="w")
        setting_spinbox.bind("<FocusOut>",
                             lambda event, var=setting_var, setting=settings: self.update_setting(event, var,
                                                                                                  setting))
        settings[f"{label_text.lower()}_spinbox"] = setting_spinbox

    def update_setting(self, event, var, setting):
        new_value = float(var.get())
        setting[var._name] = new_value
    def choose_color(self, graph_name):
        color = colorchooser.askcolor()[1]
        if color:
            self.graph_settings[graph_name]["color"] = color

    def plot_selected_graphs(self):
        for kpi_name, settings in self.graph_settings.items():
            if settings["selected"].get():
                df = pd.read_csv(settings["csv"], delimiter=',')
                fig = plt.figure(kpi_name, figsize=(settings["width"].get(), settings["height"].get()))

                x = df[settings["x"]]
                y = df[settings["y"]]
                plt.plot(x, y, label=kpi_name, color=settings["color"], marker=settings["marker_combobox"].get(),
                         markersize=7)
                plt.title(label=kpi_name)
                plt.grid()
                plt.legend()
                plt.xlim(settings["xlim0"].get(), settings["xlim1"].get())
                plt.ylim(settings["ylim0"].get(), settings["ylim1"].get())
                plt.xlabel(settings["x"])
                plt.ylabel(settings["y"])
                name_of_file = f'visualisations/{settings["csv"].replace(".csv", "")}_{kpi_name.replace(" ", "_")}'
                plt.savefig(f'{name_of_file}.eps')
                plt.savefig(f'{name_of_file}.png')
                plt.show()


app = GraphPlotterApp()
app.mainloop()


