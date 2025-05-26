from supabase import create_client, Client
from src.core.infrastructure.config.settings import Settings

class Supabase:
    def __init__(self, settings: Settings):
        self._url = settings.SUPABASE_URL
        self._key = settings.SUPABASE_KEY
        self._client: Client = create_client(self._url, self._key)

    def get_client(self) -> Client:
        return self._client