from yandex_api import QuasarSession, QuasarApi

class UserSession:
    token_name = "csrf_token"

    @property
    def token(self):
        return self.quasar_session.csrf_token

    def __init__(self, yandex_login, yandex_password):
        self.quasar_session = QuasarSession(yandex_login, yandex_password)
        self.user_settings = UserSettings(speakers = [ Speaker(r_s) for r_s in QuasarApi(self.quasar_session).get_raw_speakers()])

    def check(self):
        return self.quasar_session.check()

    def get_speakers(self):
        return self.user_settings.speakers

    def change_active_speaker(self, new_speaker):
        self.user_settings.change_active_speaker(new_speaker)

    def play_music(self, name = ""):
        QuasarApi(self.quasar_session).play_music(self.user_settings.active_speaker, name)

    def stop_music(self):
        QuasarApi(self.quasar_session).stop_music(self.user_settings.active_speaker)

class UserSettings:
    @property
    def active_speaker(self):
        return next(s for s in self.speakers if s.used == True)

    def __init__(self, speakers):
        self.speakers : list = speakers
        active_speaker = next(s for s in speakers)
        active_speaker.used = True
        # TODO: self.volume = volume

    def change_active_speaker(self, new_speaker):
        for s in self.speakers:
            if s.id == new_speaker.id:
                s.used = True
            else:
                s.used = False


class Speaker:
    def __init__(self, raw_speaker, used = False):
        self.id = raw_speaker["id"]
        self.image = raw_speaker["icon_url"]
        self.name = raw_speaker["name"]
        self.used = used