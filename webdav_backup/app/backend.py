import pathlib as pl 

from webdav_backup.settings import Log, Credential, Config
from webdav_backup.client import Client


def fullPath( p: str ):
    ret = pl.Path(p).expanduser().absolute().resolve()
    return ret

class Backend:
    def __init__(self):
        self.__config = None
        self.__credential = None 
        self.__client = None

    @property
    def config(self) -> Config:
        return self.__config

    @config.setter
    def config(self, c: Config):
        self.__config = c

    @property
    def credential(self) -> Credential:
        return self.__credential

    @credential.setter
    def credential(self, c: Credential):
        self.__credential = c

    @property
    def client(self) -> Client:
        return self.__client

    @client.setter
    def client(self, c: Client):
        self.__client = c

    def listRessource(self, path: str ) -> list :
        ressource = fullPath(path)
        ret = self.__client.listDir(ressource)
        return ret 

    def saveData(self, path: list ) -> bool:
        status = True
        new_file = True
        if len(path) == 1 and path[0] == "all":
            path = self.__config.data_to_save
            new_file = False

        for p in path:
            pok = fullPath(p)
            if not self.__client.remoteIsUpToDate(pok):
                self.__client.save(pok)

        ## Add new file in config.data_to_save 
        if new_file:
            count = 0
            for p in path:
                pok = fullPath(p)
                if pok not in self.__config.data_to_save:
                    self.__config.data_to_save.append(str(pok))
                    count += 1
            if count > 0:
                self.__config.save()
                Log.Info(f"{count} new ressources added in the remote storage")

        return status         

    def restore(self, path: str):
        p = fullPath(path)
        self.__client.restore( p )

    def removeRessource(self, path: str, on_remote=False):
        p = fullPath( path )
        if on_remote and self.__client.exists( p ):
            self.__client.remove( p )

        if str(p) not in self.__config.data_to_save:
            Log.Error("You try to delete file which is not in the webdav_backup registry")
            return 
        self.__config.data_to_save.remove( str(p) )
        self.__config.save()


    def updateConfig(self, key: str, value: str, credential=False):
        if credential:
            self.__credential[key] = value
        else:
            self.__config[key] = value 


        self.__config.save()