from pydantic import BaseModel
from datetime import datetime

STOCKS_PREFIX = "stocks"

class StockQuote(BaseModel):
    price: float
    timestamp: datetime

    def to_dict(self):
        return {
            "price": self.price,
            "timestamp": self.timestamp.isoformat()
        }