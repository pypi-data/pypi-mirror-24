#!/bin/sh
set -e
cwd=`pwd`
src="libogg-1.3.2"
if [ "$1" = "" ]; then
  dest=`pwd`/../build
else
  dest=$1
fi
mkdir -p ${dest}/src
cd ${dest}/src

if [ ! -d "${src}" ]; then
  if [ `which curl` ]; then
    cmd="curl -k -O -L"
  else
    cmd="wget"
  fi
  ${cmd} https://gr-framework.org/downloads/3rdparty/${src}.tar.gz
  tar -xf ${src}.tar.gz
fi

cd ${src}

./configure --prefix=${dest} --libdir=${dest}/lib --disable-shared --with-pic \
  ${OGG_EXTRA_CONFIGURE_FLAGS}
make -j4
make install

cd ${cwd}

