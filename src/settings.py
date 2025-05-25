from os import getenv

class Settings():
    # API Configuration
    STOCK_API_BASE_URL: str = getenv('STOCK_API_BASE_URL', '')
    STOCK_API_TOKEN: str = getenv('STOCK_API_TOKEN', '')
    HISTORIC_STOCK_API_BASE_URL: str = getenv('HISTORIC_STOCK_API_BASE_URL', '')
    HISTORIC_STOCK_API_TOKEN: str = getenv('HISTORIC_STOCK_API_TOKEN', '')
    SUPABASE_URL: str = getenv('SUPABASE_URL', '')
    SUPABASE_KEY: str = getenv('SUPABASE_KEY', '')
    
    # Server Configuration
    PORT: int = int(getenv('PORT', '8000'))
    ENVIRONMENT: str = getenv('ENVIRONMENT', 'development')
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == 'development'
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == 'production'
