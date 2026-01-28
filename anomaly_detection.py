import random
import pandas as pd
from datetime import datetime

class AnomalyDetectionSystem:
    def __init__(self):
        # In a real setup, train Isolation Forest / Autoencoder here
        self.anomaly_types = ["Unusual Movement", "Night Activity", "Zone Breach", "Noise Spike"]

    def detect(self, n=5):
        """
        Simulate anomaly detection results.
        In real usage, feed sensor data to ML model here.
        """
        data = []
        for _ in range(n):
            anomaly = random.choice(self.anomaly_types)
            severity = random.choice(["Low", "Medium", "High"])
            location = random.choice(["Zone A", "Zone B", "Zone C", "Zone D"])
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data.append([anomaly, severity, location, timestamp])

        df = pd.DataFrame(data, columns=["Anomaly", "Severity", "Location", "Timestamp"])
        return df


# ---------------- Demo Run ---------------- #
if __name__ == "__main__":
    detector = AnomalyDetectionSystem()
    results = detector.detect(n=3)
    print("Simulated anomalies:\n", results)
