import cfscrape as cfscrape
import requests
import re

class YandexAPI:
    quasar_url = "https://iot.quasar.yandex.ru/m/user"
    music_url = "https://api.music.yandex.net"
    session = requests.session()
    csrf_token = None
    login = ""

    def __init__(self, login, password):
        self.login = login
        self.session.headers.update({
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0)   Gecko/20100101 Firefox/69.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'ru,en-US;q=0.5',
            'Accept-Encoding':'gzip, deflate, br',
            'DNT':'1',
            'Connection':'keep-alive',
            'Upgrade-Insecure-Requests':'1',
            'Pragma':'no-cache',
            'Cache-Control':'no-cache',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1'
        })

        resp = self.session.get("https://passport.yandex.ru/auth/welcome")

        m = re.search(r'"csrf_token" value="([^"]+)"', resp.text)
        auth_payload = {"csrf_token": m[1]}
        self.csrf_token = m[1]

        resp = self.session.post("https://passport.yandex.ru/registration-validations/auth/multi_step/start",
                                 {**auth_payload, "login": login}).json()
        auth_payload["track_id"] = resp["track_id"]

        resp = self.session.post("https://passport.yandex.ru/registration-validations/auth/multi_step/commit_password",
                          {**auth_payload, "password": password,
                           'retpath': "https://passport.yandex.ru/am/finish?status=ok&from=Login"}).json()

        if ("errors" in resp and resp["errors"][0] == "password.not_matched"):
            raise RuntimeError("Login or password isn't correct")

        self.get_music_id()

    def get_music_id(self):
        self.music_uid = str(self.session.get(self.music_url + '/users/' + self.login).json()['result']['uid'])

    def get_speakers(self):
        rooms: list = self.session.get(self.quasar_url + "/devices").json()['rooms']
        all_devices = []
        for room_devices in [r['devices'] for r in rooms]:
            all_devices += room_devices
        return all_devices

    def _update_csrf(self):
        raw = self.session.get("https://yandex.ru/quasar").text
        m = re.search('"csrfToken2":"(.+?)"', raw)
        self.csrf_token = m[1]

    def get_scenarios(self):
        return self.session.get(self.quasar_url + "/scenarios").json()['scenarios']

    def add_scenario(self, payload):
        self._update_csrf()
        return self.session.post(self.quasar_url + "/scenarios", json=payload,
                                 headers={'x-csrf-token': self.csrf_token}).json()

    def exec_scenario(self, id):
        self._update_csrf()
        return self.session.post(self.quasar_url + "/scenarios/" + id + "/actions",
                                 headers={'x-csrf-token': self.csrf_token}).json()

    def play_song(self, speaker, name, id):
        logic = {
            'type': 'devices.capabilities.quasar.server_action',
            'state': {
                'instance': 'text_action',
                'value': 'Включи ' + name,
            }
        }

        scenario = YandexAPI.create_scenario('Включи', speaker, logic)
        self._update_csrf()
        self.session.put(self.quasar_url + "/scenarios/" + id, json=scenario, headers={'x-csrf-token': self.csrf_token})
        self._update_csrf()
        return self.session.post(self.quasar_url + "/scenarios/" + id + "/actions",
                                 headers={'x-csrf-token': self.csrf_token}).json()

    def get_liked_tracks(self):
        track_list = \
            self.session.get(self.music_url + "/users/" + self.music_uid + "/likes/tracks").json()['result']['library'][
                'tracks']
        track_ids = [track['id'] for track in track_list]
        self._update_csrf()
        return self.session.post(self.music_url + "/tracks", {'track-ids': track_ids}).json()['result']

    @staticmethod
    def create_scenario(scenario, speaker, logic):
        return {
            'name': scenario,
            'icon': 'home',
            'triggers': [{
                'type': 'scenario.trigger.voice',
                'value': scenario
            }],
            'steps': [{
                'type': 'scenarios.steps.actions',
                'parameters': {
                    'requested_speaker_capabilities': [],
                    'launch_devices': [{
                        'id': speaker,
                        'capabilities': [logic]
                    }]
                }
            }]
        }
