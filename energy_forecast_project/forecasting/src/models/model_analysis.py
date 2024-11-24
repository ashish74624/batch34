from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
import pandas as pd


class ModelAnalyzer:
    def __init__(self, df):
        self.df = df

    def analyze_models(self, test_date):
        """Evaluate models and return metrics for a given test date."""
        results = {}

        # Example: Short-term prediction RMSE
        if 'short_term_prediction' in self.df.columns and 'total_consumption' in self.df.columns:
            y_true = self.df.loc[test_date, 'total_consumption']
            y_pred = self.df.loc[test_date, 'short_term_prediction']
            if not pd.isna(y_pred):
                results['Short-Term RMSE'] = np.sqrt(mean_squared_error([y_true], [y_pred]))
                results['Short-Term MAE'] = mean_absolute_error([y_true], [y_pred])

        # Example: Long-term prediction RMSE
        if 'long_term_prediction' in self.df.columns and 'total_consumption' in self.df.columns:
            y_true = self.df.loc[test_date, 'total_consumption']
            y_pred = self.df.loc[test_date, 'long_term_prediction']
            if not pd.isna(y_pred):
                results['Long-Term RMSE'] = np.sqrt(mean_squared_error([y_true], [y_pred]))
                results['Long-Term MAE'] = mean_absolute_error([y_true], [y_pred])

        return results
