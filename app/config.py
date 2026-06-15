from datetime import timedelta
import os


class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)

    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)


class DevelopmentConfig(Config):

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"


class TestingConfig(Config):

    TESTING = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


class ProductionConfig(Config):

    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
