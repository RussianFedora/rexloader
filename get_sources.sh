#!/bin/bash

ORIGNAME=rexloader
VERSION=0.1
SVN_REVISION=334
NAME=${ORIGNAME}-${VERSION}.svn${SVN_REVISION}

rm -rf ${ORIGNAME}
svn co -r $SVN_REVISION http://rexloader.googlecode.com/svn/trunk/ ${ORIGNAME} >/dev/null
find ${ORIGNAME} -name ".svn" -exec rm -rf {} \; 2>/dev/null
mv ${ORIGNAME} ${NAME}

tar cfJ ${NAME}.tar.xz ${NAME}
rm -rf ${NAME}
