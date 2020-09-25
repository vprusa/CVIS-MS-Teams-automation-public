# Setup Teams from links and user ids

This script is for automating adding participants to teams in MS Teams when links are giver.

## Installation

Run
```
# ./install.sh -p <postfix> -u <user>
```
as root that installs all libraries and requirements. *<user>* is non-root account under which browser can be opened without admin privileges

*-p <postfix>* sets virtualenv postfix g.e. *-p local* generates *.virtenv-local* dir 

## Notest

IDE was used pycharm from idea

All execution configuration is in conf/propertie.properties

Path to used properties file can be changed with ```export PROPERTIES_FILE_NAME=./pathToProperties.properties```  

If you want to get rid of modal dialogs and popups requiresing access to resource such as mic, cam, etc. use BROWSER_PROFILE_DIR property

JSON file from property *JSON_FILE_PATH* should be in a format:
```json
[ 
{"https://link1": ["id1","id2","id3"]},
{"https://link1": ["id2","id4","id5"]}, 
// ... 
]
```

There has to be manual setup that requires to:
- start x-session g.e. ```X :2```
- start MS Teams ```export DISPLAY=:2 ; teams```
- start and setup google-chrome:
-- login to MS Teams (or AD or other) accounts, 
-- enable automatic teams opening in external app (depends on system)
-- optionaly 'Unlock Profile And Start Chrome' or simillar
- If executed on remote system then I recommend to use XForwarding etc. with ```./run.sh X_IP:X_DUSPLAY```