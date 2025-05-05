import numpy as np
import torch
from pathlib import Path
from .recommender import Recommender
from django.core.cache import cache
class RecommenderService:
    def __init__(self):
        self.model =None
        self.user_mapping = None
        self.item_mapping = None
        self.load_model()
    def load_model(self):
        model_path = Path("ml/models/model.pth")
        user_mapping_path = Path("ml/models/user_mapping.npy")
        item_mapping_path = Path("ml/models/item_mapping.npy")

        if model_path.exists():
            num_users = len(np.load(user_mapping_path,allow_pickle=True))
            num_items = len(np.load(item_mapping_path,allow_pickle=True))

            self.model = Recommender(num_users,num_items)
            self.model.load_state_dict(torch.load(model_path))
            self.model.eval()
            self.user_mapping = np.load(user_mapping_path,allow_pickle=True)
            self.item_mapping = np.load(item_mapping_path,allow_pickle=True)

    def get_recommendations(self, user_id, top_n=10):
        if not self.model:
            return self.get_popular_content(top_n)

        user_idx = np.where(self.user_mapping == user_id)[0]
        if len(user_idx) == 0:
            return self.get_popular_content(top_n)  # Fallback

        item_indices = torch.LongTensor(np.arange(len(self.item_mapping)))
        user_indices = torch.LongTensor([user_idx[0]] * len(item_indices))

        with torch.no_grad():
            scores = self.model(user_indices, item_indices).numpy()

        # Fix: Sort descendingly
        top_indices = np.argsort(-scores)[:top_n]
        return self.item_mapping[top_indices].tolist()

    def get_popular_content(self, top_n=10):
        from recommendations.models import Content
        return list(Content.objects.order_by('-created_at').values_list('id', flat=True)[:top_n])