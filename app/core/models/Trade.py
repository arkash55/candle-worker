


from dataclasses import dataclass
import datetime


@dataclass(frozen=True)
class Trade:
    symbol: str
    price: float
    size: int
    timestamp: datetime

