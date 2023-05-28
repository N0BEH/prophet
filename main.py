# This is a sample Python script.
import csv
import math
import os
import pandas as pd
from prophet import Prophet
import redis
from datetime import datetime, timedelta
from prophet.plot import plot_plotly, plot_components_plotly

def destroyAllRedisData():
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushall()

    r2 = redis.Redis(host='localhost', port=6379, db=1)
    r2.flushall()


def generateRandomData():
    r = redis.Redis(host='localhost', port=6379, db=0)

    now = datetime.now()

    start_time = now

    total_periods = int(1 * 24 * 60 / 5)

    for i in range(0, total_periods):
        key = start_time.strftime("%Y-%m-%d/%H-%M-%S")

        seconds_since_midnight = (
                    start_time - start_time.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        radians = math.pi * seconds_since_midnight / (12 * 60 * 60)

        value = math.ceil((math.sin(radians) + 1) / 2 * 4)
        value2 = math.ceil((math.sin(radians) + 1) / 2 * 12)

        r.set("Elypool:PointInTime:" + key + ":servers", value)
        r.set("Elypool:PointInTime:" + key + ":candidates", value2)

        start_time = start_time - timedelta(minutes=5)


def loadRedisDataToCSV():
    r = redis.Redis(host='localhost', port=6379)

    prefix = 'Elypool:PointInTime:'

    five_days_ago = datetime.now() - timedelta(days=1)

    data_servers = {}
    data_candidates = {}

    for key in r.scan_iter(f'{prefix}*'):
        key_parts = key.decode().split(':')
        datetime_str, category = key_parts[2], key_parts[3]
        key_datetime = datetime.strptime(datetime_str, '%Y-%m-%d/%H-%M-%S')

        if key_datetime > five_days_ago:
            if category == "servers":
                data_servers[key_datetime.strftime('%Y-%m-%d %H:%M:%S')] = r.get(key).decode()
            elif category == "candidates":
                data_candidates[key_datetime.strftime('%Y-%m-%d %H:%M:%S')] = r.get(key).decode()

    sorted_keys_servers = sorted(data_servers.keys())
    sorted_keys_candidates = sorted(data_candidates.keys())

    if os.path.exists("output.csv"):
        os.remove("output.csv")
    else:
        print("The file does not exist")

    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ds', 'servers', 'candidates'])

        for key in sorted_keys_servers:
            print(key)
            writer.writerow([key, data_servers[key], data_candidates.get(key, '')])

    print('Les données ont été écrites dans output.csv')


def predict_candidates(number_of_cicles, freq):
    # Préparez vos données comme avant
    df = pd.read_csv('output.csv')
    df = df.rename(columns={'ds': 'ds', 'candidates': 'y'})
    df['ds'] = pd.to_datetime(df['ds'])

    # Entraînez un modèle pour prédire 'candidates'
    model_candidates = Prophet()
    model_candidates.fit(df)

    # Prédisez les valeurs futures de 'candidates'
    future_dates = model_candidates.make_future_dataframe(periods=int(number_of_cicles), freq=str(freq))
    forecast_candidates = model_candidates.predict(future_dates)

    return forecast_candidates


def predict_servers(number_of_cicles, forecast_candidates):
    # Préparez vos données comme avant
    df = pd.read_csv('output.csv')
    df = df.rename(columns={'ds': 'ds', 'servers': 'y', 'candidates': 'candidates'})
    df['ds'] = pd.to_datetime(df['ds'])

    # Entraînez un modèle pour prédire 'servers'
    model_servers = Prophet()
    model_servers.add_regressor('candidates')
    model_servers.fit(df)

    # Préparez le DataFrame future_dates avec les valeurs prédites de 'candidates'
    future_dates = df.copy()
    future_dates = future_dates._append(forecast_candidates[['ds']].tail(int(number_of_cicles)), ignore_index=True)
    future_dates['candidates'] = forecast_candidates['yhat'].values

    # Prédisez les valeurs futures de 'servers'
    forecast_servers = model_servers.predict(future_dates)

    forecast_future = forecast_servers[forecast_servers['ds'] > max(df['ds'])]
    print(forecast_future[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

    # fig1 = model_servers.plot(forecast_servers)
    # fig2 = model_servers.plot_components(forecast_servers)
    # plot_plotly(model_servers, forecast_servers)
    # plot_components_plotly(model_servers, forecast_servers)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    frequence = '10min'  # minutes
    number_of_cicles = 1

    destroyAllRedisData()

    generateRandomData()

    loadRedisDataToCSV()

    forecast_candidates = predict_candidates(number_of_cicles, frequence)
    predict_servers(number_of_cicles, forecast_candidates)
