
from .backend import Backend
from .cli import WDBCli

from webdav_backup.settings import Credential, Config
from webdav_backup.client  import Client


def main():
    config = Config()
    credential = Credential()
    client = Client()
    client.connect(credential)
    client.setConfig(config)

    backend = Backend()
    backend.client = client
    backend.config = config
    backend.credential = credential

    WDBCli( backend )