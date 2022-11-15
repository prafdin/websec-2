from os import environ


class Config:
    def __init__(self):
        self.SITE_ROOT = environ.get('SITE_ROOT')

app_config = Config()