#!/bin/sh -e

CLASS_VERSION=$1; shift
PREFIX="$1"; shift
INSTALLDIR="$1"; shift

TMP="tmp-class-v$CLASS_VERSION"
LOGFILE="build.log"

START=$(pwd)
mkdir -p $PREFIX;
ROOT=`dirname $0`/../
cd $ROOT/depends; mkdir -p $TMP
if ! [ -f $ROOT/depends/class-v$CLASS_VERSION.tar.gz ]; then
wget https://github.com/lesgourg/class_public/archive/v$CLASS_VERSION.tar.gz \
    -O $ROOT/depends/class-v$CLASS_VERSION.tar.gz
fi

if ! [ -d $TMP/class_public-$CLASS_VERSION ]; then
    gzip -dc $ROOT/depends/class-v$CLASS_VERSION.tar.gz | tar xf - -C $TMP
    (
        cd $TMP/class_public-$CLASS_VERSION
        patch -p1 < $ROOT/depends/class-2.6.0-a_max.patch || exit 1
        patch -p1 < $ROOT/depends/class-2.6.0-tol-ncdm.patch || exit 1
    ) || exit 1
fi

# add phi_prime

# copy the Makefile
cp Makefile $TMP/class_public-$CLASS_VERSION
cd $TMP/class_public-$CLASS_VERSION

echo $ROOT/$PREFIX/data
mkdir -p $ROOT/$PREFIX/data

# copy all *.dat files to install dir
find . -type f -name "*.dat" -print0 |  xargs -0  tar cf - | tar xvf - -C $ROOT/$PREFIX/data
find . -type f -name "*_ref.pre" -print0 |  xargs -0  tar cf - | tar xvf - -C $ROOT/$PREFIX/data
find . -type f -name "*.ini" -print0 |  xargs -0  tar cf - | tar xvf - -C $ROOT/$PREFIX/data

make CLASSCFG=$ROOT/depends/class.cfg libclass.a
cp -r include $START/$PREFIX/
mkdir -p $START/$PREFIX/lib
cp libclass.a $START/$PREFIX/lib
