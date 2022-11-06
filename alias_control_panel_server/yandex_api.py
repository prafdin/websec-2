import requests
import re

class QuasarSession:
    session = requests.session()
    music_url = "https://api.music.yandex.net"
    csrf_token = None

    def __init__(self, login, password):
        self.login = login
        self.session.headers.update({
            'User-Agent': 'Chrome',
            'Host': 'passport.yandex.ru'
        })
        self.yandex_login(login, password)

    def yandex_login(self, login, password):
        resp = self.session.get("https://passport.yandex.ru/auth/welcome")
        csrf_token = re.search(r'"csrf_token" value="([^"]+)"', resp.text)[1]
        self.csrf_token = csrf_token

        auth_payload = {"csrf_token": csrf_token}
        resp = self.session.post("https://passport.yandex.ru/registration-validations/auth/multi_step/start",
                                 {**auth_payload, "login": login}).json()
        auth_payload["track_id"] = resp["track_id"]

        resp = self.session.post("https://passport.yandex.ru/registration-validations/auth/multi_step/commit_password",
                                 {**auth_payload, "password": password,
                                  'retpath': "https://passport.yandex.ru/am/finish?status=ok&from=Login"}).json()


        if resp["status"] != 'ok':
            raise RuntimeError("Some error")

        # TODO: Correct process response status (incorrect log/pass or captcha error)

    def get_music_id(self):
        self.music_uid = str(self.session.get(self.music_url + '/users/' + self.login).json()['result']['uid'])

    def check(self):
        r = self.session.get("https://id.yandex.ru/")
        return re.search('Авторизация', r.text) is None

    def post(self, url, json=None):
        return self.session.post(url, headers={'x-csrf-token': self.get_new_csrf()}, json=json)

    def get(self, url):
        return self.session.get(url, headers={'x-csrf-token': self.get_new_csrf()})

    def put(self, url, json):
        return self.session.put(url, json=json, headers={'x-csrf-token': self.get_new_csrf()})
    def get_new_csrf(self):
        raw = self.session.get("https://yandex.ru/quasar").text
        m = re.search('"csrfToken2":"(.+?)"', raw)
        return m[1]

class QuasarApi:
    quasar_url = "https://iot.quasar.yandex.ru/m/user"

    def __init__(self, session):
        self.session = session

    def get_raw_speakers(self):
        rooms = self.session.get(self.quasar_url + "/devices").json()['rooms']
        all_speakers = []
        for room_devices in [r['devices'] for r in rooms]:
            all_speakers += room_devices
        return all_speakers

    def play_music(self, active_speaker, name = ""):
        scenario_name = 'Включить'
        scenario_action = "Включить " + name if name else "Включи музыку"
        scenario = self._get_scenario(scenario_name)
        logic = {
            'type': 'devices.capabilities.quasar.server_action',
            'state': {
                'instance': 'text_action',
                'value': scenario_action,
            }
        }

        if not scenario:
            scenario = self._create_scenario(scenario_name, active_speaker, logic).json()
            scenario.update({"id": scenario["scenario_id"]})
        else:
            self._update_scenario(scenario["id"], scenario_name, active_speaker, logic)

        self.session.post(self.quasar_url + "/scenarios/" + scenario["id"] + "/actions")

    def stop_music(self, active_speaker):
        scenario_name = 'Выключить'
        scenario_action = "Выключить музыку"
        scenario = self._get_scenario(scenario_name)
        logic = {
            'type': 'devices.capabilities.quasar.server_action',
            'state': {
                'instance': 'text_action',
                'value': scenario_action,
            }
        }

        if not scenario:
            scenario = self._create_scenario(scenario_name, active_speaker, logic).json()
            scenario.update({"id": scenario["scenario_id"]})

        self.session.post(self.quasar_url + "/scenarios/" + scenario["id"] + "/actions")

    def _create_scenario(self, name, speaker, logic):
        scenario = {
            'name': name,
            'icon': 'home',
            'triggers': [{
                'type': 'scenario.trigger.voice',
                'value': name
            }],
            'steps': [{
                'type': 'scenarios.steps.actions',
                'parameters': {
                    'requested_speaker_capabilities': [],
                    'launch_devices': [{
                        'id': speaker.id,
                        'capabilities': [logic]
                    }]
                }
            }]
        }

        return self.session.post(self.quasar_url + "/scenarios", json=scenario)

    def _get_scenario(self, name):
        scenarios = self.session.get(self.quasar_url + "/scenarios").json()['scenarios']
        return next((s for s in scenarios if s["name"] == name), None)

    def _update_scenario(self, id, name, speaker, new_logic):
        scenario = {
            'name': name,
            'icon': 'home',
            'triggers': [{
                'type': 'scenario.trigger.voice',
                'value': name
            }],
            'steps': [{
                'type': 'scenarios.steps.actions',
                'parameters': {
                    'requested_speaker_capabilities': [],
                    'launch_devices': [{
                        'id': speaker.id,
                        'capabilities': [new_logic]
                    }]
                }
            }]
        }
        return self.session.put(self.quasar_url + "/scenarios/" + id, json=scenario)

def test(name, bab):
    print(name)
    print(bab)

if __name__ == '__main__':
    from models import UserSession
    session = UserSession("pravdin.vana", "pravdin2001")

    rr = session.stop_music()


