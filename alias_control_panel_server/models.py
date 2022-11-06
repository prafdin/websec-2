import requests

from yandex_api import QuasarSession, QuasarApi

class UserSession:
    token_name = "csrf_token"

    @property
    def token(self):
        return self.quasar_session.csrf_token


    def __init__(self, yandex_login, yandex_password):
        self.quasar_session = QuasarSession(yandex_login, yandex_password)
        self.user_settings = UserSettings(next(s for s in QuasarApi().get_speakers(self.quasar_session)))

    def check(self):
        return self.quasar_session.check()

class UserSettings:
    def __init__(self, speaker):
        self.speaker = speaker
        # TODO: self.volume = volume