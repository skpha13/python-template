import random

import numpy as np
import torch

from src.constants import SEED


def set_seeds(seed: int | None = None) -> None:
    """Set random seeds for reproducibility."""
    seed = seed if seed is not None else SEED

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
