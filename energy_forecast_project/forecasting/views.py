from django.shortcuts import render
from .src.models.short_term_energy_model import ShortTermEnergyModel
from .src.models.long_term_energy_model import LongTermEnergyModel
import os
import pandas as pd
from django.conf import settings
import subprocess

def forecast_view(request):
    short_term_prediction = None
    long_term_prediction = None
    
    if request.method == 'POST':
        date = request.POST.get('date')
        data_path = os.path.join(settings.BASE_DIR, 'data/processed/weather_and_consumption.csv')
        df = pd.read_csv(data_path, index_col=0, parse_dates=True)

        # Execute external scripts
        try:
            subprocess.run(["python", r"C:\Users\ashis\OneDrive\Desktop\Monthly-Daily-Energy-Forecasting-Docker-API\notebooks\a.py"], check=True)
            subprocess.run(["python", r"C:\Users\ashis\OneDrive\Desktop\Monthly-Daily-Energy-Forecasting-Docker-API\notebooks\b.py"], check=True)
            subprocess.run(["python", r"C:\Users\ashis\OneDrive\Desktop\Monthly-Daily-Energy-Forecasting-Docker-API\notebooks\m.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while executing scripts: {e}")

        # Short-term prediction
        short_term_model = ShortTermEnergyModel(df)
        short_term_prediction = short_term_model.predict_for_date(date)

        # Long-term prediction
        long_term_model = LongTermEnergyModel(df)
        long_term_prediction = long_term_model.predict_for_date(date)

    return render(
        request,
        'forecasting/forecast.html',
        {
            'short_term_prediction': short_term_prediction,
            'long_term_prediction': long_term_prediction
        }
    )
