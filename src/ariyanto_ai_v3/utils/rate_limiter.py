from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict

class RateLimiter:
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = timedelta(seconds=window_seconds)
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, user_id: str) -> bool:
        now = datetime.now()
        # Bersihkan request lama
        self.requests[user_id] = [
            t for t in self.requests[user_id] 
            if now - t < self.window
        ]
        
        if len(self.requests[user_id]) < self.max_requests:
            self.requests[user_id].append(now)
            return True
        return False

# Global instance
telegram_limiter = RateLimiter(max_requests=15, window_seconds=60)
