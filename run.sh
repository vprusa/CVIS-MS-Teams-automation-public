#!/bin/bash
# ! make sure that:
# - X is runing on DISPLAY=:2
# - teams is running

[[ -z $1 ]] && export DISPLAY=:2 || export DISPLAY=$1
export T_NOW_STR=`date "+%Y-%m-%d_%H-%M-%S"`
export T_LOG_FILE=./run.${T_NOW_STR}.log

LATEST_LOG_FILE=./run.latest.log

[[ -z ${LOG_FILE} ]] && export LOG_FILE=${T_LOG_FILE}
rm -rf ${LATEST_LOG_FILE}
ln -s ${LOG_FILE} ${LATEST_LOG_FILE}

#pkill -9 -f firefox
pkill -9 -f chrome

VIRT_ENV_DIR=`cat installed-virtenv.txt`
echo "Using virtenv: ${VIRT_ENV_DIR}"

source ${VIRT_ENV_DIR}/bin/activate

PROPERTIES_FILE_NAME_2=""

if [ ! -z ${PROPERTIES_FILE_NAME} ]; then
  PROPERTIES_FILE_NAME_2=${PROPERTIES_FILE_NAME}
fi

if [[ $1 = *".properties"* ]] ; then
  PROPERTIES_FILE_NAME_2=$1
elif [[ $1 = *"test"* ]] ; then
  PROPERTIES_FILE_NAME_2="properties-test.properties"
fi

if [ -z ${PROPERTIES_FILE_NAME_2} ]; then
PROPERTIES_FILE_NAME_2="properties.properties"
fi

echo "PROPERTIES_FILE_NAME_2: ${PROPERTIES_FILE_NAME_2}"
if [ ! -z ${PROPERTIES_FILE_NAME_2} ]; then
  DOWNLOAD_DIR_2=`cat ./conf/$PROPERTIES_FILE_NAME_2 | grep "BROWSER_DOWNLOAD_DIR=" | grep -v '#'`
  export ${DOWNLOAD_DIR_2}
  #source ./conf/${PROPERTIES_FILE_NAME_2}
fi

echo "Used DOWNLOAD_DIR: ${DOWNLOAD_DIR_2}"

NOW=`date +%Y-%m-%d_%H-%M-%S`
BROWSER_DOWNLOAD_BASE_DIR=${BROWSER_DOWNLOAD_DIR}
export BROWSER_DOWNLOAD_DIR="${BROWSER_DOWNLOAD_DIR}/${NOW}/"
mkdir -p ${BROWSER_DOWNLOAD_DIR}/debug/


python -u -c "from handleTeams import handleTeams
d = handleTeams()
d.getSessionAndLogin()
d.updateTeams()
" ${PROPERTIES_FILE_NAME_2}
