import argparse 
import pathlib as pl
import sys 
from webdav_backup.settings import Log
from webdav_backup.app import Backend




class WDBCli:
    def __init__(self, backend: Backend):
        self.__backend = backend

        self._method_list = [ (f.replace("cmd_", ""), getattr(WDBCli, f).__doc__) for f in dir(WDBCli) if f.startswith('cmd_')]

        usage = """wdb <command> [<args>]

The available commands are:
"""
        usage += "\n".join([ f"  {x}  -  {msg}" for (x, msg) in self._method_list ])

        self.__parser = argparse.ArgumentParser(
            description='WebDav Backup command line interface',
            usage = usage
            )
        self.__parser.add_argument('command', help='Subcommand to run')
        args = self.__parser.parse_args(sys.argv[1:2])

        if not hasattr(self, "cmd_" + args.command):
            self.__parser.print_help()
            exit(1)
        getattr(self, "cmd_"+args.command)()

    def cmd_list(self):
        """List remote data"""
        parser = argparse.ArgumentParser(
            description='List remote data')
        parser.add_argument('path', type=str, default=str(pl.Path.home))
        args = parser.parse_args(sys.argv[2:])
        Log.Debug(f"Ask list for {args.path}")
        ret = self.__backend.listRessource( args.path )
        for x in ret:
            print( x )

    def cmd_save(self):
        """Save local data to remote server"""
        parser = argparse.ArgumentParser(
            description='Save local data to remote server')
        parser.add_argument('path', type=str, nargs="*", default=['all'])
        args = parser.parse_args(sys.argv[2:])
        Log.Info(f'Ask to save {args.path}')
        self.__backend.saveData( args.path )

    def cmd_restore(self):
        """Restore data from the remote server"""
        parser = argparse.ArgumentParser(
            description='Restore data from the remote server')
        parser.add_argument('path', type=str)
        args = parser.parse_args(sys.argv[2:])
        Log.Info(f'Ask to restore {args.path}')
        self.__backend.restoreData(args.path)

    def cmd_config(self):
        """Modify configuration information"""
        parser = argparse.ArgumentParser(
            description='Restore data from the remote server')
        parser.add_argument('key', type=str)
        parser.add_argument("value", type=str)
        args = parser.parse_args(sys.argv[2:])
        Log.Info(f'Ask to change config {args.key} = {args.value}')
        self.__backend.updateConfig( args.key, args.value)

    def cmd_rm(self):
        """ Remove file """ 
        parser = argparse.ArgumentParser(
            description='Remove file')
        parser.add_argument("-r", "--remote", action="store_true", help='Remove the backup of this file on the webdav server', default=False)
        parser.add_argument('path', type=str)
        args = parser.parse_args(sys.argv[2:])
        Log.Info(f'Ask to remove {args.path}')
        self.__backend.removeRessource( args.path , on_remote=args.remote)

if __name__ == '__main__':

    from webdav_backup.settings import Credential, Config
    from webdav_backup.client  import Client

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


### dir(Toto)
### f = getattr(Toto, 'fake')
### f.__doc__