from django.shortcuts import render
from .src.models.short_term_energy_model import ShortTermEnergyModel
from .src.models.long_term_energy_model import LongTermEnergyModel
import os
import pandas as pd
from django.conf import settings


def forecast_view(request):
    prediction = None
    if request.method == 'POST':
        date = request.POST.get('date')
        model_choice = request.POST.get('model')
        data_path = os.path.join(settings.BASE_DIR, 'data/processed/weather_and_consumption.csv')
        df = pd.read_csv(data_path, index_col=0, parse_dates=True)

        if model_choice == 'short':
            model = ShortTermEnergyModel(df)
        elif model_choice == 'long':
            model = LongTermEnergyModel(df)
        else:
            model = None

        if model:
            prediction = model.predict_for_date(date)
    
    return render(request, 'forecasting/forecast.html', {'prediction': prediction})
