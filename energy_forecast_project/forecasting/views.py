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
    show_generate_button = True
    show_graph_button = False
    date = None  # Store the date entered by the user

    if request.method == 'POST':
        action = request.POST.get('action')
        date = request.POST.get('date')  # Retrieve the date from the POST request
        data_path = os.path.join(settings.BASE_DIR, 'data/processed/weather_and_consumption.csv')
        df = pd.read_csv(data_path, index_col=0, parse_dates=True)

        if action == 'generate_data':
            # Execute the augmentation script
            try:
                subprocess.run(["python", r"C:\Users\ashis\OneDrive\Desktop\Monthly-Daily-Energy-Forecasting-Docker-API\notebooks\eda-2.py"], check=True)
                show_generate_button = False
                show_graph_button = True
            except subprocess.CalledProcessError as e:
                print(f"Error while executing 'a.py': {e}")

        elif action == 'see_graph':
            # Execute the graph generation script
            try:
                subprocess.run(["python", r"C:\Users\ashis\OneDrive\Desktop\Monthly-Daily-Energy-Forecasting-Docker-API\notebooks\mm.py"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error while executing 'b.py': {e}")

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
            'long_term_prediction': long_term_prediction,
            'show_generate_button': show_generate_button,
            'show_graph_button': show_graph_button,
            'date': date,  # Pass the date to the template
        }
    )
