import flwr as fl
from typing import List, Tuple
from flwr.common import Metrics
import threading
import logging

logger = logging.getLogger(__name__)

class FederatedService:
    """
    Management service for Federated Learning coordination.
    Ensures data sovereignty by training models across decentralized nodes.
    """
    def __init__(self):
        self.strategy = fl.server.strategy.FedAvg(
            evaluate_metrics_aggregation_fn=self.weighted_average,
        )
        self.server_thread = None

    def weighted_average(self, metrics: List[Tuple[int, Metrics]]) -> Metrics:
        """
        Aggregates accuracy metrics weighted by the number of examples from each node.
        """
        if not metrics:
            return {"accuracy": 0.0}
            
        accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics]
        examples = [num_examples for num_examples, _ in metrics]

        return {"accuracy": sum(accuracies) / sum(examples)}

    def start_federated_server(self, rounds: int = 3):
        """
        Start the Flower federated learning server in a background thread.
        """
        def run_server():
            try:
                logger.info("Initializing Federated Learning Server...")
                fl.server.start_server(
                    server_address="0.0.0.0:8080",
                    config=fl.server.ServerConfig(num_rounds=rounds),
                    strategy=self.strategy,
                )
            except Exception as e:
                logger.error(f"Federated Server Error: {e}")

        if not self.server_thread or not self.server_thread.is_alive():
            self.server_thread = threading.Thread(target=run_server, daemon=True)
            self.server_thread.start()
            return {"status": "Federated Server Running", "rounds": rounds, "port": 8080}
        
        return {"status": "Federated Server is already active", "port": 8080}

federated_service = FederatedService()
