import time


class CacheWithTTL:
    def __init__(self, ttl=300):  # TTL de 300 segundos (5 minutos)
        self.ttl = ttl
        self.cache = {}

    def __getitem__(self, key):
        """Permite acessar valores como cache[key]"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return data
            else:
                # Remove se estiver expirado
                del self.cache[key]
        return None

    def get(self, key):
        return self.__getitem__(key)

    def __setitem__(self, key, value):
        """Permite atribuir valores como cache[key] = value"""
        self.cache[key] = (value, time.time())

    def __delitem__(self, key):
        """Permite remover valores com del cache[key]"""
        if key in self.cache:
            del self.cache[key]

    def clear(self, key=None):
        """Limpa o cache"""
        if key:
            if key in self.cache:
                del self.cache[key]
        else:
            self.cache.clear()

    def keys(self):
        """Retorna as chaves válidas no cache."""
        return [
            key
            for key, (_, timestamp) in self.cache.items()
            if time.time() - timestamp < self.ttl
        ]
