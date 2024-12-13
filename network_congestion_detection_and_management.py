import psutil
import numpy as np
import time
from sklearn.ensemble import RandomForestClassifier

def get_system_stats():
    net_io = psutil.net_io_counters()
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    bytes_sent = net_io.bytes_sent
    bytes_recv = net_io.bytes_recv
    packet_loss = np.random.randint(0, 10)  # Random packet loss between 0% and 9%
    latency = np.nan  # Not used

    return [latency, packet_loss, cpu_usage, memory, bytes_sent, bytes_recv]

def collect_initial_data(model, X_data, y_data):
    traffic_data = get_system_stats()

    if traffic_data:
        print(f"Collected Traffic Data: {traffic_data}")
        if traffic_data[4] < 15661385:
            label = 0
        elif traffic_data[4] < 26062444:
            label = 1
        else:
            label = 2

        X_data.append(traffic_data)
        y_data.append(label)

        if len(X_data) >= 5:
            print("Training model with collected data...")
            model.fit(np.array(X_data), np.array(y_data))
            print("Model trained.")

    return X_data, y_data

def change_router(packet_loss):
    if packet_loss <= 2:
        print("Switching to Router 0 due to low packet loss")
    elif packet_loss <= 5:
        print("Switching to Router 1 due to moderate packet loss")
    else:
        print("Switching to Router 2 due to high packet loss")

def monitor_system():
    model = RandomForestClassifier()
    X_data = []
    y_data = []
    model_trained = False

    while True:
        X_data, y_data = collect_initial_data(model, X_data, y_data)

        if len(X_data) >= 5:
            model_trained = True

        stats_data = get_system_stats()

        if stats_data and model_trained:
            predicted_router = model.predict([stats_data])
            print(f"Stats Data: Packet Loss={stats_data[1]}%, CPU Usage={stats_data[2]}%, Memory Usage={stats_data[3]}%, Sent Bytes={stats_data[4]}B, Recv Bytes={stats_data[5]}B")
            print(f"Predicted Router: Router {predicted_router[0]}")

            # Apply router change based on packet loss
            change_router(stats_data[1])  # Pass packet loss to change router

        time.sleep(5)

monitor_system()
