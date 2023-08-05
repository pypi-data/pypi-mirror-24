#!/usr/bin/env bash

PROJECT_NAME=${PROJECT_NAME:-mistral}
CFGFILE_NAME=${PROJECT_NAME}.conf.sample

if [ -e etc/${PROJECT_NAME}/${CFGFILE_NAME} ]; then
    CFGFILE=etc/${PROJECT_NAME}/${CFGFILE_NAME}
elif [ -e etc/${CFGFILE_NAME} ]; then
    CFGFILE=etc/${CFGFILE_NAME}
else
    echo "${0##*/}: can not find config file"
    exit 1
fi

TEMPDIR=$(mktemp -d /tmp/${PROJECT_NAME}.XXXXXX)
trap "rm -rf $TEMPDIR" EXIT

oslo-config-generator --config-file tools/config/config-generator.mistral.conf --output-file ${TEMPDIR}/${CFGFILE_NAME}

if ! diff -u ${TEMPDIR}/${CFGFILE_NAME} ${CFGFILE}
then
   echo "${0##*/}: ${PROJECT_NAME}.conf.sample is not up to date."
   echo "${0##*/}: Please run tox -egenconfig."
   exit 1
fi
