from models import UserSession

class SessionStore:
    def __init__(self):
        self.sessions = []

    def append(self, session):
        self.sessions.append(session)

    def remove(self, session):
        self.sessions.remove(session)

    def get_session(self, token):
        return next((s for s in self.sessions if s.token == token), None)