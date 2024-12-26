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
    """
    A class to interact with a Plex Media Server.
    """

    def __init__(self):
        """
        Initialize a Plex object.

        The server attribute is initially set to None and will be populated
        when a connection is established.
        """
        self.server: t.Optional[PlexServer] = None
        
    def connect_with_token(self, server_url: str, token: str) -> 'Plex':
        """
        Connect to a Plex server using a URL and token.

        Args:
            server_url (str): The URL of the Plex server.
            token (str): The authentication token for the Plex server.

        Returns:
            Plex: The current Plex object with an established server connection.
        """
        self.server = PlexServer(server_url, token)
        return self
        
    def connect_with_credentials(self, server_url: str, username: str, password: str) -> 'Plex':
        """
        Connect to a Plex server using a URL and user credentials.

        Args:
            server_url (str): The URL of the Plex server.
            username (str): The username for the Plex account.
            password (str): The password for the Plex account.

        Returns:
            Plex: The current Plex object with an established server connection.
        """
        self.server = MyPlexAccount(username, password).resource(server_url).connect()
        return self
        
    def check_sessions(self) -> list[MediaContainer]:
        """
        Check and log the current active sessions on the Plex server.

        This method retrieves all active sessions from the connected Plex server,
        logs the title and players for each session, and returns the list of sessions.

        Returns:
            list[MediaContainer]: A list of MediaContainer objects representing the active sessions.
        """
        sessions = self.server.sessions()
        for s in sessions:
            title = s.originalTitle
            players = s.players
            lg.log.info(f"Sesion Found: {title=}, {players=}")
            
        return sessions
    
    def get_butler_tasks(self) -> list[MediaContainer]:
        lg.log.info([task.name for task in self.server.butlerTasks()])
        self.server.createCollection()