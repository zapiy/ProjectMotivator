from django.contrib.sessions.backends.db import SessionStore
from django.utils.crypto import get_random_string
import string 


VALID_KEY_CHARS = (
    string.ascii_lowercase + string.digits 
    + string.ascii_uppercase
)

class SessionStore(SessionStore):
    
    def _get_session_from_db(self):
        self._model = super()._get_session_from_db()
        return self._model
    
    @classmethod
    def get_model_class(cls):
        from ..models import SessionModel
        return SessionModel
    
    def _get_new_session_key(self):
        "Return session key that isn't being used."
        while True:
            session_key = get_random_string(64, VALID_KEY_CHARS)
            if not self.exists(session_key):
                return session_key
