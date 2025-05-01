# graph_reader_api/config.py
from dataclasses import dataclass


@dataclass
class APIConfig:
    base_dir: str
    indexer_type: str = "memory"
    cache_size: int = 1000
