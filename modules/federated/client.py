import flwr as fl
import torch
import torch.nn as nn
from collections import OrderedDict

# Simple placeholder model for federated updates
class SentinelNet(nn.Module):
    def __init__(self):
        super(SentinelNet, self).__init__()
        self.fc = nn.Linear(10, 2)

    def forward(self, x):
        return self.fc(x)

class SentinelClient(fl.client.NumPyClient):
    """
    Standard Federated Learning client for SENTINEL-X nodes.
    Designed to run on edge devices (Jetson Nano, Local Servers).
    """
    def __init__(self, model, trainloader, valloader):
        self.model = model
        self.trainloader = trainloader
        self.valloader = valloader

    def get_parameters(self, config):
        return [val.cpu().numpy() for _, val in self.model.state_dict().items()]

    def set_parameters(self, parameters):
        params_dict = zip(self.model.state_dict().keys(), parameters)
        state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
        self.model.load_state_dict(state_dict, strict=True)

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        # Training logic would go here
        print("Training locally on edge data...")
        return self.get_parameters(config={}), len(self.trainloader), {}

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        # Evaluation logic would go here
        return 0.5, len(self.valloader), {"accuracy": 0.85}

def start_client(server_address="localhost:8080"):
    model = SentinelNet()
    # In a real scenario, data loaders would be initialized here
    client = SentinelClient(model, [], [])
    fl.client.start_numpy_client(server_address=server_address, client=client)
