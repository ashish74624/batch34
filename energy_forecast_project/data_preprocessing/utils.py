from django.conf import settings
import pandas as pd

# Fix for the 'consumptions' DataFrame
consumptions = pd.read_csv(
    settings.RAW_ENERGY_DATA, 
    sep=';',  # keyword argument for separator
    header=0,  # explicit positional argument
    na_values='?', 
    dtype={'Date': str, 'Time': str, 'Global_active_power': float}, 
    infer_datetime_format=False
)

# Fix for the 'french_holidays_df' DataFrame
french_holidays_df = pd.read_csv(
    settings.RAW_HOLIDAYS_DATA,
    parse_dates=['date']  # keyword argument
)

# Fix for the weather data directory
data_directory = settings.RAW_WEATHER_DIR
