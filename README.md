# osx_launchctl_cleaner

请在一个健康的系统上执行次脚本，会编译出一个删去此版本中launchctl启动项并把剩余显示出来的脚本

Please execute this in a healthy system. Then it will generate another script showing all `launchctl` items without those in this system.

# How to use
```shell script
# in a healthy system
python3 clean_launchctl.py output.py
# then in the target
$ python3 output.py
```
