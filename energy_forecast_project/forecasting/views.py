import json
from datetime import datetime, timedelta
from django.http import JsonResponse
import subprocess
import os
import pandas as pd
from django.conf import settings
from .src.models.short_term_energy_model import ShortTermEnergyModel
from .src.models.long_term_energy_model import LongTermEnergyModel
from django.views.decorators.csrf import csrf_exempt


def map_date_to_range(input_date, start_date, end_date):
    """
    Maps any date to the range between start_date and end_date.
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    range_days = (end_date - start_date).days + 1  # Include both ends

    input_date = datetime.strptime(input_date, "%Y-%m-%d")
    days_since_start = (input_date - start_date).days
    mapped_days = days_since_start % range_days

    mapped_date = start_date + timedelta(days=mapped_days)
    return mapped_date.strftime("%Y-%m-%d")


@csrf_exempt
def forecast_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")
        date = data.get("date")

        if not date:
            return JsonResponse({"error": "Date is required"}, status=400)

        # Map the input date to the specified range
        mapped_date = map_date_to_range(date, "2009-05-17", "2010-05-17")

        # Execute the appropriate script based on action
        try:
            if action == "generate_data":
                subprocess.run(["python", r"C:\Users\ashis\OneDrive\Desktop\Monthly-Daily-Energy-Forecasting-Docker-API\notebooks\eda-2.py"], check=True)
            elif action == "see_graph":
                subprocess.run(["python", r"C:\Users\ashis\OneDrive\Desktop\Monthly-Daily-Energy-Forecasting-Docker-API\notebooks\mm.py"], check=True)
        except subprocess.CalledProcessError as e:
            return JsonResponse({"error": f"Error executing script: {e}"}, status=500)

        data_path = os.path.join(settings.BASE_DIR, r"C:\Users\ashis\OneDrive\Desktop\Monthly-Daily-Energy-Forecasting-Docker-API\data\processed\weather_and_consumption.csv")
        df = pd.read_csv(data_path, index_col=0, parse_dates=True)

        # Short-term prediction
        short_term_model = ShortTermEnergyModel(df)
        short_term_prediction = short_term_model.predict_for_date(mapped_date)

        # Long-term prediction
        long_term_model = LongTermEnergyModel(df)
        long_term_prediction = long_term_model.predict_for_date(mapped_date)

        return JsonResponse({
            "mapped_date": mapped_date,
            "short_term_prediction": short_term_prediction,
            "long_term_prediction": long_term_prediction,
        })
    return JsonResponse({"error": "Invalid request method"}, status=405)
