from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_DNS: str
    using_dsn: bool

    @property
    def DATABASE_URL_asyncpg(self):
        # DSN
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        if self.using_dsn:
            return f'postgresql+pyodbc:///?odbc_connect=DSN={self.DB_DNS}'
        else: 
            return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        

    @property
    def DATABASE_URL_psycorg(self):
        # DSN
        # postgresql+psycodg://postgres:postgres@localhost:5432/sa 
        if self.using_dsn:
            return f'postgresql+pyodbc:///?odbc_connect=DSN={self.DB_DNS}'
        else:
            return f'postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()