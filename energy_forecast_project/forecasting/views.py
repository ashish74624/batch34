import json
from django.http import JsonResponse
import subprocess
import os
import pandas as pd
from django.conf import settings
from .src.models.short_term_energy_model import ShortTermEnergyModel
from .src.models.long_term_energy_model import LongTermEnergyModel
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def forecast_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")
        date = data.get("date")

        if not date:
            return JsonResponse({"error": "Date is required"}, status=400)

        # Execute the appropriate script based on action
        try:
            if action == "generate_data":
                subprocess.run(["python", r"C:\Users\ashis\OneDrive\Desktop\Monthly-Daily-Energy-Forecasting-Docker-API\notebooks\eda-2.py"], check=True)
            elif action == "see_graph":
                subprocess.run(["python",r"C:\Users\ashis\OneDrive\Desktop\Monthly-Daily-Energy-Forecasting-Docker-API\notebooks\mm.py"], check=True)
        except subprocess.CalledProcessError as e:
            return JsonResponse({"error": f"Error executing script: {e}"}, status=500)

        data_path = os.path.join(settings.BASE_DIR, r"C:\Users\ashis\OneDrive\Desktop\Monthly-Daily-Energy-Forecasting-Docker-API\data\processed\weather_and_consumption.csv")
        df = pd.read_csv(data_path, index_col=0, parse_dates=True)

          # Short-term prediction
        short_term_model = ShortTermEnergyModel(df)
        short_term_prediction = short_term_model.predict_for_date(date)

        # Long-term prediction
        long_term_model = LongTermEnergyModel(df)
        long_term_prediction = long_term_model.predict_for_date(date)

        return JsonResponse({
            "short_term_prediction": short_term_prediction,
            "long_term_prediction": long_term_prediction,
        })
    return JsonResponse({"error": "Invalid request method"}, status=405)
