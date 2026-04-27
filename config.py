import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_SERVER = os.environ.get('DB_SERVER', r'localhost\SQLEXPRESS')
    DB_NAME = os.environ.get('DB_NAME', 'HMS_DB')
    DB_USERNAME = os.environ.get('DB_USERNAME', '')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')

    @staticmethod
    def get_db_uri():
        server = os.environ.get('DB_SERVER', r'localhost\SQLEXPRESS')
        db = os.environ.get('DB_NAME', 'HMS_DB')
        username = os.environ.get('DB_USERNAME', '')
        password = os.environ.get('DB_PASSWORD', '')
        driver = 'ODBC+Driver+17+for+SQL+Server'

        if username and password:
            return (
                f'mssql+pyodbc://{username}:{password}@{server}/{db}'
                f'?driver={driver}'
            )
        else:
            return (
                f'mssql+pyodbc://@{server}/{db}'
                f'?driver={driver}&trusted_connection=yes'
            )

    SQLALCHEMY_DATABASE_URI = get_db_uri.__func__()


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
