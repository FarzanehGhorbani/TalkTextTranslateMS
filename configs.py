from pydantic_settings import BaseSettings


class Development(BaseSettings): # type: ignore
    DEBUG: bool = False
    


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
