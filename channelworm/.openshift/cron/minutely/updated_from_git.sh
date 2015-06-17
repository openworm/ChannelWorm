#!/bin/bash

cd ~/app-root/runtime/repo

rm -rf ChannelWorm

git clone https://github.com/VahidGh/ChannelWorm.git

rm ChannelWorm/channelworm/db.sqlite3

cp -r ChannelWorm/channelworm/* ~/app-root/runtime/repo
cp -r ChannelWorm/channelworm/.openshift/* ~/app-root/runtime/repo/.openshift

