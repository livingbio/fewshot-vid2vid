from pydantic import BaseSettings, Field


class Config(BaseSettings):
    CLOUDINARY_CLOUD_NAME = Field(..., env="CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = Field(..., env="CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = Field(..., env="CLOUDINARY_API_SECRET")


config = Config()
