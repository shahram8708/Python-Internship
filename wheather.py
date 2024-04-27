import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Forecast App")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.api_key = "API_Key" 

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Weather Forecast", font=("Helvetica", 24, "bold"), pady=10)
        self.title_label.pack()

        self.city_frame = tk.Frame(self.root)
        self.city_frame.pack(pady=5)

        self.city_label = tk.Label(self.city_frame, text="Enter city name:", font=("Helvetica", 14))
        self.city_label.pack(side=tk.LEFT)

        self.city_entry = tk.Entry(self.city_frame, font=("Helvetica", 14), width=30)
        self.city_entry.pack(side=tk.LEFT, padx=5)

        self.unit_label = tk.Label(self.root, text="Select unit:", font=("Helvetica", 14))
        self.unit_label.pack(pady=5)

        self.unit_var = tk.StringVar()
        self.unit_combobox = ttk.Combobox(self.root, textvariable=self.unit_var, font=("Helvetica", 14), state="readonly", width=10)
        self.unit_combobox['values'] = ('Celsius', 'Fahrenheit')
        self.unit_combobox.current(0)
        self.unit_combobox.pack()

        self.get_weather_button = tk.Button(self.root, text="Get Weather", font=("Helvetica", 14), command=self.get_weather)
        self.get_weather_button.pack(pady=10)

        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(pady=10)

        self.result_label = tk.Label(self.result_frame, text="", font=("Helvetica", 14), justify="left")
        self.result_label.pack()

    def get_weather(self):
        city = self.city_entry.get()
        unit = self.unit_var.get().lower()
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units={unit}"

        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                temperature = data['main']['temp']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                description = data['weather'][0]['description']
                city_name = data['name']
                country_code = data['sys']['country']

                result_text = f"Weather for {city_name}, {country_code}:\n"
                result_text += f"Temperature: {temperature}°{unit.upper()}\n"
                result_text += f"Humidity: {humidity}%\n"
                result_text += f"Wind Speed: {wind_speed} m/s\n"
                result_text += f"Description: {description.capitalize()}"

                self.result_label.config(text=result_text)
            else:
                error_message = data['message']
                messagebox.showerror("Error", f"Error: {error_message}")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching weather data: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
