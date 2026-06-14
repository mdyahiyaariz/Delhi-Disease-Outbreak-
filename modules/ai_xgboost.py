import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error

def xgboost_predict(spatio_temporal_df):
    """
    Train an XGBoost regressor to predict next week's case count based on lag features.
    """
    predictions = []
    rmse_list = []
    mae_list = []
    
    for (cluster_id, disease), group in spatio_temporal_df.groupby(['cluster_id', 'disease']):
        ts = group.sort_values('time_window').copy()
        
        # Need enough data for lags
        if len(ts) < 4:
            continue
            
        # Create lag features
        ts['lag_1'] = ts['case_count'].shift(1)
        ts['lag_2'] = ts['case_count'].shift(2)
        
        train_data = ts.dropna()
        
        if len(train_data) < 2:
            continue
            
        X = train_data[['lag_1', 'lag_2']]
        y = train_data['case_count']
        
        # Train simple model
        model = xgb.XGBRegressor(n_estimators=50, max_depth=3, random_state=42, objective='reg:squarederror')
        try:
            model.fit(X, y)
            
            # Calculate in-sample metrics
            train_preds = model.predict(X)
            rmse_list.append(np.sqrt(mean_squared_error(y, train_preds)))
            mae_list.append(mean_absolute_error(y, train_preds))
            
            # Predict next week based on the most recent row's data
            last_case = ts['case_count'].iloc[-1]
            last_lag = ts['lag_1'].iloc[-1]
            
            next_X = pd.DataFrame({'lag_1': [last_case], 'lag_2': [last_lag]})
            pred_y = model.predict(next_X)[0]
            
            predictions.append({
                'cluster_id': cluster_id,
                'disease': disease,
                'xgboost_predicted_cases': max(0, round(float(pred_y)))
            })
        except Exception as e:
            print(f"XGBoost failed for cluster {cluster_id} {disease}: {e}")
    metrics = {
        'xgboost_rmse': np.mean(rmse_list) if rmse_list else 0.0,
        'xgboost_mae': np.mean(mae_list) if mae_list else 0.0
    }
            
    return pd.DataFrame(predictions), metrics
