from datetime import datetime, timedelta
from django.http import JsonResponse
import json
import os
import pandas as pd
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .src.models.short_term_energy_model import ShortTermEnergyModel
from .src.models.long_term_energy_model import LongTermEnergyModel
from datetime import datetime, timedelta
import subprocess

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
        date = data.get("date")
        action = data.get("action")

        if not date:
            return JsonResponse({"error": "Date is required"}, status=400)

        # Map the input date to a specified range
        mapped_date = map_date_to_range(date, "2009-05-17", "2010-05-17")

        try:
            if action == "generate_data":
                subprocess.run(["python", r"C:\Users\ashis\OneDrive\Desktop\Monthly-Daily-Energy-Forecasting-Docker-API\notebooks\eda-2.py"], check=True)
            elif action == "see_graph":
                subprocess.run(["python", r"C:\Users\ashis\OneDrive\Desktop\Monthly-Daily-Energy-Forecasting-Docker-API\notebooks\mm.py"], check=True)
        except subprocess.CalledProcessError as e:
            return JsonResponse({"error": f"Error executing script: {e}"}, status=500)

        # Load the data
        data_path = os.path.join(settings.BASE_DIR, "data/processed/weather_and_consumption.csv")
        df = pd.read_csv(data_path, index_col=0, parse_dates=True)

        # Initialize models
        short_term_model = ShortTermEnergyModel(df)
        long_term_model = LongTermEnergyModel(df)

        # Predict for the mapped date and 4 additional days
        # input_date = datetime.strptime(mapped_date, "%Y-%m-%d")
        # date_range = [(input_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]

        # Generate the input date and extra 4 days
        input_date_obj = datetime.strptime(mapped_date, "%Y-%m-%d")
        extra_dates = [input_date_obj + timedelta(days=i) for i in range(5)]

        # # Generate short-term predictions for these dates
        # short_term_predictions = [
        #     {"date": d, "price": short_term_model.predict_for_date(d)}
        #     for d in date_range
        # ]

        short_term_predictions = []
        for extra_date in extra_dates:
            formatted_date = extra_date.strftime("%Y-%m-%d")
            price = short_term_model.predict_for_date(formatted_date)
            short_term_predictions.append({"date": formatted_date, "price": price})
        
        # Long-term prediction for the mapped date
        long_term_prediction = long_term_model.predict_for_date(mapped_date)

        return JsonResponse({
            "mapped_date": mapped_date,
            "short_term_predictions": short_term_predictions,
            "long_term_prediction": long_term_prediction,
        })

    return JsonResponse({"error": "Invalid request method"}, status=405)
