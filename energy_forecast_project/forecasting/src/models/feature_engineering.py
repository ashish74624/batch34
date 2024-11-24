import pandas as pd
import numpy as np

class FeatureEngineer:
    def __init__(self, df):
        self.df = df.copy()

    def create_features(self):
        """Generate time-series features, lags, and rolling averages."""
        created_features = []

        # Time-based features
        self.df['dayofweek'] = self.df.index.dayofweek
        self.df['month'] = self.df.index.month
        self.df['quarter'] = self.df.index.quarter
        self.df['year'] = self.df.index.year
        created_features.extend(['dayofweek', 'month', 'quarter', 'year'])

        # Lag and rolling average features
        columns_to_lag = ['total_consumption', 'temp', 'day_length']
        lags = [1, 2, 3, 7, 30]
        rolling_windows = [2, 3, 7]

        for column in columns_to_lag:
            for lag in lags:
                feature_name = f"{column}_lag_{lag}"
                self.df[feature_name] = self.df[column].shift(lag)
                created_features.append(feature_name)

            for window in rolling_windows:
                feature_name = f"{column}_rolling_mean_{window}"
                self.df[feature_name] = self.df[column].shift(1).rolling(window=window).mean()
                created_features.append(feature_name)

        # Return the DataFrame and the list of created features
        return self.df, created_features
