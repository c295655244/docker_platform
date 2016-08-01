@echo off
netsh interface ip set address "bridge" static 10.0.0.3 255.255.255.0 10.0.0.1 1
