# WebDav Backup 

## Why this not really usefull app ?

This Python app is just the results of the Covid-19 confinement in France. Indeed since 4 weeks now, the automatic backup of my laptop is not made, I don't have access to the remote server from the outside of my company. 

That's why as a quick and dirty safety solution I made this utility in order to automatically perform backup of my laptop on the nextCloud instance of my company. And I say to me it can be helpful for other peoples. 


The main idea of this app is to offer a backup system transparent for the end user. Transparent in the sense that in the programm corrispondance between local and remote path is automatically managed. In other words, all file path are considered relative to the home user and on the remote webdav server this home is symbolised by a main directory named `wdbackup`.  

## Installation 

As usual just enter the command 

```bash 
pip install . 
```

At its first execution the program will ask you for certain configuration elements, username, password and url of your WebDav server. For information your password is encrypted before to be stored on the disk. Configuration files are stored in `~/.config/webdav_backup/{config, credental}.json`

## Usage 

### Command line interface 

A command line interface comes with webdav_backup, it's `wdb`. Of course you can use the `--help` to have some help about usage. 

#### Push a file or directory to the remote server 

```bash 
wdb save <path>
```

This action push the file or directory to the remote server, for example if you push the file `/home/user/Documents/helloWorld.md` it will be saved on your remote server as `/wdbackup/Documents/helloWorld.md` the `Documents` subdirectory is automatically create. And in addition the path `/home/user/Documents/helloWorld.md` is saved in the webdav_backup internal registry (a complicated term to say a list) as a tracked file. 

The interest of the registry comes from the fact that it makes it possible to define the specific path `all` which allows you to save all the files in the registry.

**Remark**: of course to minimize transfert only file more recent in your local laptop than the remote server are uploaded.

#### Show remote ressources

```bash
wdb list <path>
```

This command can be viewed as a remote `ls`. The subtility comes from the path management. Indeed here the path to specify is a local one but the results corrispond to the content of the associated remote storage. For example if I type 

```bash 
wdb list ~/Documents
```

The displayed results is the content of the directory `/wdbackup/Documents` on the remote webdav server.

#### Restore a file or directory from the remote backup 

```bash
wdb restore <path>
```

This command perform the download of a saved file to restore this one from the last saved version. As usual in `wdb` the specified path is a local path.

#### Untrack file 

```bash 
wdm rm [--remote] <path>
```

This subcommand allow you to untrack the data specified by `path`, i.e. the `wdb rm ~/Documents/helloWorld.md` remove the file from the internal registry. The file on the disk stay in place and the copy in your Webdav also. It's just that at the next backup your local file will not be saved.

If you want to remove also the remote copy of the file you should use the `--remote` option to unregister **and** delete the remote copy. But the local file already exists. 


## The todo list

* Embedded deamon for automatic periodic backup in place of a crontab
* Do some test 
* Check error management, verify all is catch 
* Add a GUI ? 

