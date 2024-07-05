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

        # Labels and Text Boxes for Station Information
        self.label_station = tk.Label(root, text="Station:")
        self.label_station.pack()

        self.text_station = tk.Text(root, height=1, width=20, state='disabled')  # Start disabled
        self.text_station.pack()

        # Labels and Text Boxes for Weather Data
        self.label_temperature = tk.Label(root, text="Temperature:")
        self.label_temperature.pack()

        self.text_temperature = tk.Text(root, height=1, width=20, state='disabled')
        self.text_temperature.pack()

        self.label_precipitation = tk.Label(root, text="Precipitation:")
        self.label_precipitation.pack()

        self.text_precipitation = tk.Text(root, height=1, width=20, state='disabled')
        self.text_precipitation.pack()

        self.label_humidity = tk.Label(root, text="Humidity:")
        self.label_humidity.pack()

        self.text_humidity = tk.Text(root, height=1, width=20, state='disabled')
        self.text_humidity.pack()

        self.label_wind_speed = tk.Label(root, text="Wind Speed:")
        self.label_wind_speed.pack()

        self.text_wind_speed = tk.Text(root, height=1, width=20, state='disabled')
        self.text_wind_speed.pack()

        # Frame for graphs
        self.frame_graphs = tk.Frame(root)
        self.frame_graphs.pack()

        # Initialize Figure and Axes for each graph
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

            # Update text boxes with latest data
            if 'temp' in data.columns:
                self.text_temperature.config(state='normal')
                self.text_temperature.delete(1.0, "end")
                self.text_temperature.insert("end", f"{data.temp.iloc[0]:.2f} °C")
                self.text_temperature.config(state='disabled')
            else:
                print("Temperature data not available for this station.") 

            if 'prcp' in data.columns:
                self.text_precipitation.config(state='normal')
                self.text_precipitation.delete(1.0, "end")
                self.text_precipitation.insert("end", f"{data.prcp.iloc[0]:.2f} mm")
                self.text_precipitation.config(state='disabled')
            else:
                    print("Precipitation data not available for this station.") 

            if 'rhum' in data.columns:
                self.text_humidity.config(state='normal')
                self.text_humidity.delete(1.0, "end")
                self.text_humidity.insert("end", f"{data.rhum.iloc[0]:.2f} %")
                self.text_humidity.config(state='disabled')
            else:
                print("Humidity data not available for this station.") 

            if 'wspd' in data.columns:
                self.text_wind_speed.config(state='normal')
                self.text_wind_speed.delete(1.0, "end")
                self.text_wind_speed.insert("end", f"{data.wspd.iloc[0]:.2f} m/s")
                self.text_wind_speed.config(state='disabled')
            else:
                print("Wind speed data not available for this station.") 

            # Plot data
            if 'temp' in data.columns:
                self.axes_temperature.plot(data.index, data.temp)
                self.canvas_temperature.draw()
            else:
                print("Temperature data not available for this station.") 

            if 'prcp' in data.columns:
                self.axes_precipitation.plot(data.index, data.prcp)
                self.canvas_precipitation.draw()
            else:
                print("Precipitation data not available for this station.") 

            if 'rhum' in data.columns:
                self.axes_humidity.plot(data.index, data.rhum)
                self.canvas_humidity.draw()
            else:
                print("Humidity data not available for this station.") 

            if 'wspd' in data.columns:
                self.axes_wind_speed.plot(data.index, data.wspd)
                self.canvas_wind_speed.draw()
            else:
                print("Wind speed data not available for this station.") 

        except Exception as e:
            print(e)

root = tk.Tk()
app = WeatherApp(root)
root.mainloop()
