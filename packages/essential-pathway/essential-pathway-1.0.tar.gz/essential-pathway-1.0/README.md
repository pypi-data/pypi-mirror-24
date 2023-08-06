Essential-pathway Documentation v1.0
====================================
**Quick Links**
---------------
- `Project <https://github.com/realasking/essential-pathway>`
- `Author's Homepage <https://realasking.wordpress.com>`
- `Author's Emails <realasking@gmail.com,tomwangsim@163.com>`
- `Manual of Environment Modules <http://modules.sourceforge.net/tcl/module.html>`

Introduction
------------
Essential-pathway (short for ep) is a tool that helps people quickly access to their most commonly used folders in command line in some 
operation systems like linux. A PATHWAY is an environment variable defined by users using this tool, which consists of a pathway name, a path and a comment. 
One can add, modify or delete their definations of PATHWAYS to their folders' paths, or do some comments to prevent forgetting.

This tool have only been tested in archlinux and might not be able to use under root. It's based on Environment Modules (short for em) and is released under LGPLv3.

Dependencies
------------
The native Tcl version Environment Modules package is needed by this tool, while a $HOME/.modulespath with a contained user modulefiles folder 
should also be created by user before using ep. 

An example of $HOME/.modulespath:<br>
```bash
modules
```

And a folder name modules should be created in $HOME/

After that, the following sentences must be add to $HOME/.bashrc to keep em works properly:<br>
```bash
export MODULEPATH=${HOME}/modules:$MODULEPATH <br>
source /etc/modules-tcl/init/bash<br>
```
Prettytable, an elegant table processing python library is also needed.

Ep can be installed when all dependencies are met.

Installation
------------
```bash 
git clone https://github.com/realasking/essential-pathway.git 
cd essential-pathway 
sudo python ./setup.py install 
```
Or you can use pip 
```bash 
pip install essential-pathway 
```

Usage
-----
Notice:<br>
Before each operations below, please execute \'module unload epath\' first.<br>
To make pathways usable, please execute \'module load epath\' or add this sentence to $HOME/.bashrc.<br>
\'ep u\' just delete epath, and will keep the database file in $HOME/.ep.

Quckly add current foler to a pathway<br>
```bash 
ep a PATHWAY_NAME
```
Listing exsit pathways<br>
```bash 
ep l
```
Create a pathway<br>
```bash
ep a PATHWAY_NAME PATH_TO_YOUR_FOLDER
```
Make or change a short comment for an exists pathway<br>
```bash 
ep c PATHWAY_NAME 
```
Modify a pathway<br>
```bash 
ep m PATHWAY_NAME PATH_TO_NEW_FOLDER
```
Delete a pathway<br>
```bash 
ep d PATHWAY_NAME 
```
Check paths' availabilities and automatic delete invalid ones<br>
```bash 
ep k
```
Refresh the Env-module<br>
```bash 
ep r
```
Backup settings<br>
```bash 
ep b 
``` 
Uninstall all settings<br>
```bash 
ep u 
```

realasking
Aug 15,2017
