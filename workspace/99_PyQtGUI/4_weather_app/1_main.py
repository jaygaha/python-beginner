# Python Weather App
# Author: Jay Gaha

import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                            QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.city_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: Optima;
            }
            QLabel#city_label {
                font-size: 32px;
                font-style: italic;
            }
            QLineEdit#city_input {
                padding: 4px;
                font-size: 20px;
            }
            QPushButton#get_weather_button {
                padding: 8px;
                font-size: 20px;
                font-weight: bold;
            }
            QLabel#temperature_label {
                font-size: 42px;
            }
            QLabel#emoji_label {
                font-size: 54px;
                font-family: Apple Color Emoji;
            }
            QLabel#description_label {
                font-size: 32px;
            }
            """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "a69b2993d0ed2b28ed48c6114fc3b543"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\nPlease check your city name.")
                case 401:
                    self.display_error("Unauthorized:\nPlease check your API key.")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied.")
                case 404:
                    self.display_error("Not Found:\nCity not found.")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later.")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from server.")
                case 503:
                    self.display_error("Service Unavailable:\nServer is overloaded.")
                case 504:
                    self.display_error("Gateway Timeout:\nServer is taking too long to respond.")
                case _:
                    self.display_error("Unknown Error:\nPlease try again later.")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nPlease check your internet connection.")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nPlease try again later.")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects:\nPlease try again later.")
        except requests.exceptions.RequestException as req_error:
            self.display_error("Request Error:\nPlease try again later.")
            pass

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 24px; color: hsl(0, 100%, 50%);")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        """
        Convert weather data to displayable format.

        Args:
        data (dict): Weather data from OpenWeatherMap API
        """
        temperature_k = data["main"]["temp"]
        # Convert temperature to Kelvin
        temperature_c = (temperature_k - 273.15)
        # temperature_f = temperature_c * 9 / 5 + 32
        weather_description = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]

        temperature_hsl = self.temperature_to_hsl(temperature_c)
        self.temperature_label.setText(f"{temperature_c:.1f}°C")
        self.temperature_label.setStyleSheet(f"font-size: 42px; color: {temperature_hsl};")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌨️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "🌞"
        elif  801 <= weather_id <= 804:
            return "☁️"
        else:
            return "❓"

    @staticmethod
    def temperature_to_hsl(temperature):
        """
        Convert temperature to HSL color value.

        Args:
        temperature (float): Temperature in Celsius

        Returns:
        str: HSL color value
        """
        # Define temperature ranges
        cold_temp = 0
        cool_temp = 10
        mild_temp = 20
        warm_temp = 30
        hot_temp = 40

        # Map temperature to hue (0-360 degrees)
        if temperature <= cold_temp:
            # Deep blue for very cold temperatures
            hue = 240
        elif temperature <= cool_temp:
            # Gradient from blue to green for cool temperatures
            hue = 240 - (temperature - cold_temp) * (60 / (cool_temp - cold_temp))
        elif temperature <= mild_temp:
            # Gradient from green to yellow for mild temperatures
            hue = 180 - (temperature - cool_temp) * (60 / (mild_temp - cool_temp))
        elif temperature <= warm_temp:
            # Gradient from yellow to orange for warm temperatures
            hue = 60 - (temperature - mild_temp) * (30 / (warm_temp - mild_temp))
        elif temperature <= hot_temp:
            # Gradient from orange to red for hot temperatures
            hue = 30 - (temperature - warm_temp) * (30 / (hot_temp - warm_temp))
        else:
            # Deep red for very hot temperatures
            hue = 0

        # Adjust saturation based on temperature extremity
        if temperature <= cold_temp or temperature >= hot_temp:
            # Saturation is 100% for extreme temperatures
            saturation = 100
        else:
            # Moderate saturation for middle temperatures
            saturation = 80

        # Adjust lightness based on temperature
        if temperature <= cold_temp:
            lightness = 40
        elif temperature >= hot_temp:
            lightness = 50
        else:
            # Lighter for moderate temperatures
            lightness = 60

        # Return HSL color value
        return f"hsl({hue}, {saturation}%, {lightness}%)"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
