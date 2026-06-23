import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import logging

logger = logging.getLogger(__name__)

class AnomalyDetector:
    def __init__(self):
        # Isolation Forest is excellent for outlier detection in high-dimensional data
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.is_trained = False

    def train(self, historical_data: list):
        """
        Train the model on historical threat features.
        """
        if not historical_data or len(historical_data) < 5:
            return
        
        df = pd.DataFrame(historical_data)
        self.model.fit(df)
        self.is_trained = True
        logger.info("Anomaly detection pulse updated: Model retrained on new historical data.")

    async def continuous_learning(self):
        """
        Fetch historical reports from MongoDB and trigger a retraining cycle.
        """
        from sentinel_x.db.mongodb import get_database
        db = get_database()
        if not db:
            return

        # Fetch the last 1000 reports to learn from
        cursor = db.intelligence.find().sort("timestamp", -1).limit(1000)
        reports = await cursor.to_list(length=1000)
        
        # Extract features for training (Vision count and NLP probabilities)
        training_features = []
        for r in reports:
            v_count = len(r.get("findings", {}).get("vision", []))
            n_prob = r.get("findings", {}).get("nlp", {}).get("probability", 0)
            training_features.append([v_count, n_prob])
        
        if training_features:
            self.train(training_features)

    def detect(self, current_features: list):
        """
        Detect if the current intelligence report is an anomaly.
        Returns: 1 for normal, -1 for anomaly.
        """
        if not self.is_trained:
            # Fallback for initial phase: simple heuristic threshold
            return 1 if np.mean(current_features) < 0.8 else -1
            
        prediction = self.model.predict([current_features])
        return int(prediction[0])

anomaly_detector = AnomalyDetector()
