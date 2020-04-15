import datetime
import pathlib as pl
import webdav3.client as wclient

from webdav3.exceptions import RemoteResourceNotFound

from webdav_backup.settings import Log, Credential, Config 

## webdav3.exceptions.RemoteResourceNotFound

class Client:
    def __init__(self):
        self.__client = None

    def connect(self, credential: Credential):
        opts = {"webdav_hostname": credential.url, 
        "webdav_login": credential.login,
        "webdav_password": credential.password}

        try:
            self.__client = wclient.Client(opts)
            Log.Info("Connection established with the remote storage")
        except:
            Log.Error("Failed to connet to your webdav storage. Verify your configuration")

    def setConfig(self, conf: Config):
        self.__config = conf
        self.verifSetup()

    def verifSetup(self):
        if not self.__client.check("/" + self.__config.userhome_webdav):
            self.__client.mkdir( "/" + self.__config.userhome_webdav )
        

    def lastUpdate(self, path: str) -> datetime.datetime:
        """[summary]
        
        Arguments:
            path {str} -- [description]
        
        Returns:
            datetime.datetime -- [description]
        """
        info = self.__client.info(path)
        time = datetime.datetime.strptime( info["modified"], self.__config.datetime_parser )
        return time 

    def remotePath(self, path: pl.Path) -> pl.Path:
        return pl.Path( self.__config.userhome_webdav ) / path.absolute().relative_to(path.home())

    def listDir(self, path: pl.Path) -> list:
        """[summary]
        
        Arguments:
            path {pl.Path} -- [description]
        
        Returns:
            list -- [description]
        """

        remote_path = self.remotePath(path)
        try:
            ret = self.__client.list(str(remote_path))[1:]
        except RemoteResourceNotFound :
            print("ERROR --- the specified remote ressources doesn't exists")
            ret = []
        return ret 

    def remoteIsUpToDate(self, path: pl.Path) -> bool:
        """[summary]
        
        Arguments:
            path {pl.Path} -- [description]
        
        Returns:
            bool -- [description]
        """
        if not self.exists( path ):
            return False 
        time_local = datetime.datetime.fromtimestamp(path.stat().st_mtime)
        path_remote = self.remotePath( path )
        time_remote = self.lastUpdate( str(path_remote) )
        return time_remote >= time_local

    def mkdir(self, path: pl.Path):
        remote_path = self.remotePath( path )
        self.__client.mkdir( str(remote_path) )

    def remote_mkdirp(self, path: pl.Path):
        if not self.exists(path.parent):
            self.remote_mkdirp(path.parent)
            self.mkdir( path )
        else:
            self.mkdir( path )


    def exists(self, path:pl.Path) -> bool:
        remote_path = self.remotePath(path)
        return self.__client.check(str(remote_path))

    def remove(self, path: pl.Path) -> bool:
        remote_path = self.remotePath(path)
        self.__client.clean( str(remote_path) )

    def save(self, path: pl.Path):

        if not self.exists(path.parent):
            Log.Info(f"The path {path.parent} doesn't exists on the remote storage we create it ")
            self.remote_mkdirp( path.parent )

        remote_path = self.remotePath( path )
        self.__client.upload_async(str(remote_path), str(path) )
        


    def restore(self, path: pl.Path):
        remote_path = self.remotePath( path )
        self.__client.download_sync(str(remote_path), str(path))
        Log.Info(f"The file {path} has been succesfully restored")

if __name__=="__main__":
    credential = Credential()
    config = Config()

    client = Client()
    client.connect(credential)
    client.setConfig( config )
