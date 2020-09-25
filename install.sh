#!/bin/bash

# this script:
# - expects that yum is upgraded & updated
#    -> python is installed
# - selenium and all its dependencies
# first argument is user under which selenium will be executed and desktop env is running

user="root"
postfix=""
CHROME_VERSION="85.0.4183.87"
# TODO it is possible that last chrome version will be different so change this to version that is closest to version
# fount at https://chromedriver.storage.googleapis.com/index.html
#
PYTHON_VERSION=3.8
PYTHON_VERSION_NODOT=${PYTHON_VERSION/\./}
PYTHON_BIN=/usr/bin/python${PYTHON_VERSION}


function usage {
  printf "This script isntalls python automation.\n As arguments it takes:\m"
  printf "\t-u <username> ; to set ownership of dirs after install\n"
  printf "\t-p <postfix> ; to use in .vitrenv-<postfix> dir"
}


function parse_args
{
  while getopts "u:p:" o; do
    case "${o}" in
      p)
        postfix="-${OPTARG}"
        ;;
      u)
        user=${OPTARG}
        ;;
      *)
        usage
        ;;
    esac
  done
  shift $((OPTIND-1));
}

parse_args "$@"
echo "postfix: $postfix"
echo "user: $user"

# Install virtualenv, libcurl-devel, gcc, wget, unzipx

sudo yum install virtualenv
sudo yum install python${PYTHON_VERSION_NODOT} wget unzip libcurl-devel unzip gcc openssl-devel bzip2-devel -y
# because of installation of python version 3.6
sudo yum install https://centos7.iuscommunity.org/ius-release.rpm -y
# sudo yum install python36u python36u-pip python36u-devel -y

sudo yum install python${PYTHON_VERSION_NODOT} python${PYTHON_VERSION_NODOT}-pip python${PYTHON_VERSION_NODOT}-devel -y

# install chrome
#yum install google-chrome -y
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo dnf localinstall google-chrome-stable_current_x86_64.rpm -y

# https://www.server-world.info/en/note?os=CentOS_8&p=desktop&f=1
#sudo yum groupinstall "GNOME Desktop"
sudo yum groupinstall "Server with GUI"  -y

# https://serverfault.com/questions/363827/how-can-i-run-firefox-on-centos-with-no-display
yum install xorg-x11-server-Xvfb -y
yum install -y x11vnc
# there was an error when -X and these missing packages may have been a reason, idk
yum install -y xterm xauth


# https://www.howtoforge.com/how-to-install-microsoft-teams-linux-on-ubuntu-and-centos/
wget https://packages.microsoft.com/yumrepos/ms-teams/teams-1.3.00.5153-1.x86_64.rpm
dnf install teams-1.3.00.5153-1.x86_64.rpm -y

# https://forums.centos.org/viewtopic.php?t=72036
dnf config-manager --enable PowerTools


# Setup virtual environment
#virtualenv .virtenv${postfix}
rm -rf .virtenv${postfix}

rm -rf geckodriver-v0.20.1-linux32.tar.gz*
rm -rf firefox-59.0.tar.bz2*

virtualenv --python=${PYTHON_BIN} .virtenv${postfix}
source .virtenv${postfix}/bin/activate

# Install base requirements
pip${PYTHON_VERSION} install --upgrade setuptools
pip${PYTHON_VERSION} install selenium chromedriver ipython pycurl xlrd PyuserInput lxml
pip${PYTHON_VERSION} install webdriver_manager
pip${PYTHON_VERSION} install -U pip

export PATH=${PATH}:./
# Install Chromdriver - PATH must include "."

wget https://github.com/mozilla/geckodriver/releases/download/v0.20.1/geckodriver-v0.20.1-linux32.tar.gz
tar -xvzf geckodriver-v0.20.1-linux32.tar.gz

#cd /opt
wget https://download-installer.cdn.mozilla.net/pub/firefox/releases/59.0/linux-x86_64/en-US/firefox-59.0.tar.bz2
tar xfj firefox-59.0.tar.bz2

# wget https://chromedriver.storage.googleapis.com/81.0.4044.138/chromedriver_linux64.zip
# unzip ./chromedriver_linux64.zip

# goto https://chromedriver.storage.googleapis.com/index.html
# CHROME_VERSION="85.0.4183.102"
# wget https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_linux64.zip
wget https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip
unzip -o ./chromedriver_linux64.zip
cp -r chromedriver .virtenv${postfix}/

chown -R ${user}:${user} ./
echo ".virtenv${postfix}" > installed-virtenv.txt


echo -e "\nSetup Complete.\n"

echo "# TODO preparations
# Start X, teams, setup chrome profile so it does not need microphone, g.e. setup it manually and use same profile
# /usr/bin/Xvfb :2 -screen 0 1400x900x24
# X :2
"


#
