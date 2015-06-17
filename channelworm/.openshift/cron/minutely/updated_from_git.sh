#!/bin/bash

cd ~/app-root/runtime/repo

rm -rf ChannelWorm

git clone https://github.com/joebowen/ChannelWorm.git

cp -r ChannelWorm/channelworm/* ~/app-root/runtime/repo
cp -r ChannelWorm/channelworm/.openshift/* ~/app-root/runtime/repo/.openshift

