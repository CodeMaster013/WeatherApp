import tkinter as tk
from meteostat import Stations, Daily
import meteostat
import datetime
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class WeatherApp:
    def __init__(self, root):
        self.root = root

        self.label_station = tk.Label(root, text="Station:")
        self.label_station.pack()

        self.text_station = tk.Text(root, height=1, width=20)
        self.text_station.pack()

        self.label_temperature = tk.Label(root, text="Temperature:")
        self.label_temperature.pack()

        self.text_temperature = tk.Text(root, height=1, width=20)
        self.text_temperature.pack()

        self.label_precipitation = tk.Label(root, text="Precipitation:")
        self.label_precipitation.pack()

        self.text_precipitation = tk.Text(root, height=1, width=20)
        self.text_precipitation.pack()

        self.label_humidity = tk.Label(root, text="Humidity:")
        self.label_humidity.pack()

        self.text_humidity = tk.Text(root, height=1, width=20)
        self.text_humidity.pack()

        self.label_wind_speed = tk.Label(root, text="Wind Speed:")
        self.label_wind_speed.pack()

        self.text_wind_speed = tk.Text(root, height=1, width=20)
        self.text_wind_speed.pack()

        self.frame_graphs = tk.Frame(root)
        self.frame_graphs.pack()

        self.figure_temperature = Figure(figsize=(5, 4), dpi=100)
        self.axes_temperature = self.figure_temperature.add_subplot(111)
        self.canvas_temperature = FigureCanvasTkAgg(self.figure_temperature, master=self.frame_graphs)
        self.canvas_temperature.draw()
        self.canvas_temperature.get_tk_widget().pack(side=tk.LEFT)

        self.figure_precipitation = Figure(figsize=(5, 4), dpi=100)
        self.axes_precipitation = self.figure_precipitation.add_subplot(111)
        self.canvas_precipitation = FigureCanvasTkAgg(self.figure_precipitation, master=self.frame_graphs)
        self.canvas_precipitation.draw()
        self.canvas_precipitation.get_tk_widget().pack(side=tk.LEFT)

        self.figure_humidity = Figure(figsize=(5, 4), dpi=100)
        self.axes_humidity = self.figure_humidity.add_subplot(111)
        self.canvas_humidity = FigureCanvasTkAgg(self.figure_humidity, master=self.frame_graphs)
        self.canvas_humidity.draw()
        self.canvas_humidity.get_tk_widget().pack(side=tk.LEFT)

        self.figure_wind_speed = Figure(figsize=(5, 4), dpi=100)
        self.axes_wind_speed = self.figure_wind_speed.add_subplot(111)
        self.canvas_wind_speed = FigureCanvasTkAgg(self.figure_wind_speed, master=self.frame_graphs)
        self.canvas_wind_speed.draw()
        self.canvas_wind_speed.get_tk_widget().pack(side=tk.LEFT)

        self.fetch_data()

    def fetch_data(self):
        try:
            stations = meteostat.Stations()
            stations = stations.nearby(29.2108, -81.0226)  # Daytona Beach, FL
            station = stations.fetch(1)  # fetch the first station
            station_name = station.name

            self.text_station.config(state='normal')
            self.text_station.delete(1.0, "end")
            self.text_station.insert("end", station_name)
            self.text_station.config(state='disabled')

            data = Daily(station, start=datetime.datetime(2021, 1, 1), end=datetime.datetime(2022, 1, 1))
            data = data.fetch()
            data = data.sort_index(ascending=False)

            self.data = data

            self.axes_temperature.plot(data.index, data.temp)
            self.axes_precipitation.plot(data.index, data.prcp)
            self.axes_humidity.plot(data.index, data.rhum)
            self.axes_wind_speed.plot(data.index, data.wspd)

            self.canvas_temperature.draw()
            self.canvas_precipitation.draw()
            self.canvas_humidity.draw()
            self.canvas_wind_speed.draw()

        except Exception as e:
            print(e)

root = tk.Tk()
app = WeatherApp(root)
root.mainloop()
