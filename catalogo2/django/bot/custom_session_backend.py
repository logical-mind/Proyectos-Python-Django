from django.contrib.sessions.backends.base import SessionBase

class CustomSessionStore(SessionBase):
    def load(self):
        # Implementa aquí la lógica para cargar la sesión
        return {}

    def create(self):
        # Implementa aquí la lógica para crear una nueva sesión
        pass

    def save(self, must_create=False):
        # Implementa aquí la lógica para guardar la sesión
        pass

    @classmethod
    def exists(cls, session_key):
        # Implementa aquí la lógica para verificar si la sesión existe
        return False