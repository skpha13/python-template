import torch

from src.core.logging import logger


def resolve_device(device: str | int | torch.device | None = None) -> torch.device:
    """Return an inference device, preferring cuda, then mps, then cpu."""
    if device is not None:
        device = torch.device(device)

    if torch.cuda.is_available():
        device = torch.device("cuda")

    mps = getattr(torch.backends, "mps", None)
    if mps is not None and mps.is_available():
        device = torch.device("mps")

    if device is None:
        device = torch.device("cpu")

    logger.info(f"Using device: {device}")

    return device
