import pandas as pd
import matplotlib.pyplot as plt
from django.http import JsonResponse, HttpResponse
from io import BytesIO
import base64
from forecasting.src.models.short_term_energy_model import ShortTermEnergyModel
from forecasting.src.models.long_term_energy_model import LongTermEnergyModel
from django.conf import settings
import os
# from forecasting.src.models.base_energy_model import ShortTermEnergyModel, LongTermEnergyModel

# Load processed data

# Short-term Model View
def short_term_feature_importance(request):
    data_path = os.path.join(settings.BASE_DIR, 'data/processed/weather_and_consumption.csv')
    weather_and_consumption_df = pd.read_csv(data_path, index_col=0, parse_dates=True)
    short_term_model = ShortTermEnergyModel(weather_and_consumption_df)
    fig, ax = plt.subplots(figsize=(12, 6))
    short_term_model.plot_feature_importance(top_n=10)
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    image_base64 = base64.b64encode(image_png).decode("utf-8")
    return JsonResponse({"image": image_base64})

# Prediction Comparison
def prediction_comparison(request):
    date_range = pd.date_range(start='2009-05-17', end='2010-05-17', freq='D')
    predictions = []

    short_term_model = ShortTermEnergyModel(weather_and_consumption_df)
    long_term_model = LongTermEnergyModel(weather_and_consumption_df)

    for date in date_range:
        date_str = date.strftime('%Y-%m-%d')
        long_term_prediction = long_term_model.predict_for_date(date_str)
        short_term_prediction = short_term_model.predict_for_date(date_str)
        real_value = weather_and_consumption_df.loc[date_str, 'total_consumption']

        predictions.append({
            'date': date_str,
            'long_term_prediction': long_term_prediction,
            'short_term_prediction': short_term_prediction,
            'real_value': real_value
        })

    predictions_df = pd.DataFrame(predictions).set_index('date')
    fig, ax = plt.subplots(figsize=(20, 6))
    predictions_df[['real_value', 'long_term_prediction', 'short_term_prediction']].plot(ax=ax)
    ax.set_xlabel('Date')
    ax.set_ylabel('Consumption')
    ax.set_title('Comparison of Long-Term and Short-Term Predictions with Real Values')
    ax.grid(True)
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    image_base64 = base64.b64encode(image_png).decode("utf-8")
    return JsonResponse({"image": image_base64})
