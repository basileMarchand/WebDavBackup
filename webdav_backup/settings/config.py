import pathlib as pl
from traitlets.config.loader import JSONFileConfigLoader
from traitlets.config import Config as traitConfig
import json

from webdav_backup.settings.log import Log 

"""The configuration object use to define some parameters in the webdav_backup. The user parameters are stored in ~/.config/webdav_backup/config.json 


    backup_frequency : following unix crontab syntax
    data to save :  list of path (file or directory)
    
"""

class Config:
    def __init__(self, cpath=""):
        self.__config_path = None
        self.__config = {}

        if cpath != "" and pl.Path(cpath).exists():
            self.__config_path = pl.Path(cpath) 
        elif cpath != "":
            Log.Error("You give an invalide path for config.json")
        else:
            userhome = pl.Path.home()
            path = userhome / ".config" / "webdav_backup" / "config.json"
            if path.exists():
                self.__config_path = path
            else:
                self.initializeConfig()

        self.load()

    def load(self):
        loader = JSONFileConfigLoader(self.__config_path.name, str(self.__config_path.parent.resolve()))
        self.__config = loader.load_config()

    def initializeConfig(self):
        userhome = pl.Path.home()
        path = userhome / ".config" / "webdav_backup" / "config.json"
        if not path.parent.exists():
            path.parent.mkdir()
        
        self.__config_path = path

        data = {"userhome_webdav": "/wdbackup", 
                "datetime_parser": "%a, %d %b %Y %H:%M:%S %Z",
                "data_to_save": []}
        
        self.__config = traitConfig(data)

        with open(self.__config_path, "w") as fid:
            json.dump(self.__config, fid)

    def save(self):
        with open(self.__config_path, "w") as fid:
            json.dump(self.__config, fid, indent=4)

    @property 
    def userhome_webdav(self):
        return self.__config.userhome_webdav

    @property
    def datetime_parser(self):
        return self.__config.datetime_parser

    @property
    def data_to_save(self):
        return self.__config.data_to_save


if __name__=="__main__":

    config = Config()
    