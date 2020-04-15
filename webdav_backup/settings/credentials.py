
import pathlib as pl
from traitlets.config import Config
from traitlets.config.loader import JSONFileConfigLoader
import cryptography.fernet as cfe
import getpass
import json 

from .log import Log

class Credential:
    def __init__(self, cpath=None):
        self.__credential_path = ""
        self.__config = {}
        self.__crypto = None

        if not cpath is None and pl.Path(cpath).exists():
            self.__credential_path = pl.Path(cpath) 

        elif not cpath is None:
            Log.Error("You give an invalide path for credential")
        else:
            userhome = pl.Path.home()
            path = userhome / ".config" / "webdav_backup" / "credential.json"
            if path.exists():
                self.__credential_path = path
            else:
                self.initalizeCredential()

        self.load()


    def load(self):
        ## Load the key 
        keypath = self.__credential_path.parent / "useless_or_not"
        with open(keypath) as fid:
            token = fid.read()
        
        self.__crypto = cfe.Fernet(token.encode())
        loader = JSONFileConfigLoader(self.__credential_path.name, str(self.__credential_path.parent.resolve()))
        self.__config = loader.load_config()

    def initalizeCredential(self):
        userhome = pl.Path.home()
        path = userhome / ".config" / "webdav_backup" / "credential.json"
        if not path.parent.exists():
            path.parent.mkdir()
        
        self.__credential_path = path
        ### Ask user for credential 
        uname = input("Username : ")
        url   = input("The WebDav url : ")
        password = getpass.getpass("Your password : ")


        token = cfe.Fernet.generate_key()
        keypath = self.__credential_path.parent / "useless_or_not"
        with open( keypath, "w" ) as fid:
            fid.write( token.decode() )

        self.__crypto = cfe.Fernet(token)

        cpassword = self.__crypto.encrypt(password.encode()).decode()

        data = {"username": uname, "url": url, "password": cpassword}
        
        self.__config = Config(data)

        with open(self.__credential_path, "w") as fid:
            json.dump(self.__config, fid)

    @property
    def login(self):
        return self.__config['username']

    @property 
    def url(self):
        return self.__config['url']

    @property 
    def password(self):
        pword = self.__crypto.decrypt(self.__config["password"].encode()).decode()
        return pword


if __name__=='__main__':

    c = Credential()
