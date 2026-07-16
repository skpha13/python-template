from pathlib import Path

SEED: int = 42

CACHE_DIR: Path = Path(__file__).parent.parent / ".cache"
CONFIGS_DIR: Path = Path(__file__).parent.parent / "configs"
DATA_DIR: Path = Path(__file__).parent.parent / "data"
