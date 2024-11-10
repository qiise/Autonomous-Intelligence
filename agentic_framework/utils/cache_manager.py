# utils/cache_manager.py
import diskcache
from utils.logger import logger

class CacheManager:
    def __init__(self, cache_dir='cache'):
        self.cache = diskcache.Cache(cache_dir)

    def get(self, key):
        result = self.cache.get(key, default=None)
        if result:
            logger.info(f"Cache hit for key '{key}'.")
        return result

    def set(self, key, value, expire=3600):
        self.cache.set(key, value, expire=expire)
        logger.info(f"Cache set for key '{key}' with expiration {expire} seconds.")
