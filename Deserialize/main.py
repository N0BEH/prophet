# This is a sample Python script.
import csv
import math
import os
import pandas as pd
from prophet import Prophet
import redis
from datetime import datetime, timedelta
from PointInTime import PointInTime

import yaml

def load_config(file_name):
    with open(file_name, 'r') as file:
        config = yaml.safe_load(file)
    return config

config = load_config('config.yaml')

def loadDataFromCSV():
    df = pd.read_csv('output.csv')
    df['ds'] = pd.to_datetime(df['ds'])

    # Convert DataFrame to list of dictionaries
    data = df.to_dict('records')
    return data

def loadRedisDataToCSV(filterType, nCandidates):
    r = redis.Redis(host=config['redis']['host'], port=config['redis']['port'])

    prefix = config['redis']['prefix']

    ten_days_ago = datetime.now() - timedelta(days=config['load_data']['past_days'])

    data_points = {}

    for key in r.scan_iter(f'{prefix}*'):
        key_parts = key.decode().split(':')
        datetime_str = key_parts[3].replace('/', ' ')
        key_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H-%M-%S')

        if key_datetime > ten_days_ago:
            data = r.get(key).decode()

            data_points[key_datetime.strftime('%Y-%m-%d %H:%M:%S')] = PointInTime.from_json(data,filterType)

    sorted_keys = sorted(data_points.keys())

    if os.path.exists("output.csv"):
        os.remove("output.csv")
    else:
        print("The file does not exist")

    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ds', 'servers'] + [f'candidate_{i + 1}' for i in range(nCandidates)])

        for key in sorted_keys:
            servers = data_points[key].get_total_servers() if key in data_points else ''
            candidates = [stat.get_total_candidates() for stat in data_points[key].stats] if key in data_points else ['' for _ in range(nCandidates)]
            writer.writerow([key, servers, *candidates])

    print('Les données ont été écrites dans output.csv')


def loadRedisData(filterType, nCandidates):
    r = redis.Redis(host=config['redis']['host'], port=config['redis']['port'])

    print(r.ping())

    prefix = config['redis']['prefix']

    print("Prefix : " + prefix)

    one_day_ago = datetime.now() - timedelta(days=config['load_data']['past_days'])

    data_points = {}

    for key in r.scan_iter(f'{prefix}*'):

        key_parts = key.decode().split(':')
        datetime_str = key_parts[3].replace('/', ' ')
        key_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H-%M-%S')

        if key_datetime > one_day_ago:
            data = r.get(key).decode()

            data_points[key_datetime.strftime('%Y-%m-%d %H:%M:%S')] = PointInTime.from_json(data, filterType)

    sorted_keys = sorted(data_points.keys())

    results = []
    for key in sorted_keys:
        servers = data_points[key].get_total_servers() if key in data_points else ''
        candidates = [stat.get_total_candidates() for stat in data_points[key].stats] if key in data_points else ['' for
                                                                                                                  _ in
                                                                                                                  range(
                                                                                                                      nCandidates)]

        result_dict = {'ds': key, 'servers': servers}
        for i in range(nCandidates):
            result_dict[f'candidate_{i + 1}'] = candidates[i]
        results.append(result_dict)

    return results

def predict_candidates(data, event):
    forecasts = []
    cols = []

    for i in range(int(config['filters']['kolizeum'])):
        print(f'candidate_{i + 1}')
        cols.append(f'candidate_{i + 1}')

    for candidate in cols:
        df = pd.DataFrame(data)
        df = df.rename(columns={candidate: 'y'})
        df['ds'] = pd.to_datetime(df['ds'])

        model_candidates = Prophet(holidays=event)
        model_candidates.fit(df)

        future_dates = model_candidates.make_future_dataframe(periods=int(config['prediction']['number_of_cicles']), freq=str(config['prediction']['freq']))
        forecast_candidates = model_candidates.predict(future_dates)
        forecasts.append(forecast_candidates)

    return forecasts  # A list of forecasts for each candidate


def predict_servers(data, forecast_candidates, event):
    df = pd.DataFrame(data)
    df = df.rename(columns={'servers': 'y'})
    df['ds'] = pd.to_datetime(df['ds'])

    model_servers = Prophet(holidays=event)
    for i in range(len(forecast_candidates)):
        df[f'candidate_{i + 1}'] = forecast_candidates[i]['yhat']
        model_servers.add_regressor(f'candidate_{i + 1}')

    model_servers.fit(df)

    future = df.copy()
    for i in range(len(forecast_candidates)):
        future[f'candidate_{i + 1}'] = forecast_candidates[i]['yhat']

    # Add future periods
    last_date = future['ds'].max()
    future_periods = pd.date_range(start=last_date, periods=config['prediction']['number_of_cicles'] + 1, freq=config['prediction']['freq'])[
                        1:]  # Exclude the first date because it's already in `future`
    future_periods_df = pd.DataFrame(index=future_periods)
    future_periods_df.reset_index(inplace=True)
    future_periods_df.columns = ['ds']
    for i in range(len(forecast_candidates)):
        future_periods_df[f'candidate_{i + 1}'] = forecast_candidates[i]['yhat'].tail(config['prediction']['number_of_cicles']).values

    future = pd.concat([future, future_periods_df])

    forecast_servers = model_servers.predict(future)

    forecast_future = forecast_servers[forecast_servers['ds'] > max(df['ds'])]
    return (forecast_future[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

    #fig1 = model_servers.plot(forecast_servers)
    #fig2 = model_servers.plot_components(forecast_servers)
    #plot_plotly(model_servers, forecast_servers)
    #plot_components_plotly(model_servers, forecast_servers)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    config = load_config('config.yaml')

    evenement_ouverture = pd.DataFrame({
        'holiday': 'event',
        'ds': pd.to_datetime(['2023-07-12', '2023-06-16']),
        'lower_window': 0,
        'upper_window': 1,
    })

    for key, value in config['filters'].items():
        print(key, value)
        print(config['redis']['enabled'])

        if config['redis']['enabled']:
            data = loadRedisData(key, value)
            loadRedisDataToCSV(key, value)
        else:
            data = loadDataFromCSV()

        forecast_candidates = predict_candidates(data, evenement_ouverture)
        res = predict_servers(data, forecast_candidates, evenement_ouverture)

        print(res)

        if config['redis']['enabled']:
            r = redis.Redis(host=config['redis']['host'], port=config['redis']['port'])
            r.set(f'Elypool:Forecast:{key}', res.to_json(orient='records'))



