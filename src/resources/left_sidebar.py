from PyQt5.QtCore import Qt
from src.db.database_logic_objects import WeatherDbReader
from src.backend.styling import load_stylesheet
from src.resources.weather_widgets import CurrentTemp, CurrentIcon, SnowReport
from src.resources.base_containers import BaseVContainer, BaseHContainer
from src.resources.weather_forecast_widgets import WeatherForecastTable


class WeatherBar(BaseHContainer):
    left_icon: CurrentIcon = None
    right_temp: CurrentTemp = None

    def __init__(self, parent=None, todays_weather: dict = None):
        super(WeatherBar, self).__init__(parent)
        self.initUI(todays_weather=todays_weather)

    def initUI(self, todays_weather: dict):
        self.left_icon = CurrentIcon(parent=self, weather_icon_path=todays_weather.get("icon"))
        self.left_icon.setFixedWidth(int(self.config.get_width() * 0.15))
        self.left_icon.setIcon()
        self.right_temp = CurrentTemp(parent=self, cur_temp=todays_weather.get("temp"))
        self.right_temp.setFixedWidth(int(self.config.get_width() * 0.14))
        self.layout.addWidget(self.left_icon, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.right_temp, alignment=Qt.AlignHCenter)


class LeftSidebar(BaseVContainer):
    top_weather_bar: WeatherBar = None
    middle_snow_report: SnowReport = None
    bottom_weather_forecast: WeatherForecastTable = None
    weather_db_reader: WeatherDbReader = None

    def __init__(self, parent=None, resort: str = None):
        super(LeftSidebar, self).__init__(parent)
        self.weather_db_reader = WeatherDbReader(self.config.get_db_path())
        weather_info = self.weather_db_reader.get_weather_info(resort)
        self.initUI(weather_info=weather_info, resort=resort)

    def initUI(self, weather_info: dict, resort: str):
        self.top_weather_bar = WeatherBar(parent=self, todays_weather=weather_info.get('today'))
        self.middle_snow_report = SnowReport(report=weather_info.get("today").get("details"))
        self.bottom_weather_forecast = WeatherForecastTable(parent=self, forecast=weather_info.get('forecast'))
        self.top_weather_bar.setFixedHeight(int(self.config.get_height() * 0.22))
        self.middle_snow_report.setFixedHeight(int(self.config.get_height() * 0.28))
        self.bottom_weather_forecast.setFixedHeight(int(self.config.get_height() * 0.37))
        self.layout.addWidget(self.top_weather_bar, alignment=Qt.AlignTop)
        self.layout.addWidget(self.middle_snow_report, alignment=Qt.AlignVCenter)
        self.layout.addWidget(self.bottom_weather_forecast, alignment=Qt.AlignTop)
        self.setStyleSheet(load_stylesheet('weather_table.qss'))
