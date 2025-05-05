import torch
import torch.nn as nn
import numpy as np
from pathlib import Path
import sys
import os
BASE_DIR = Path(__file__).resolve().parent.parent  # Should point to recoai-backend/
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
import django
django.setup()
from recommendations.models import UserInteraction
class Recommender(nn.Module):
    def __init__(self, num_users, num_items, embedding_dim=64):
        super().__init__()
        self.user_embed = nn.Embedding(num_users, embedding_dim)
        self.item_embed = nn.Embedding(num_items, embedding_dim)
        self.user_bias = nn.Embedding(num_users, 1)
        self.item_bias = nn.Embedding(num_items, 1)

    def forward(self, user_ids, item_ids):
        user_vec = self.user_embed(user_ids)
        item_vec = self.item_embed(item_ids)
        dot_product = (user_vec * item_vec).sum(dim=1)
        return dot_product + self.user_bias(user_ids).squeeze() + self.item_bias(item_ids).squeeze()


def get_training_data():
    # Only use interactions with a rating
    interactions = UserInteraction.objects.exclude(rating__isnull=True)
    content_ids = list({i.content_id for i in interactions})
    if not interactions.exists():
        raise ValueError("No training data found. Add user interactions with ratings first.")
    from recommendations.models import Content
    all_content_ids = Content.objects.values_list('id', flat=True)
    item_mapping = np.array(list(all_content_ids))  # <-- Use all valid IDs

    user_ids = []
    item_ids = []
    ratings = []

    # Create mapping for user and item IDs to indices
    user_set = sorted({i.user_id for i in interactions})
    item_set = sorted({i.content_id for i in interactions})
    user_id_to_idx = {uid: idx for idx, uid in enumerate(user_set)}
    item_id_to_idx = {iid: idx for idx, iid in enumerate(item_set)}

    for interaction in interactions:
        user_ids.append(user_id_to_idx[interaction.user_id])
        item_ids.append(item_id_to_idx[interaction.content_id])
        ratings.append(interaction.rating)

    return (
        torch.LongTensor(user_ids),
        torch.LongTensor(item_ids),
        torch.FloatTensor(ratings),
        np.array(user_set),
        np.array(item_set)
    )


def train_model(embedding_dim=64, epochs=10, lr=0.01):
    print("Fetching data from database...")
    user_ids, item_ids, ratings, user_mapping, item_mapping = get_training_data()
    num_users = len(user_mapping)
    num_items = len(item_mapping)

    print(f"Training on {len(ratings)} samples, {num_users} users, {num_items} items.")

    model = Recommender(num_users, num_items, embedding_dim)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        predictions = model(user_ids, item_ids)
        loss = criterion(predictions, ratings)
        loss.backward()
        optimizer.step()
        print(f"Epoch: {epoch + 1}, Loss: {loss.item():.4f}")

    # Save model and mappings
    model_dir = Path("ml/models")
    model_dir.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), model_dir / "model.pth")
    np.save(model_dir / "user_mapping.npy", user_mapping)
    np.save(model_dir / "item_mapping.npy", item_mapping)
    print("Model and mappings saved to ml/models/")


if __name__ == "__main__":
    train_model(embedding_dim=64, epochs=10, lr=0.01)