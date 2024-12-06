from dataclasses import dataclass
from typing import Dict

from pandas import DataFrame


@dataclass
class ExtractContract:
    """
    Contrato que representa o resultado do processo de extração.
    """

    data: Dict[str, DataFrame]
