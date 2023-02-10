import os

from pydantic import validator, Field, BaseSettings


class ProjectSettings(BaseSettings):
    # main
    current_dir: str = os.path.dirname(os.path.abspath(__file__))
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8081, env="PORT")
    # database
    db_driver: str = Field("postgresql+asyncpg", env="DB_DRIVER")
    db_host: str = Field(..., env="POSTGRES_HOST")
    db_port: str = Field(..., env="POSTGRES_PORT")
    db_user: str = Field(..., env="POSTGRES_USER")
    db_name: str = Field(..., env="POSTGRES_DATABASE")
    db_password: str = Field(..., env="POSTGRES_PASSWORD")
    test: bool = Field(False, env="TEST")

    def __getattr__(self, item):
        return self.dict()[item]

    @validator("test")
    def validate_debug(cls, value):
        return bool(int(value))

    @property
    def data_base_url(self):
        return (
            f"{self.db_driver}://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def sync_postgres_url(self):
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def base_api_url(self):
        return f"http://{self.host}:{self.port}"

    @property
    def db_unix_socket_url(self):
        return


ProjectSettings = ProjectSettings()
