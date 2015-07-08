#!/bin/bash

cd ~/app-root/runtime/repo

rm -rf ChannelWorm

git clone https://github.com/VahidGh/ChannelWorm.git

rm ChannelWorm/channelworm/db.sqlite3
rm -rf ChannelWorm/channelworm/web_app/media/*

cp -r ChannelWorm/channelworm/* ~/app-root/runtime/repo
cp -r ChannelWorm/channelworm/.openshift/* ~/app-root/runtime/repo/.openshift

#echo "y" | python manage.py makemigrations
#DJANGO_SETTINGS_MODULE=web_app.settings python -c 'import django; django.setup(); django.core.management.call_command("makemigrations", merge=True, interactive=True)'
#python manage.py migrate
