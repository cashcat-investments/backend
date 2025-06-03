from src.infrastructure.config.config import configs

class Settings():
    PROJECT_NAME: str = configs.PROJECT_NAME
    VERSION: str = configs.VERSION
    STOCK_API_BASE_URL: str = configs.STOCK_API_BASE_URL
    STOCK_API_TOKEN: str = configs.STOCK_API_TOKEN
    HISTORIC_STOCK_API_BASE_URL: str = configs.HISTORIC_STOCK_API_BASE_URL
    HISTORIC_STOCK_API_TOKEN: str = configs.HISTORIC_STOCK_API_TOKEN
    SUPABASE_URL: str = configs.SUPABASE_URL
    SUPABASE_KEY: str = configs.SUPABASE_KEY
    DATABASE_URL: str = configs.DATABASE_URI
    CORS_ORIGINS: list[str] = configs.CORS_ORIGINS

    # Server Configuration
    PORT: int = int(configs.PORT)
    ENVIRONMENT: str = configs.ENV
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == 'dev'
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == 'prod'
    
    @property
    def is_test(self) -> bool:
        return self.ENVIRONMENT == 'test'
    
    @property
    def is_stage(self) -> bool:
        return self.ENVIRONMENT == 'stage'
