from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.base import MediaContainer
import typing as t
import os

from src.utils import PabLog

lg = PabLog(__name__)

PLEX_URL = os.getenv('PLEX_URL')
PLEX_TOKEN = os.getenv('PLEX_TOKEN')

class Plex:
    
    def __init__(self):
        self.server: t.Optional[PlexServer] = None
        
    def connect_with_token(self, server_url: str, token: str) -> 'Plex':
        self.server = PlexServer(server_url, token)
        return self
        
    def connect_with_credentials(self, server_url: str, username: str, password: str) -> 'Plex':
        self.server = MyPlexAccount(username, password).resource(server_url).connect()
        return self
        
    def check_sessions(self) -> list[MediaContainer]:
        sessions = self.server.sessions()
        for s in sessions:
            title = s.originalTitle
            players = s.players
            lg.log.info(f"Sesion Found: {title=}, {players=}")
            
        return sessions