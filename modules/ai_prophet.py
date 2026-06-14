import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_error

def prophet_forecast(spatio_temporal_df, periods=1):
    """
    Generate next-week case count forecasts using Facebook Prophet.
    """
    forecasts = []
    rmse_list = []
    mae_list = []
    
    for (cluster_id, disease), group in spatio_temporal_df.groupby(['cluster_id', 'disease']):
        ts = group[['time_window', 'case_count']].copy()
        
        # Convert time_window to a datetime object
        if pd.api.types.is_period_dtype(ts['time_window']):
            ts['ds'] = ts['time_window'].dt.to_timestamp()
        else:
            ts['ds'] = pd.to_datetime(ts['time_window'].astype(str).str.split('/').str[0])
        ts['y'] = ts['case_count']
        
        # We need at least 2 data points for Prophet
        if len(ts) < 2:
            continue
            
        # Suppress verbose Prophet logs
        import logging
        logging.getLogger('prophet').setLevel(logging.WARNING)
        
        model = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False)
        try:
            model.fit(ts)
            future = model.make_future_dataframe(periods=periods, freq='W')
            forecast = model.predict(future)
            
            # Get the forecast for the last `periods` rows
            future_forecast = forecast.tail(periods)[['ds', 'yhat']].copy()
            future_forecast['cluster_id'] = cluster_id
            future_forecast['disease'] = disease
            future_forecast['yhat'] = future_forecast['yhat'].apply(lambda x: max(0, round(x)))
            
            forecasts.append(future_forecast)
            
            # Calculate in-sample metrics
            train_pred = forecast[['ds', 'yhat']].merge(ts[['ds', 'y']], on='ds', how='inner')
            if not train_pred.empty:
                rmse_list.append(np.sqrt(mean_squared_error(train_pred['y'], train_pred['yhat'])))
                mae_list.append(mean_absolute_error(train_pred['y'], train_pred['yhat']))
                
        except Exception as e:
            print(f"Prophet forecast failed for cluster {cluster_id} {disease}: {e}")
            
    metrics = {
        'prophet_rmse': np.mean(rmse_list) if rmse_list else 0.0,
        'prophet_mae': np.mean(mae_list) if mae_list else 0.0
    }
    
    if forecasts:
        return pd.concat(forecasts, ignore_index=True), metrics
    return pd.DataFrame(), metrics
