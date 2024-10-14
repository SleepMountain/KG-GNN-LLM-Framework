# build_gnn.py
import torch
from torch_geometric.nn import GCNConv, global_mean_pool
import torch.nn.functional as F

class SemanticAwareGNN(torch.nn.Module):
    def __init__(self, num_node_features, hidden_channels,length):
        super(GNN, self).__init__()
        self.conv1 = GCNConv(num_node_features, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.lin = torch.nn.Linear(hidden_channels, length)

    def forward(self, x, edge_index, batch):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        x = global_mean_pool(x, batch)  
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.lin(x)
        return x