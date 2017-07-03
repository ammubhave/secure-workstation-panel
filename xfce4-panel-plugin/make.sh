#!/bin/sh
gcc -Wall -shared -o libsecure-workstation-plugin.so -fPIC secure-workstation-plugin.c `pkg-config --cflags --libs libxfce4panel-1.0` `pkg-config --cflags --libs gtk+-3.0`